import json
import logging
import time
from datetime import datetime as dt
from typing import Set

import brotli
import requests
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
        logger.info(f"From {short_url(r.url)} were parsed {len(proxies_set)} proxies")
    except Exception:
        logger.exception(f"Proxies from {short_url(url)} were not loaded :(")
    return proxies_set


def proxy_searcher() -> Set[str]:
    url = "http://proxysearcher.sourceforge.net/Proxy%20List.php?type=http"
    proxies_set2 = set()
    try:
        r = requests.get(url, headers=standard_headers, timeout=timeout)
        proxies_set2.update(parse_proxies(r.text))
        logger.info(f"From {short_url(r.url)} were parsed {len(proxies_set2)} proxies")
    except Exception:
        logger.exception(f"Proxies from {short_url(url)} were not loaded :(")
    return proxies_set2


def hidester() -> Set[str]:
    url = "https://hidester.com/proxydata/php/data.php"
    referer_url = "https://hidester.com/ru/public-proxy-ip-list/"
    user_agent = generate_user_agent()
    proxies_set3 = set()
    try:
        with requests.Session() as s:
            response = s.get(referer_url, headers=standard_headers, timeout=timeout)
    except Exception:
        logger.exception("Proxylink from {url} where not loaded :(")
        return proxies_set3
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
    try:
        r = requests.get(url, params=params, headers=headers, timeout=10)
        decompress_uni = brotli.decompress(r.content)
        proxies = json.loads(decompress_uni.decode("utf-8"))
        for raw_proxy in proxies:
            if raw_proxy.get("type") in ("http", "https"):
                proxy = f"{raw_proxy['IP']}:{raw_proxy['PORT']}"
                proxies_set3.add(proxy)
        logger.info(f"From {short_url(r.url)} were parsed {len(proxies_set3)} proxies")
    except Exception:
        logger.exception(f"Proxies from {short_url(url)} were not loaded :(")
    return proxies_set3


def awmproxy() -> Set[str]:
    url = "http://awmproxy.net"
    proxy_set4 = set()
    try:
        r = requests.get(url, headers=standard_headers, timeout=timeout)
        proxy_set4.update(parse_proxies(r.text))
        logger.info(f"From {short_url(r.url)} were parsed {len(proxy_set4)} proxies")
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

    logger.info(f"Parsing proxies from {short_url(url)}...")
    for link in links:
        try:
            r = requests.get(link, headers=standard_headers, timeout=timeout)
            proxies = parse_proxies(str(r.json().get("data")))
            proxy_set5.update(proxies)
            logger.info(f"From {r.url.split('/')[-1]} section were parsed {len(proxies)} proxies")
        except Exception:
            logger.exception(f"Proxies from {link.split('/')[-1]} were not loaded :(")
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
    logger.info(f"Parsing proxies from {short_url(urls[0])}...")  # aliveproxy.com
    for url in urls:
        try:
            r = requests.get(url, headers=standard_headers, timeout=timeout)
            soup = BeautifulSoup(r.content, "lxml")
            plp_s7 = len(proxy_set7)  # previous len proxy_set7
            for proxy in soup.find("table", {"class": "cm or"}).find_all("tr")[1:]:
                proxies = parse_proxies(str(proxy.find("td")))
                proxy_set7.update(proxies)
            link = r.url.split("/")[-2]
            logger.info(f"From {link} section were parsed {len(proxy_set7) - plp_s7} proxies")
            time.sleep(1.3)  # crawling-delay
        except Exception:
            logger.exception(f"Proxies from {short_url(url)} were not loaded :(")
    logger.info(f"From {short_url(urls[0])} were parsed {len(proxy_set7)} proxies")
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
        logger.info(f"From {short_url(r.url)} were parsed {len(proxy_set8)} proxies")
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
            logger.exception(f"Proxies from {short_url(url)} were not loaded :(")
    logger.info(f"From {short_url(r.url)} were parsed {len(proxies_set9)} proxies")
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
        logger.info(f"From {short_url(r.url)} were parsed {len(proxies_set10)} proxies")
    except Exception:
        logger.exception(f"Proxies from {short_url(url)} were not loaded :(")
    return proxies_set10


