from services.apple_service import AppleService
from services.notify_service import NotifyService
from services.proxy_service import ProxyService

import threading
import logging
import time


class MonitorService:
    def __init__(self, apple_service: AppleService, notify_service: NotifyService, proxy_service: ProxyService, monitor_setting: dict, product_list: dict):
        self.apple_service: AppleService = apple_service
        self.notify_service: NotifyService = notify_service
        self.proxy_service: ProxyService = proxy_service
        self.setting = monitor_setting
        self.product_list = product_list
        self.running_threads = []

        self.error_event = threading.Event()
        self.error_event.clear()
        self.on_error = False
        self.error_remove_run = False

    def reset_error(self, error_delay):
        self.error_event.set()
        logging.info(f"Error delay, sleeping for {error_delay}")
        time.sleep(error_delay)
        self.on_error = False
        self.error_event.clear()

    def monitor_task(self, product_id, error_delay, monitor_delay):
        near_zip = self.setting['near_zip']
        product_name = self.product_list[product_id]
        task_proxy = self.proxy_service.get_proxy() if self.setting['use_proxy'] else {}
        while True:
            if not self.on_error:
                status_code, json_data = self.apple_service.get_data(product_id, near_zip, task_proxy)
                if status_code == 200 and json_data:
                    avi_list = self.apple_service.parse_data(product_id, json_data)
                    if avi_list:
                        self.notify_service.process_notification(avi_list, product_name)
                elif self.setting['use_proxy']:
                    logging.error("Switching to a new proxy")
                    task_proxy = self.proxy_service.get_proxy()
                else:
                    self.on_error = True
                    self.reset_error(error_delay)
            else:
                self.error_event.wait()
                self.on_error = False

            time.sleep(monitor_delay)

    def start_monitor(self):
        error_delay = self.setting['delay']['error_delay']
        monitor_delay = self.setting['delay']['monitor_delay']
        load_up_delay = self.setting['delay']['load_up_delay']
        for product_id in self.product_list:
            logging.info(f"Loading up product id {self.product_list[product_id]} ({product_id})")
            task_thread = threading.Thread(target=self.monitor_task, args=(product_id, error_delay, monitor_delay))
            task_thread.start()
            self.running_threads.append(task_thread)
            time.sleep(load_up_delay)

        logging.info("All tasks have started running")
        for thread in self.running_threads:
            thread.join()

