import json
import logging
import re
import time
from datetime import datetime as dt
from typing import Set

import requests

import brotli
from bs4 import BeautifulSoup
from user_agent import generate_user_agent

from .tools.proxies_manipulation import parse_proxies, short_url

logger = logging.getLogger(__name__)
standard_headers = {"User-Agent": generate_user_agent()}
timeout = 6


def proxy50_50() -> Set[str]:
    url = "https://proxy50-50.blogspot.com/"
    proxies_set = set()
    try:
        r = requests.get(url, headers=standard_headers, timeout=timeout)
        proxies_set.update(parse_proxies(r.text))
        logger.info(
            f"From {short_url(r.url)} were parsed {len(proxies_set)} proxies"
        )
    except Exception:
        logger.exception(f"Proxies from {short_url(url)} were not loaded :(")
    return proxies_set


def proxy_searcher() -> Set[str]:
    url = "http://proxysearcher.sourceforge.net/Proxy%20List.php?type=http"
    proxies_set2 = set()
    try:
        r = requests.get(url, headers=standard_headers, timeout=timeout)
        proxies_set2.update(parse_proxies(r.text))
        logger.info(
            f"From {short_url(r.url)} were parsed {len(proxies_set2)} proxies"
        )
    except Exception:
        logger.exception(f"Proxies from {short_url(url)} were not loaded :(")
    return proxies_set2


def hidester() -> Set[str]:
    url = "https://hidester.com/proxydata/php/data.php"
    referer_url = "https://hidester.com/ru/public-proxy-ip-list/"
    user_agent = generate_user_agent()
    with requests.Session() as s:
        response = s.get(referer_url, headers=standard_headers, timeout=timeout)
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
    proxies_set3 = set()
    try:
        r = requests.get(url, params=params, headers=headers, timeout=10)
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
        logger.exception(f"Proxies from {short_url(url)} were not loaded :(")
    return proxies_set3


def awmproxy() -> Set[str]:
    url = "http://awmproxy.net"
    proxy_set4 = set()
    try:
        r = requests.get(url, headers=standard_headers, timeout=timeout)
        proxy_set4.update(parse_proxies(r.text))
        logger.info(
            f"From {short_url(r.url)} were parsed {len(proxy_set4)} proxies"
        )
    except Exception:
        logger.exception(f"Proxies from {short_url(url)} were not loaded :(")
    return proxy_set4


def openproxy() -> Set[str]:
    date = dt.now().strftime("%d.%m.%Y %H:%M:%S")
    strp_date = dt.strptime(date, "%d.%m.%Y %H:%M:%S")
    stamp_date = int(time.mktime(strp_date.timetuple()) * 1000)
    proxy_set5 = set()
    links = set()

    url = f"https://api.openproxy.space/list?skip=0&ts={stamp_date}"
    try:
        r = requests.get(url, headers=standard_headers, timeout=timeout)
        data = r.json()
        for _dict in data:
            if len(_dict.get("protocols")) == 2:
                links.add(f"https://api.openproxy.space/list/{_dict.get('code')}")
    except Exception:
        logger.exception(f"Proxies from {short_url(url)} were not loaded :(")

    logger.info(f"Parsing proxies from {short_url(r.url)}...")
    for link in links:
        try:
            r = requests.get(link, headers=standard_headers, timeout=timeout)
            proxies = parse_proxies(str(r.json().get("data")))
            proxy_set5.update(proxies)
            logger.info(
                f"From {r.url.split('/')[-1]} section were parsed {len(proxies)} proxies"
            )
        except Exception:
            logger.exception(
                f"Proxies from {link.split('/')[-1]} were not loaded :("
            )
        time.sleep(1.3)  # crawling-delay
    logger.info(f"From {short_url(url)} were parsed {len(proxy_set5)} proxies")
    return proxy_set5


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
    proxy_set7 = set()  # type: ignore
    logger.info(
        f"Parsing proxies from {short_url(urls[0])}..."
    )  # aliveproxy.com
    for url in urls:
        try:
            r = requests.get(url, headers=standard_headers, timeout=timeout)
            soup = BeautifulSoup(r.content, "lxml")
            plp_s7 = len(proxy_set7)  # previous len proxy_set7
            for proxy in soup.find("table", {"class": "cm or"}).find_all("tr")[
                1:
            ]:
                proxies = parse_proxies(str(proxy.find("td")))
                proxy_set7.update(proxies)
            link = r.url.split("/")[-2]
            logger.info(
                f"From {link} section were parsed {len(proxy_set7) - plp_s7} proxies"
            )
            time.sleep(1.3)  # crawling-delay
        except Exception:
            logger.exception(
                f"Proxies from {short_url(url)} were not loaded :("
            )
    logger.info(
        f"From {short_url(urls[0])} were parsed {len(proxy_set7)} proxies"
    )
    return proxy_set7


