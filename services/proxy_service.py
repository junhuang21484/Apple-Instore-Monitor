import logging
import random


class ProxyService:
    def __init__(self):
        self.proxies_list = self.load_proxies()

    def load_proxies(self):
        proxies_list = []
        with open("data/proxies.txt", 'r') as f:
            proxies = f.readlines()

            for proxy in proxies:
                proxy = proxy.strip()
                proxy_parts = proxy.split(":")

                if len(proxy_parts) == 2:  # IP:Port proxy
                    pass
                elif len(proxy_parts) == 4:  # IP:PORT:USER:AUTH proxy
                    proxies_list.append(f"http://{proxy_parts[2]}:{proxy_parts[3]}@{proxy_parts[0]}:{proxy_parts[1]}")

        logging.info(f"{len(proxies_list)} proxies loaded")
        return proxies_list

    def get_proxy(self):
        return random.choice(self.proxies_list)