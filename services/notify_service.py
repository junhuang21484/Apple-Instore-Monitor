from pynotifier import Notification
from services.models import AppleAviData

import logging
import requests


class NotifyService:
    def __init__(self, notification_setting):
        self.setting = notification_setting

    def send_discord_notification(self, avi_list: list[AppleAviData], product_name: str):
        for store_avi in avi_list:
            store_name = store_avi.storeName

            embed_data = {
                'color': 3462635, 'title': 'Detected Monitor Item In-store Pickup Avi!',
                'fields': [
                    {'name': '__Product Name__', 'value': product_name, 'inline': True},
                    {'name': '__Store Name__', 'value': store_name, 'inline': True},
                    {'name': '__Store Info__',
                     'value': f'**Address Detail:**\n{store_avi.storeAddr}\n\n**Contact Info**\n{store_avi.storeContact}',
                     'inline': False}
                ]
            }

            webhook = self.setting['discord']['webhook']
            msg = "@everyone" if self.setting['discord']['mention_all'] else ""
            req = requests.post(webhook, json={'content': msg, 'embeds': [embed_data]})
            if req.status_code != 204:
                logging.info("Error sending discord notification")

    def send_desktop_notification(self, avi_list: list[AppleAviData], product_name: str):
        for store_avi in avi_list:
            try:
                Notification(
                    title=product_name + f" [{store_avi.productId}]",
                    description=f'Store: {store_avi.storeName}',
                    duration=3,
                    urgency='normal'
                ).send()
            except AttributeError:
                logging.error("Error sending desktop notification")

    def process_notification(self, avi_list: list[AppleAviData], product_name: str):
        excluded_stores = set(self.setting.get("exclude_store_list", []))
        avi_list = [item for item in avi_list if item.storeName not in excluded_stores]
        if not avi_list:
            return

        if self.setting["discord"]["on"]:
            self.send_discord_notification(avi_list, product_name)

        if self.setting["desktop"]["on"]:
            self.send_desktop_notification(avi_list, product_name)
