import json
import logging
import re
import time
from datetime import datetime as dt
from typing import Set

import brotli
import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent

from utils import normalize_for_hidemy, parse_proxies, short_url

logger = logging.getLogger(__name__)
standard_headers = {"User-Agent": generate_user_agent()}


def proxy50_50() -> Set[str]:
    url = "https://proxy50-50.blogspot.com/"
    r = requests.get(url, headers=standard_headers)
    proxies_set = parse_proxies(r.text)
    logger.info(
        f"From {short_url(r.url)} were parsed {len(proxies_set)} proxies"
    )
    return proxies_set


def proxy_ip_list() -> Set[str]:
    url = "http://proxy-ip-list.com/"
    r = requests.get(url, headers=standard_headers)
    proxies_set2 = parse_proxies(r.text)
    logger.info(
        f"From {short_url(r.url)} were parsed {len(proxies_set2)} proxies"
    )
    return proxies_set2


def hidester() -> Set[str]:
    url = "https://hidester.com/proxydata/php/data.php"
    referer_url = "https://hidester.com/ru/public-proxy-ip-list/"
    user_agent = generate_user_agent()
    with requests.Session() as s:
        response = s.get(referer_url, headers=standard_headers)
    cookies_dict = response.cookies.get_dict()
    cookies = "".join([f"{k}={v}" for k, v in cookies_dict.items()])
    params = (
        ("mykey", "data"),
        ("offset", "0"),
        ("limit", "50"),
        ("orderBy", "latest_check"),
        ("sortOrder", "DESC"),
        ("country", ""),
        ("port", ""),
        ("type", "15"),
        ("anonymity", "7"),
        ("ping", "7"),
        ("gproxy", "2"),
    )
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "cookie": cookies,
        "referer": referer_url,
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": user_agent,
    }
    r = requests.get(url, params=params, headers=headers, timeout=20)
    proxies_set3 = set()
    if r.ok:
        try:
            decompress_uni = brotli.decompress(r.content)
            proxies = json.loads(decompress_uni.decode("utf-8"))
            for raw_proxy in proxies:
                if raw_proxy.get("type") in ("http", "https"):
                    proxy = f"{raw_proxy['IP']}:{raw_proxy['PORT']}"
                    proxies_set3.add(proxy)
            logger.info(
                f"From {short_url(r.url)} were parsed {len(proxies_set3)} proxies"
            )
        except Exception:
            logger.exception(
                f"Proxies from {short_url(r.url)} were not loaded :("
            )
    return proxies_set3


def awmproxy() -> Set[str]:
    url = "http://awmproxy.net"
    r = requests.get(url, headers=standard_headers)
    proxy_set4 = parse_proxies(r.text)
    logger.info(
        f"From {short_url(r.url)} were parsed {len(proxy_set4)} proxies"
    )
    return proxy_set4


def openproxy() -> Set[str]:
    date = dt.now().strftime("%d.%m.%Y %H:%M:%S")
    strp_date = dt.strptime(date, "%d.%m.%Y %H:%M:%S")
    stamp_date = int(time.mktime(strp_date.timetuple()) * 1000)
    proxy_set5 = set()
    links = set()

    url = f"https://api.openproxy.space/list?skip=0&ts={stamp_date}"
    r = requests.get(url, headers=standard_headers)
    data = r.json()
    for _dict in data:
        if len(_dict.get("protocols")) == 2:
            links.add(f"https://openproxy.space/list/{_dict.get('code')}")

    logger.info(f"Parsing proxies from {short_url(r.url)}...")
    for link in links:
        r = requests.get(link, headers=standard_headers)
        try:
            soup = BeautifulSoup(r.content, "lxml")
            proxies = parse_proxies(str(soup.find_all("script")[-6]))
            proxy_set5.update(proxies)
            logger.info(
                f"From {r.url.split('/')[-1]} section were parsed {len(proxies)} proxies"
            )
        except Exception:
            logger.exception(
                f"Proxies from {link.split('/')[-1]} were not loaded :("
            )
        time.sleep(1.3)  # crawling-delay
    logger.info(
        f"From {short_url(r.url)} were parsed {len(proxy_set5)} proxies"
    )
    return proxy_set5


def proxy_list_download() -> Set[str]:
    url = "https://www.proxy-list.download/api/v0/get?l=en&t=http"
    proxy_set6 = set()
    try:
        r = requests.get(url, headers=standard_headers)
        proxies_list = r.json()[0].get("LISTA")
        for proxy in proxies_list:
            proxy_set6.add(f"{proxy.get('IP')}:{proxy.get('PORT')}")
        logger.info(
            f"From {short_url(r.url)} were parsed {len(proxy_set6)} proxies"
        )
    except Exception:
        logger.exception(f"Proxies from {short_url(r.url)} were not loaded :(")
    return proxy_set6