def httptunnel() -> Set[str]:
    url = "http://www.httptunnel.ge/ProxyListForFree.aspx"
    proxies_set11 = set()
    try:
        r = requests.get(url, headers=standard_headers, timeout=timeout)
        proxies_set11.update(parse_proxies(r.text))
        logger.info(f"From {short_url(r.url)} were parsed {len(proxies_set11)} proxies")
    except Exception:
        logger.exception(f"Proxies from {short_url(url)} were not loaded :(")
    return proxies_set11


def spys_me() -> Set[str]:
    url = "https://spys.me/proxy.txt"
    proxies_set12 = set()
    try:
        r = requests.get(url, headers=standard_headers, timeout=timeout)
        proxies_set12.update(parse_proxies(r.text))
        logger.info(f"From {short_url(r.url)} were parsed {len(proxies_set12)} proxies")
    except Exception:
        logger.exception(f"Proxies from {short_url(url)} were not loaded :(")
    return proxies_set12


def fatezero() -> Set[str]:
    url = "http://static.fatezero.org/tmp/proxy.txt"
    proxies_set13 = set()
    try:
        r = requests.get(url, headers=standard_headers, timeout=timeout)
        proxies_set13.update(parse_proxies(r.text))
        logger.info(f"From {short_url(r.url)} were parsed {len(proxies_set13)} proxies")
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
        logger.info(f"From {short_url(r.url)} were parsed {len(proxies_set14)} proxies")
    except Exception:
        logger.exception(f"Proxies from {short_url(url)} were not loaded :(")
    return proxies_set14


def proxylists() -> Set[str]:
    url = "http://www.proxylists.net/http_highanon.txt"
    proxies_set15 = set()
    try:
        r = requests.get(url, headers=standard_headers, timeout=timeout)
        proxies_set15.update(parse_proxies(r.text))
        logger.info(f"From {short_url(r.url)} were parsed {len(proxies_set15)} proxies")
    except Exception:
        logger.exception(f"Proxies from {short_url(url)} were not loaded :(")
    return proxies_set15


def ab57ru() -> Set[str]:
    url = "http://ab57.ru/downloads/proxylist.txt"
    proxies_set16 = set()
    try:
        r = requests.get(url, headers=standard_headers, timeout=timeout)
        proxies_set16.update(parse_proxies(r.text))
        logger.info(f"From {short_url(r.url)} were parsed {len(proxies_set16)} proxies")
    except Exception:
        logger.exception(f"Proxies from {short_url(url)} were not loaded :(")
    return proxies_set16


def shifty() -> Set[str]:
    url = "http://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt"
    proxies_set17 = set()
    try:
        r = requests.get(url, headers=standard_headers, timeout=timeout)
        proxies_set17.update(parse_proxies(r.text))
        logger.info(f"From {short_url(r.url)} were parsed {len(proxies_set17)} proxies")
    except Exception:
        logger.exception(f"Proxies from {short_url(url)} were not loaded :(")
    return proxies_set17


def shifty2() -> Set[str]:
    url = "http://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt"
    proxies_set18 = set()
    try:
        r = requests.get(url, headers=standard_headers, timeout=timeout)
        proxies_set18.update(parse_proxies(r.text))
        logger.info(f"From {short_url(r.url)} were parsed {len(proxies_set18)} proxies")
    except Exception:
        logger.exception(f"Proxies from {short_url(url)} were not loaded :(")
    return proxies_set18


def sunny9577() -> Set[str]:
    url = "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt"
    proxies_set19 = set()
    try:
        r = requests.get(url, headers=standard_headers, timeout=timeout)
        proxies_set19.update(parse_proxies(r.text))
        logger.info(f"From {short_url(r.url)} were parsed {len(proxies_set19)} proxies")
    except Exception:
        logger.exception(f"Proxies from {short_url(url)} were not loaded :(")
    return proxies_set19


