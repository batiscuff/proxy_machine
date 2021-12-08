import json
import logging
from datetime import date
from time import sleep
from typing import List, Set

import brotli
import requests
from user_agent import generate_user_agent

from .tools.proxies_manipulation import short_url

logger = logging.getLogger(__name__)


class CheckerProxyArchive:
    def __init__(self) -> None:
        current_date = date.today().strftime("%Y-%m-%d")
        self.URL = f"https://checkerproxy.net/api/archive/{current_date}"
        self.REFERER_URL = f"https://checkerproxy.net/archive/{current_date}"
        self.proxies_set: Set[str] = set()
        cookies = self.get_cookies()
        self.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cookie": cookies[0] if len(cookies) > 0 else "",
            "Referer": self.REFERER_URL,
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "User-Agent": generate_user_agent(),
        }

    def get_cookies(self) -> List[str]:
        """Loads cookies from the page and returns as string"""
        r_cookies = requests.get(
            self.REFERER_URL,
            headers={"User-Agent": generate_user_agent()},
            timeout=6,
        )
        cookies_dict = r_cookies.cookies.get_dict()
        return [f"{k}={v}" for k, v in cookies_dict.items()]

    def parse_proxies(self) -> Set[str]:
        try:
            r = requests.get(self.URL, headers=self.headers, timeout=6)
            if not r.ok:
                logger.info(f"Proxies from {short_url(r.url)} were not loaded :(")
                return self.proxies_set
            raw_proxies = brotli.decompress(r.content)
            proxies = raw_proxies.decode("utf-8")
            proxies = json.loads(proxies)
            for proxy in proxies:
                if proxy.get("type") in (1, 2) and 210 < proxy.get("timeout") < 6000:
                    self.proxies_set.add(proxy.get("addr"))
            logger.info(f"From {short_url(r.url)} were parsed {len(self.proxies_set)} proxies")
        except Exception:
            logger.exception(
                f"Proxies from {short_url(r.url)} were not loaded :(\
                \n*This can happen if there is no proxies on site"
            )
        return self.proxies_set


def parse_proxyarchive() -> Set[str]:
    cpa = CheckerProxyArchive()
    sleep(3)
    cpa_set = cpa.parse_proxies()
    return cpa_set
