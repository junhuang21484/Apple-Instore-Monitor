import logging
import threading


class ProxyService:
    def __init__(self):
        self.proxies_list = self.load_proxies()
        self._proxy_id = 0
        self._id_lock = threading.Lock()

    def load_proxies(self):
        proxies_list = []
        with open("data/proxies.txt", 'r') as f:
            proxies = f.readlines()

            for proxy in proxies:
                proxy = proxy.strip()
                proxy_parts = proxy.split(":")

                if len(proxy_parts) == 2:  # IP:Port proxy
                    proxies_list.append(f"http://{proxy_parts[0]}:{proxy_parts[1]}")
                elif len(proxy_parts) == 4:  # IP:PORT:USER:AUTH proxy
                    proxies_list.append(f"http://{proxy_parts[2]}:{proxy_parts[3]}@{proxy_parts[0]}:{proxy_parts[1]}")

        logging.info(f"{len(proxies_list)} proxies loaded")
        return proxies_list

    def get_proxy(self):
        # Thread safe round robin
        with self._id_lock:
            if not self.proxies_list:
                raise RuntimeError("No valid proxies are loaded")
            proxy = self.proxies_list[self._proxy_id]
            self._proxy_id = (self._proxy_id + 1) % len(self.proxies_list)
            return proxy
