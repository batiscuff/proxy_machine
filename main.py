import logging
import time
from typing import Set

from checkerproxy_net import CheckerProxyArchive
from otherproxies import (aliveproxy, awmproxy, community_aliveproxy, hidester,
                          openproxy, proxy50_50, proxy_ip_list,
                          proxy_list_download)
from proxyscrape_all import ProxyScraper
from utils import prepare_proxy


def load_proxies() -> Set[str]:
    main_set: Set[str] = set()
    cpa = CheckerProxyArchive()
    ps = ProxyScraper()
    cpa_set, ps_set = cpa.parse_proxies(), ps.combine_results()
    p50_set, pil_set, h_set = proxy50_50(), proxy_ip_list(), hidester()
    al_set, aw_set, op_set = aliveproxy(), awmproxy(), openproxy()
    cal_set, pld_set = community_aliveproxy(), proxy_list_download()
    return main_set.union(
        cpa_set,
        ps_set,
        p50_set,
        pil_set,
        op_set,
        h_set,
        al_set,
        aw_set,
        cal_set,
        pld_set,
    )


def save_proxies(filename: str, proxies: Set[str]) -> None:
    with open(filename, "w+") as f:
        f.writelines(proxies)
        logger.info(f"{len(proxies)} proxies were recorded in {filename}")


def main() -> None:
    start = time.time()
    proxies_set = load_proxies()
    # Clearing unnecessary lines. (These can be from proxyscrape_all)
    prepared_proxies = {
        f"{prepare_proxy(proxy)}\n" for proxy in proxies_set if len(proxy) > 0
    }
    save_proxies("proxies.txt", prepared_proxies)
    logger.info(f"Program execution time: {time.time() - start: .2f} sec")


if __name__ == "__main__":
    logging.basicConfig(
        format="{asctime} <{levelname}> {name}: {message}",
        datefmt="%Y-%m-%d %H:%M:%S",
        style="{",
        level=logging.INFO
    )
    logger = logging.getLogger("proxy_machine")

    main()
