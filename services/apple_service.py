import logging
import requests
from urllib.parse import urlencode

from services.models import AppleAviData


class AppleService:
    FULFILLMENT_URL = "https://www.apple.com/shop/fulfillment-messages"

    def __init__(self, product_list):
        self.product_list = product_list
        self.headers = {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/153.0.0.0 Safari/537.36",
            "Sec-CH-UA": '"Google Chrome";v="153", "Not_A Brand";v="8", "Chromium";v="153"',
            "Sec-CH-UA-Mobile": "?0",
            "Sec-CH-UA-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
        }

    def get_data(self, product_id: str, near_zip: str, proxy):
        logging.info(f"Fetching stock status for {self.product_list[product_id]} ({product_id})")
        params = {
            "fae": "true",
            "pl": "true",
            "mts.0": "regular",
            "cppart": "UNLOCKED/US",
            "parts.0": product_id,
            "location": near_zip,
        }
        req_url = f"{self.FULFILLMENT_URL}?{urlencode(params, safe='/')}"
        proxies = {"http": proxy, "https": proxy} if proxy else None

        try:
            response = requests.get(
                req_url,
                headers=self.headers,
                proxies=proxies,
                timeout=10,
            )

            if response.status_code == 200:
                return response.status_code, response.json()

            logging.error(f"Incorrect status code [{response.status_code}]")
            return response.status_code, {}
        except (requests.RequestException, ValueError) as error:
            logging.error("Apple request failed (%s)", type(error).__name__)
            return 500, {}

    def parse_data(self, product_id, json_data) -> list[AppleAviData]:
        avi_list = []
        if 'stores' not in json_data['body']['content']['pickupMessage']:
            return avi_list

        all_store_data = json_data['body']['content']['pickupMessage']['stores']
        for store_data in all_store_data:
            store_name = store_data['storeName']
            address_dict = store_data["retailStore"]["address"]
            store_address = f"{address_dict['street']}\n{address_dict['city']} - {address_dict['postalCode']}"
            store_phone_email = store_data["storeEmail"] + " - " + store_data["phoneNumber"]
            avi = store_data['partsAvailability'][product_id]['pickupDisplay']

            if avi != "unavailable":
                logging.info(f"{self.product_list[product_id]} ({product_id}) has stock been found at {store_name}")
                avi_list.append(AppleAviData(
                    storeName=store_name,
                    storeAddr=store_address,
                    storeContact=store_phone_email,
                    productId=product_id,
                ))

        return avi_list