def multiproxy() -> Set[str]:
    url = "http://multiproxy.org/txt_all/proxy.txt"
    proxies_set21 = set()
    try:
        r = requests.get(url, headers=standard_headers, timeout=timeout)
        proxies_set21.update(parse_proxies(r.text))
        logger.info(f"From {short_url(r.url)} were parsed {len(proxies_set21)} proxies")
    except Exception:
        logger.exception(f"Proxies from {short_url(url)} were not loaded :(")
    return proxies_set21


def root_jazz() -> Set[str]:
    url = "http://rootjazz.com/proxies/proxies.txt"
    proxies_set22 = set()
    try:
        r = requests.get(url, headers=standard_headers, timeout=timeout)
        proxies_set22.update(parse_proxies(r.text))
        logger.info(f"From {short_url(r.url)} were parsed {len(proxies_set22)} proxies")
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
        ("format", "txt"),
    )
    for _ in range(8):
        try:
            r = requests.get(url, params=params, headers=standard_headers, timeout=timeout)
            proxies = parse_proxies(r.text)
            proxies_set23.update(proxies)
        except Exception:
            logger.exception(f"Proxies from {short_url(url)} were not loaded :(")
    logger.info(f"From {short_url(url)} were parsed {len(proxies_set23)} proxies")
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
        "User-Agent": generate_user_agent(),
    }
    proxies_set24 = set()
    try:
        r = requests.get(url, headers=pl_headers, timeout=timeout)

        bytebrotl = brotli.decompress(r.content)
        strbrotl = bytebrotl.decode("utf-8")
        data = json.loads(strbrotl)

        proxies_list = data[0].get("LISTA")
        for proxy in proxies_list:
            proxies_set24.add(f"{proxy.get('IP')}:{proxy.get('PORT')}")
        logger.info(f"From {short_url(r.url)} were parsed {len(proxies_set24)} proxies")
    except Exception:
        logger.exception(f"Proxies from {short_url(url)} were not loaded :(")
    return proxies_set24


def proxylistplus() -> Set[str]:
    url = "https://list.proxylistplus.com/SSL-List-1"
    proxies_set25 = set()
    try:
        r = requests.get(url, headers=standard_headers, timeout=timeout)
        soup = BeautifulSoup(r.content, "lxml")
        max_page_num = soup.find("select", {"onchange": "window.location=this.value"}).find_all("option")[-1].text
        for page_num in range(1, int(max_page_num) + 1):
            url = f"https://list.proxylistplus.com/SSL-List-{page_num}"
            r = requests.get(url, headers=standard_headers, timeout=timeout)
            soup = BeautifulSoup(r.content, "lxml")
            table = soup.find("table", {"class": "bg"})
            for tr in table.find_all("tr")[2:]:
                tds = tr.find_all("td")
                ip, port = tds[1].text.strip(), tds[2].text.strip()
                proxies_set25.add(f"{ip}:{port}")
        logger.info(f"From {short_url(r.url)} were parsed {len(proxies_set25)} proxies")
    except Exception:
        logger.exception(f"Proxies from {short_url(url)} were not loaded :(")
    return proxies_set25


def proxyhub() -> Set[str]:
    url = "https://www.proxyhub.me/ru/all-https-proxy-list.html"
    proxies_set26 = set()
    for page in range(1, 11):
        try:
            cookies = {"anonymity": "all", "page": f"{page}"}
            r = requests.get(url, headers=standard_headers, cookies=cookies, timeout=timeout)
            soup = BeautifulSoup(r.content, "lxml")
            table = soup.find("table", {"class": "table-bordered"}).find("tbody")
            for tr in table.find_all("tr"):
                tds = tr.find_all("td")
                proxies_set26.add(f"{tds[0].text}:{tds[1].text}")
        except Exception:
            logger.exception(f"Proxies from {short_url(url)} page: {page} were not loaded :(")
    logger.info(f"From {short_url(url)} were parsed {len(proxies_set26)} proxies")
    return proxies_set26


