import argparse
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from inspect import getmembers, isfunction
from time import time
from typing import Any, List, Set

import proxy_machine.otherproxies as otherproxies

from .proxyarchive import parse_proxyarchive
from .proxyscrape_all import parse_proxyscrape
from .tools.proxies_manipulation import filtrate_ports, prepare_proxy
from .tools.proxy_checker import check_proxy, run_checking


def load_proxies_func() -> List[Any]:
    # Functions that don't parsing proxies
    other_func = ("generate_user_agent", "parse_proxies", "short_url")
    functions = [
        func
        for name, func in getmembers(otherproxies, isfunction)
        if name not in other_func
    ]  # Filtering result based on tuple: other_func
    # Adding parsers in other modules
    functions.append(parse_proxyarchive)
    functions.append(parse_proxyscrape)
    return functions


def save_proxies(filename: str, proxies: Set[str]) -> None:
    with open(filename, "w+") as f:
        f.writelines(proxies)
        logger.info(f"{len(proxies)} proxies were recorded in {filename}")


def main(workers=None, checker=False) -> None:
    start = time()
    proxies = set()
    parsers = load_proxies_func()

    with ThreadPoolExecutor(workers) as executor:
        futures = []
        for parser in parsers:
            futures.append(executor.submit(parser))
        for future in as_completed(futures):
            parser_proxies = future.result()
            proxies.update(parser_proxies)

    # Clearing unnecessary lines. (These can be from proxyscrape_all)
    prepared_proxies = {
        f"{prepare_proxy(proxy)}\n"
        for proxy in proxies
        if filtrate_ports(proxy)
    }

    if checker:
        logger.info("----- Launch the proxies checker... -----")
        checked_proxies = run_checking(prepared_proxies, workers)
        prepared_proxies = {f"{proxy}\n" for proxy in checked_proxies}

    save_proxies("proxies.txt", prepared_proxies)
    logger.info(f"Program execution time: {time() - start:.2f} sec")


if __name__ == "__main__":
    logging.basicConfig(
        format="{asctime} <{levelname}> {name}: {message}",
        datefmt="%Y-%m-%d %H:%M:%S",
        style="{",
        level=logging.INFO,
    )
    logger = logging.getLogger("proxy_machine")
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "-pc",
        "--proxy-checker",
        default=False,
        action="store_true",
        help="If you want to keep only working proxies use this. "
        "Default set False.",
    )
    argparser.add_argument(
        "-w",
        "--workers",
        default=None,
        type=int,
        help="The number of workers that is transferred to "
        "ThreadPoolExecutor. Default set None. Because "
        "python himself determines the required number of workers.",
    )

    args = argparser.parse_args()
    main(workers=args.workers, checker=args.proxy_checker)
