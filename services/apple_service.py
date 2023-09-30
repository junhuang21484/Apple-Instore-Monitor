import logging
import requests


class AppleService:
    def __init__(self, product_list):
        self.product_list = product_list
        self.header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.38"
        }

    def get_data(self, product_id: str, near_zip: str):
        logging.info(f"Fetching stock status for {self.product_list[product_id]} ({product_id})")
        req_url = f"https://www.apple.com/shop/fulfillment-messages?pl=true&mts.0=regular&cppart=UNLOCKED/US&parts.0={product_id}&location={near_zip}"
        req = requests.get(req_url, headers=self.header)
        if req.status_code == 200:
            return req.status_code, req.json()
        else:
            logging.error(f"Incorrect status code [{req.status_code}]")
            return req.status_code, {}

    def parse_data(self, product_id, json_data) -> list:
        avi_list = []
        all_store_data = json_data['body']['content']['pickupMessage']['stores']
        for store_data in all_store_data:
            store_name = store_data['storeName']
            address_dict = store_data["retailStore"]["address"]
            store_address = f"{address_dict['street']}\n{address_dict['city']} - {address_dict['postalCode']}"
            store_phone_email = store_data["storeEmail"] + " - " + store_data["phoneNumber"]
            avi = store_data['partsAvailability'][product_id]['pickupDisplay']

            if avi != "unavailable":
                logging.info(f"{self.product_list[product_id]} ({product_id}) has stock been found [{avi}]")
                avi_list.append((store_name, store_address, store_phone_email, product_id))

        return avi_list

