import re
from urllib.parse import urlparse


def short_url(url: str) -> str:
    return urlparse(url).netloc.upper()


def parse_proxies(response: str) -> set:
    return set(re.findall(r"((?:\d{1,3}\.){3}\d{1,3}:\d{1,5})", response))


def prepare_proxy(ip_port: str) -> str:
    return f"http://{ip_port}"