def community_aliveproxy() -> Set[str]:
    url = "http://community.aliveproxy.com/proxy_list_http_fastest"
    proxy_set8 = set()
    try:
        r = requests.get(url, headers=standard_headers, timeout=timeout)
        soup = BeautifulSoup(r.content, "lxml")
        for proxy in soup.find("table").find_all("tr")[1:]:
            proxies = parse_proxies(proxy.text)
            proxy_set8.update(proxies)
        logger.info(
            f"From {short_url(r.url)} were parsed {len(proxy_set8)} proxies"
        )
    except Exception:
        logger.exception(f"Proxies from {short_url(url)} were not loaded :(")
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
        params = (
            ("country", countries),
            ("maxtime", 3000),
            ("type", "hs"),
            ("out", "plain"),
            ("lang", "en"),
            ("utf", ""),
            ("start", n),
        )
        try:
            r = requests.get(url, params=params, headers=standard_headers, timeout=timeout)
            soup = BeautifulSoup(r.content, "lxml")
            for tr in soup.find("table").find_all("tr")[1:]:
                tds = tr.find_all("td")
                proxies_set9.add(f"{tds[0].text}:{tds[1].text}")
        except Exception:
            logger.exception(
                f"Proxies from {short_url(url)} were not loaded :("
            )
    logger.info(
        f"From {short_url(r.url)} were parsed {len(proxies_set9)} proxies"
    )
    return proxies_set9


def proxy11() -> Set[str]:
    url = "https://proxy11.com/api/demoweb/proxy.json"
    proxies_set10 = set()
    try:
        r = requests.get(url, headers=standard_headers, timeout=timeout)
        data_list = r.json().get("data")
        for data in data_list:
            proxy = f"{data.get('ip')}:{data.get('port')}"
            proxies_set10.add(proxy)
        logger.info(
            f"From {short_url(r.url)} were parsed {len(proxies_set10)} proxies"
        )
    except Exception:
        logger.exception(f"Proxies from {short_url(url)} were not loaded :(")
    return proxies_set10


def httptunnel() -> Set[str]:
    url = "http://www.httptunnel.ge/ProxyListForFree.aspx"
    proxies_set11 = set()
    try:
        r = requests.get(url, headers=standard_headers, timeout=timeout)
        proxies_set11.update(parse_proxies(r.text))
        logger.info(
            f"From {short_url(r.url)} were parsed {len(proxies_set11)} proxies"
        )
    except Exception:
        logger.exception(f"Proxies from {short_url(url)} were not loaded :(")
    return proxies_set11


def spys_me() -> Set[str]:
    url = "https://spys.me/proxy.txt"
    proxies_set12 = set()
    try:
        r = requests.get(url, headers=standard_headers, timeout=timeout)
        proxies_set12.update(parse_proxies(r.text))
        logger.info(
            f"From {short_url(r.url)} were parsed {len(proxies_set12)} proxies"
        )
    except Exception:
        logger.exception(f"Proxies from {short_url(url)} were not loaded :(")
    return proxies_set12


def fatezero() -> Set[str]:
    url = "http://static.fatezero.org/tmp/proxy.txt"
    proxies_set13 = set()
    try:
        r = requests.get(url, headers=standard_headers, timeout=timeout)
        proxies_set13.update(parse_proxies(r.text))
        logger.info(
            f"From {short_url(r.url)} were parsed {len(proxies_set13)} proxies"
        )
    except Exception:
        logger.exception(f"Proxies from {short_url(url)} were not loaded :(")
    return proxies_set13


def pubproxy() -> Set[str]:
    url = "http://pubproxy.com/api/proxy"
    params = {"limit": "200", "format": "txt", "type": "http"}
    proxies_set14 = set()
    try:
        r = requests.get(url, params=params, headers=standard_headers, timeout=timeout)
        proxies_set14.update(parse_proxies(r.text))
        logger.info(
            f"From {short_url(r.url)} were parsed {len(proxies_set14)} proxies"
        )
    except Exception:
        logger.exception(f"Proxies from {short_url(url)} were not loaded :(")
    return proxies_set14


def proxylists() -> Set[str]:
    url = "http://www.proxylists.net/http_highanon.txt"
    proxies_set15 = set()
    try:
        r = requests.get(url, headers=standard_headers, timeout=timeout)
        proxies_set15.update(parse_proxies(r.text))
        logger.info(
            f"From {short_url(r.url)} were parsed {len(proxies_set15)} proxies"
        )
    except Exception:
        logger.exception(f"Proxies from {short_url(url)} were not loaded :(")
    return proxies_set15