def proxylist4all() -> Set[str]:
    url = "https://www.proxylist4all.com/wp-admin/admin-ajax.php"
    proxies_set27 = set()
    data = {"action": "getProxyList", "request": ""}
    cookies = {"www.proxylist4all.com": "{}"}
    try:
        r = requests.post(url, data=data, cookies=cookies, headers=standard_headers, timeout=timeout)
        for proxy in r.json():
            proxies_set27.add(f"{proxy.get('host')}:{proxy.get('port')}")
        logger.info(f"From {short_url(r.url)} were parsed {len(proxies_set27)} proxies")
    except Exception:
        logger.exception(f"Proxies from {short_url(url)} were not loaded :(")
    return proxies_set27


def proxynova() -> Set[str]:
    url = "https://www.proxynova.com/proxy-server-list/"
    proxies_set28 = set()
    try:
        r = requests.get(url, headers=standard_headers, timeout=timeout)
        soup = BeautifulSoup(r.content, "lxml")
        table = soup.find("table", {"id": "tbl_proxy_list"}).find("tbody")
        for tr in table.find_all("tr"):
            if tr.attrs.get("data-proxy-id") is not None:
                tds = tr.find_all("td")
                host = tds[0].find("script").text.strip().split("'")[1]
                port = tds[1].text.strip()
            proxies_set28.add(f"{host}:{port}")
        logger.info(f"From {short_url(r.url)} were parsed {len(proxies_set28)} proxies")
    except Exception:
        logger.exception(f"Proxies from {short_url(url)} were not loaded :(")
    return proxies_set28


def fatezero2() -> Set[str]:
    url = "http://proxylist.fatezero.org/proxy.list"
    proxies_set29 = set()
    try:
        r = requests.get(url, headers=standard_headers, timeout=timeout)
        raw_proxies = r.text.strip().split("\n")
        for raw_proxy in raw_proxies:
            proxy = json.loads(raw_proxy)
            if proxy.get("type") == "https":
                proxies_set29.add(f"{proxy['host']}:{proxy['port']}")
        logger.info(f"From {short_url(r.url)} were parsed {len(proxies_set29)} proxies")
    except Exception:
        logger.exception(f"Proxies from {short_url(url)} were not loaded :(")
    return proxies_set29


def xiladaili() -> Set[str]:
    url = "http://www.xiladaili.com/https"
    proxies_set30 = set()
    max_page_num = 8
    try:
        for n in range(max_page_num):
            url = f"http://www.xiladaili.com/https/{n}"
            r = requests.get(url, headers=standard_headers, timeout=timeout)
            if r.ok:
                proxies_set30.update(parse_proxies(r.text))
            time.sleep(0.5)
        logger.info(f"From {short_url(r.url)} were parsed {len(proxies_set30)} proxies")
    except Exception:
        logger.exception(f"Proxies from {short_url(url)} were not loaded :(")
    return proxies_set30


def geonode() -> Set[str]:
    url = "https://proxylist.geonode.com/api/proxy-list"
    params = {
        "limit": 500,
        "page": 1,
        "sort_by": "lastChecked",
        "sort_type": "desc",
        "protocols": "https",
    }
    proxies_set31 = set()
    try:
        r = requests.get(url, params=params, headers=standard_headers, timeout=timeout)
        r_data = r.json()
        for proxy in r_data.get("data"):
            proxies_set31.add(f"{proxy.get('ip')}:{proxy.get('port')}")
        logger.info(f"From {short_url(url)} were parsed {len(proxies_set31)} proxies")
    except Exception:
        logger.exception(f"Proxies from {short_url(url)} were not loaded :(")
    return proxies_set31