def aliveproxy() -> Set[str]:
    urls = [
        "http://aliveproxy.com/fastest-proxies",
        "http://aliveproxy.com/high-anonymity-proxy-list",
        "http://aliveproxy.com/anonymous-proxy-list",
        "http://aliveproxy.com/transparent-proxy-list",
        "http://aliveproxy.com/us-proxy-list",
        "http://aliveproxy.com/gb-proxy-list",
        "http://aliveproxy.com/de-proxy-list",
        "http://aliveproxy.com/jp-proxy-list",
        "http://aliveproxy.com/ca-proxy-list",
    ]
    proxy_set7 = set()
    logger.info(
        f"Parsing proxies from {short_url(urls[0])}..."
    )  # aliveproxy.com
    for url in urls:
        r = requests.get(url, headers=standard_headers)
        soup = BeautifulSoup(r.content, "lxml")
        plp_s7 = len(proxy_set7)  # previous len proxy_set7
        for proxy in soup.find("table", {"class": "cm or"}).find_all("tr")[1:]:
            proxies = parse_proxies(str(proxy.find("td")))
            proxy_set7.update(proxies)
        link = r.url.split("/")[-2]
        logger.info(
            f"From {link} section were parsed {len(proxy_set7) - plp_s7} proxies"
        )
        time.sleep(1.3)  # crawling-delay
    logger.info(
        f"From {short_url(urls[0])} were parsed {len(proxy_set7)} proxies"
    )
    return proxy_set7


def community_aliveproxy() -> Set[str]:
    url = "http://community.aliveproxy.com/proxy_list_http_fastest"
    proxy_set8 = set()
    r = requests.get(url, headers=standard_headers)
    soup = BeautifulSoup(r.content, "lxml")
    try:
        for proxy in soup.find("table").find_all("tr")[1:]:
            proxies = parse_proxies(proxy.text)
            proxy_set8.update(proxies)
        logger.info(
            f"From {short_url(r.url)} were parsed {len(proxy_set8)} proxies"
        )
    except Exception:
        logger.exception(f"Proxies from {short_url(r.url)} were not loaded :(")
    return proxy_set8


def hidemy() -> Set[str]:
    url = "http://hidemy.name/en/proxy-list/"
    countries = """AFALARAMAUATAZBHBDBYBEBZBJBOBABWBRBGBIKHCM\
CACLCNCOCDCRHRCYCZDKECEGGQFIFRGEDEGRGTHNHKHUINIDIRIQIEILI\
TJPKZKEKRKGLVLSLYLTMKMGMWMYMVMLMTMXMDMNMEMZNPNLNZNGNOPKPS\
PAPYPEPHPLPTPRRORURWRSSCSGSKSISOZAESSDSESYTWTJTZTHTNTRUGU\
AAEGBUSUYUZVEVNVGZW"""
    proxies_set9 = set()

    # 1-st start = 0. new page start=start+64.
    for n in range(0, 15 * 64, 64):
        params = {
            "country": countries,
            "maxtime": 3000,
            "type": "hs",
            "out": "plain",
            "lang": "en",
            "utf": "",
            "start": n,
        }
        r = requests.get(url, params=params, headers=standard_headers)
        soup = BeautifulSoup(r.content, "lxml")

        try:
            for tr in soup.find("table").find_all("tr")[1:]:
                tds = tr.find_all("td")
                proxies_set9.add(f"{tds[0].text}:{tds[1].text}")
            logger.info(
                f"From {short_url(r.url)} were parsed {len(proxies_set9)} proxies"
            )
        except Exception:
            logger.exception(
                f"Proxies from {short_url(r.url)} were not loaded :("
            )
    return proxies_set9


def proxy11() -> Set[str]:
    url = "https://proxy11.com/api/demoweb/proxy.json"
    proxies_set10 = set()
    r = requests.get(url, headers=standard_headers)
    try:
        data_list = r.json().get("data")
        for data in data_list:
            proxy = f"{data.get('ip')}:{data.get('port')}"
            proxies_set10.add(proxy)
        logger.info(
            f"From {short_url(r.url)} were parsed {len(proxies_set10)} proxies"
        )
    except Exception:
        logger.exception(f"Proxies from {short_url(r.url)} were not loaded :(")
    return proxies_set10


def httptunnel() -> Set[str]:
    url = "http://www.httptunnel.ge/ProxyListForFree.aspx"
    r = requests.get(url, headers=standard_headers)
    proxies_set11 = parse_proxies(r.text)
    logger.info(
        f"From {short_url(r.url)} were parsed {len(proxies_set11)} proxies"
    )
    return proxies_set11
