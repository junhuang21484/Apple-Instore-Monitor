from services.apple_service import AppleService
from services.monitor_service import MonitorService
from services.notify_service import NotifyService
from services.proxy_service import ProxyService

import json
import logging
import traceback

log_f = "%(asctime)s [%(thread)d-%(levelname)s] - %(message)s"
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.basicConfig(
    format=log_f,
    level=logging.DEBUG,
)

setting = json.load(open("data/monitor_data.json"))
product_list = setting['product_list']
monitor_setting = setting['monitor']
notification_setting = setting['notifications']

apple_ser = AppleService(product_list)
notify_ser = NotifyService(notification_setting)
proxy_ser = ProxyService()
monitor_ser = MonitorService(apple_ser, notify_ser, proxy_ser, monitor_setting, product_list)

try:
    monitor_ser.start_monitor()
except Exception as e:
    traceback.print_exc()
    logging.error(f"An exception occurred: {e}")