def ab57ru() -> Set[str]:
    url = "http://ab57.ru/downloads/proxylist.txt"
    proxies_set16 = set()
    try:
        r = requests.get(url, headers=standard_headers, timeout=timeout)
        proxies_set16.update(parse_proxies(r.text))
        logger.info(
            f"From {short_url(r.url)} were parsed {len(proxies_set16)} proxies"
        )
    except Exception:
        logger.exception(f"Proxies from {short_url(url)} were not loaded :(")
    return proxies_set16


def shifty() -> Set[str]:
    url = (
        "http://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt"
    )
    proxies_set17 = set()
    try:
        r = requests.get(url, headers=standard_headers, timeout=timeout)
        proxies_set17.update(parse_proxies(r.text))
        logger.info(
            f"From {short_url(r.url)} were parsed {len(proxies_set17)} proxies"
        )
    except Exception:
        logger.exception(f"Proxies from {short_url(url)} were not loaded :(")
    return proxies_set17


def shifty2() -> Set[str]:
    url = (
        "http://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt"
    )
    proxies_set18 = set()
    try:
        r = requests.get(url, headers=standard_headers, timeout=timeout)
        proxies_set18.update(parse_proxies(r.text))
        logger.info(
            f"From {short_url(r.url)} were parsed {len(proxies_set18)} proxies"
        )
    except Exception:
        logger.exception(f"Proxies from {short_url(url)} were not loaded :(")
    return proxies_set18


def sunny9577() -> Set[str]:
    url = "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt"
    proxies_set19 = set()
    try:
        r = requests.get(url, headers=standard_headers, timeout=timeout)
        proxies_set19.update(parse_proxies(r.text))
        logger.info(
            f"From {short_url(r.url)} were parsed {len(proxies_set19)} proxies"
        )
    except Exception:
        logger.exception(f"Proxies from {short_url(url)} were not loaded :(")
    return proxies_set19


def multiproxy() -> Set[str]:
    url = "http://multiproxy.org/txt_all/proxy.txt"
    proxies_set21 = set()
    try:
        r = requests.get(url, headers=standard_headers, timeout=timeout)
        proxies_set21.update(parse_proxies(r.text))
        logger.info(
            f"From {short_url(r.url)} were parsed {len(proxies_set21)} proxies"
        )
    except Exception:
        logger.exception(f"Proxies from {short_url(url)} were not loaded :(")
    return proxies_set21


def root_jazz() -> Set[str]:
    url = "http://rootjazz.com/proxies/proxies.txt"
    proxies_set22 = set()
    try:
        r = requests.get(url, headers=standard_headers, timeout=timeout)
        proxies_set22.update(parse_proxies(r.text))
        logger.info(
            f"From {short_url(r.url)} were parsed {len(proxies_set22)} proxies"
        )
    except Exception:
        logger.exception(f"Proxies from {short_url(url)} were not loaded :(")
    return proxies_set22


def proxyscan() -> Set[str]:
    url = "http://www.proxyscan.io/api/proxy"
    proxies_set23 = set()
    params = (
        ("ping", "500"),
        ("limit", "100"),
        ("type", "http,https"),
        ("format", "txt")
    )
    for _ in range(8):
        try:
            r = requests.get(url, params=params, headers=standard_headers, timeout=timeout)
            proxies = parse_proxies(r.text)
            proxies_set23.update(proxies)
        except Exception:
            logger.exception(f"Proxies from {short_url(url)} were not loaded :(")
    logger.info(
        f"From {short_url(url)} were parsed {len(proxies_set23)} proxies"
    )
    return proxies_set23


def proxy_list_download() -> Set[str]:
    url = "https://www.proxy-list.download/api/v0/get?l=en&t=http"
    pl_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,\
                   image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "ru,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Alt-Used": "www.proxy-list.download",
        "Cache-Control": "max-age=0",
        "User-Agent": generate_user_agent()
    }
    proxy_set24 = set()
    try:
        r = requests.get(url, headers=pl_headers, timeout=timeout)

        bytebrotl = brotli.decompress(r.content)
        strbrotl = bytebrotl.decode("utf-8")
        data = json.loads(strbrotl)

        proxies_list = data[0].get("LISTA")
        for proxy in proxies_list:
            proxy_set24.add(f"{proxy.get('IP')}:{proxy.get('PORT')}")
        logger.info(
            f"From {short_url(r.url)} were parsed {len(proxy_set24)} proxies"
        )
    except Exception:
        logger.exception(f"Proxies from {short_url(url)} were not loaded :(")
    return proxy_set24
