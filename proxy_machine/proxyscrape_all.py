import logging
from typing import Dict, Set, Union

import requests
from proxyscrape import create_collector, get_collector, scrapers
from proxyscrape.errors import CollectorAlreadyDefinedError
from user_agent import generate_user_agent

from .tools.proxies_manipulation import short_url

logger = logging.getLogger(__name__)


class ProxyScraper:
    def __init__(self) -> None:
        self.proxy_set: Set[str] = set()
        self.proxy_set2: Set[str] = set()
        self.lib_proxies = self.proxyscrape_lib()
        self.site_proxies = self.proxyscrape_site()

    def proxyscrape_lib(self) -> Set[str]:
        """Parsing proxies from proxyscrape py library"""
        free_proxies, ssl_proxies = set(), set()
        try:
            free_proxies = scrapers.get_free_proxy_list_proxies()
            ssl_proxies = scrapers.get_ssl_proxies()
        except Exception:
            logger.info("Proxies from proxyscrape library not loaded :(")
        try:
            collector = create_collector("default", "https")
        except CollectorAlreadyDefinedError:
            collector = get_collector("default")
        collector_proxies = set(collector.get_proxies())
        proxies = free_proxies | ssl_proxies | collector_proxies

        for proxy in proxies:
            prepare_proxy = f"{proxy.host}:{proxy.port}"
            if prepare_proxy not in self.proxy_set:
                self.proxy_set.add(prepare_proxy)
        logger.info(f"From proxyscrape_lib were parsed {len(self.proxy_set)} proxies")
        return self.proxy_set

    def proxyscrape_site(self) -> Set[str]:
        """Parsing proxies from proxyscrape"""
        url = "https://api.proxyscrape.com/"
        payload: Dict[str, Union[str, int]] = {
            "request": "getproxies",
            "proxytype": "https",
            "timeout": 10000,
            "country": "all",
            "ssl": "all",
            "anonymity": "all",
        }
        head: Dict[str, Union[str, object]] = {
            "Accept": "text/html,application/xhtml+xml,application/xml;\
            q=0.9,image/webp,*/*;q=0.8",
            "User-Agent": generate_user_agent(),
        }
        r = requests.get(url, params=payload, headers=head, timeout=6)
        try:
            if r.ok:
                data = r.text.encode()
                data_utf = data.decode("utf-8")
                self.proxy_set2 = set(data_utf.replace("\r", "").split("\n"))
            logger.info(f"From {short_url(r.url)} were parsed {len(self.proxy_set2)} proxies")
        except Exception:
            logger.exception(f"Proxies from {short_url(r.url)} were not loaded :(")
        return self.proxy_set2

    def combine_results(self) -> Set[str]:
        return self.lib_proxies.union(self.site_proxies)


def parse_proxyscrape() -> Set[str]:
    ps = ProxyScraper()
    ps_set = ps.combine_results()
    return ps_set
