from dhooks import Webhook, Embed
from pynotifier import Notification

import requests
import json
import time
import threading
import datetime


def print_log(msg: str):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{current_time}]: {msg}")


class Monitor:
    def __init__(self):
        monitor_data = json.load(open('monitor_data.json', 'r', encoding='UTF-8'))
        self.product_list = monitor_data['product_list']
        self.setting = monitor_data['setting']

        self.webhook = Webhook(
            url=self.setting['webhook_url'],
            avatar_url="https://thebait.no/wp-content/uploads/2020/11/apple-logo-mac-pro-2019.jpg"
        )

        self.header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.38"
        }

        self.cooldown_list = []

    def get_data(self, product_id: str) -> dict:
        req_url = f"https://www.apple.com/shop/fulfillment-messages?pl=true&mt=compact&cppart=UNLOCKED/US&parts.0={product_id}&searchNearby=true&store={self.setting['store_near']}"
        req = requests.get(req_url, headers=self.header)
        if req.status_code == 200:
            return req.json()

        return {}

    def parse_data(self, product_id, json_data) -> list:
        return_list = []
        all_store_data = json_data['body']['content']['pickupMessage']['stores']
        for store_data in all_store_data:
            store_name = store_data['storeName']
            address_dict = store_data["retailStore"]["address"]
            store_address = f"{address_dict['street']}\n{address_dict['city']} - {address_dict['postalCode']}"
            store_phone_email = store_data["storeEmail"] + " - " + store_data["phoneNumber"]
            avi = store_data['partsAvailability'][product_id]['pickupDisplay']

            if avi != "unavailable":
                if (product_id, store_name) not in self.cooldown_list:
                    print_log(f"{self.product_list[product_id]} ({product_id}) has stock been found")
                    return_list.append((store_name, store_address, store_phone_email, product_id))
                    self.cooldown_list.append((product_id, store_name))

        return return_list

    def send_embed(self, avi_list: list):
        for store_avi in avi_list:
            store_name = store_avi[0]
            store_add = store_avi[1]
            store_phone_email = store_avi[2]
            product_id = store_avi[-1]
            product_name = self.product_list[product_id]

            embed = Embed(title="Detected Monitor Item In-store Pickup Avi!", color=0x34d5eb)
            embed.add_field("__Product Name__", product_name)
            embed.add_field("__Store Name__", store_name)
            embed.add_field(f"__Store Info__",
                            f"**Address Detail:**\n"
                            f"{store_add}\n\n"
                            f"**Contact Info**\n"
                            f"{store_phone_email}",
                            inline=False)

            self.webhook.send(content="@everyone", embed=embed)

    def send_desktop_notification(self, avi_list: list):
        for store_avi in avi_list:
            store_name = store_avi[0]
            product_id = store_avi[-1]
            product_name = self.product_list[product_id]

            try:
                Notification(
                    title=product_name + f" [{product_id}]",
                    description=f'Store: {store_name}',
                    duration=3,
                    urgency='normal'
                ).send()
            except AttributeError:
                print_log("Error sending desktop notification")

    def remove_cool_down_item(self):
        while True:
            self.cooldown_list = []
            time.sleep(self.setting['item_cooldown'])

    def start_monitor(self, product_id):
        while True:
            json_data = self.get_data(product_id)
            if json_data:
                parse_data = self.parse_data(product_id, json_data)
                self.send_embed(parse_data)

                if self.setting['notifications']['desktop']:
                    self.send_desktop_notification(parse_data)

            time.sleep(self.setting['delay'])

    def start_threads(self):
        running_thread = []

        t = threading.Thread(target=self.remove_cool_down_item)
        t.start()
        print_log("Starting cooldown remover")

        for product_id in self.product_list:
            print_log(f"LOADING UP PRODUCT ID [{product_id}] - {self.product_list[product_id]}")
            task_thread = threading.Thread(target=self.start_monitor, args=(product_id,))
            task_thread.start()
            running_thread.append(task_thread)

        print_log("ALL PRODUCTS LOADED UP AND MONITORING!")

        t.join()
        for thread in running_thread:
            thread.join()


if __name__ == '__main__':
    m = Monitor()
    m.start_threads()
