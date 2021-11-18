import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Set, Union

import httpx
import requests
from user_agent import generate_user_agent

logger = logging.getLogger(__name__)
url = "http://api.myip.com/"
headers = {"User-Agent": generate_user_agent()}
client = httpx.AsyncClient(timeout=6)


def check_proxy(proxy: str) -> Union[str, None]:
    proxy = proxy.replace("\n", "")
    proxies = {"http": proxy, "https": proxy}
    proxy = proxy.replace("http://", "").split(":")  # type: ignore
    ip = proxy[0]
    try:
        result = requests.get(url, headers=headers, proxies=proxies, timeout=6)
        data = result.json()
        if data.get("ip") == ip:
            logger.info(f"Good proxy: {proxy[0]}:{proxy[1]} !!!")
            return proxies.get("http")
    except Exception:
        logger.info(f"Dead proxy: {proxy[0]}:{proxy[1]}")
    return None


async def check_proxy_async(proxy: str) -> Union[str, None]:
    proxy = proxy.replace("\n", "")
    proxies = {"http://": proxy, "https://": proxy}
    proxy = proxy.replace("http://", "").split(":")  # type: ignore
    ip = proxy[0]
    try:
        client.proxies = proxies
        start_time = time.perf_counter()
        async with httpx.AsyncClient(proxies=proxies) as client_2:
            result = await client_2.get(url, headers=headers)
        # result = await client.get(url, headers=headers)
        total_time = time.perf_counter() - start_time
        data = result.json()
        if data.get("ip") == ip:
            logger.info(f"Good proxy: {proxy[0]}:{proxy[1]} !!! - {total_time=}")
            return proxies.get("http")
        else:
            raise ConnectionError()
    except Exception as e:
        logger.warning(f"Error {e}")
        logger.info(f"Dead proxy: {proxy[0]}:{proxy[1]} - current_id:")
    return None


def run_checking(proxies_set: Set[str], workers=None) -> Set[str]:
    checked_proxies = set()
    with ThreadPoolExecutor(workers) as executor:
        futures = []
        for proxy in proxies_set:
            futures.append(executor.submit(check_proxy, proxy))
        for future in as_completed(futures):
            c_proxy = future.result()
            if c_proxy is not None:
                checked_proxies.add(c_proxy)
    return checked_proxies


async def run_checking_async(proxies_set: Set[str], workers=None) -> Set[str]:
    checked_proxies = set()
    for proxy in proxies_set:
        c_proxy = await check_proxy_async(proxy)
        if c_proxy:
            checked_proxies.add(c_proxy)
    return checked_proxies
