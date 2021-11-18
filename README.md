<h1 align="center">Proxy Machine</h1>
<h2 align="center">
    <a href="https://github.com/batiscuff/proxy_machine/blob/main/LICENSE" target="_blank">
        <img alt="License: GPLv3" src="https://img.shields.io/badge/License-GPLv3-green.svg" />
    </a>
    <a href="https://github.com/psf/black" target="_blank">
        <img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg" />
    </a>
    </a href="https://github.com/batiscuff/proxy_machine" target="_blank">
        <img alt="Build with love <3" src="https://img.shields.io/badge/build%20with-%F0%9F%92%9D-green" />
    </a>
</h2>

## Description 
The maximum number of proxies you can get is 35.000 </br>

**List of sites for parsing proxies:**
- [free-proxy-list.net/anonymous-proxy.html](http://free-proxy-list.net/anonymous-proxy.html)
- [free-proxy-list.net](http://free-proxy-list.net)
- [proxy-daily.com](http://proxy-daily.com)
- [sslproxies.org](http://sslproxies.org)
- [free-proxy-list.net/uk-proxy.html](http://free-proxy-list.net/uk-proxy.html)
- [us-proxy.org](http://us-proxy.org)
- [api.proxyscrape.com](http://proxyscrape.com)
- [checkerproxy.net](http://checkerproxy.net)
- [proxy50-50.blogspot.com](http://proxy50-50.blogspot.com)
- [hidester.com](http://hidester.com)
- [awmproxy.net](http://awmproxy.net)
- [api.openproxy.space](http://openproxy.space)
- [aliveproxy.com](http://aliveproxy.com)
- [community.aliveproxy.com](http://community.aliveproxy.com)
- [hidemy.name](http://hidemy.name/en)
- [proxy11.com](http://proxy11.com)
- [spys.me](http://spys.me/proxy.txt)
- [proxysearcher](http://proxysearcher.sourceforge.net)
- [fatezero](http://static.fatezero.org/tmp/proxy.txt)
- [pubproxy](http://pubproxy.com/)
- [proxylists](http://www.proxylists.net/http_highanon.txt)
- [ab57ru](http://ab57.ru/downloads/proxylist.txt)
- [shifty-https](http://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt)
- [shifty-http](http://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt)
- [sunny9577](http://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt)
- [multiproxy](http://multiproxy.org/txt_all/proxy.txt)
- [rootjazz](http://rootjazz.com/proxies/proxies.txt)
- [proxyscan.io](http://www.proxyscan.io/api/proxy?format=txt&ping=500&limit=10000&type=http,https)
- [proxy-list.download](http://www.proxy-list.download/api/v0/get?l=en&t=http)
- [proxylistplus.com](http://list.proxylistplus.com/SSL-List-1)
- [proxyhub.me](http://www.proxyhub.me/ru/all-https-proxy-list.html)
- [proxylist4all.com](http://www.proxylist4all.com)
- [proxynova.com](http://www.proxynova.com/proxy-server-list)
- [xiladaili.com](http://www.xiladaili.com/https)

## Install through pip

```sh
pip install proxy_machine
```
## Install 
```sh
sudo apt update && sudo apt upgrade
sudo apt-get install python3 python3-pip
git clone https://github.com/batiscuff/proxy_machine
cd proxy_machine
pip3 install -r requirements.txt
```

## Usage
```sh
python3 -m proxy_machine
```
or
```shell
proxy_machine --help
```
#### Usage with proxy checker
```sh
python3 -m proxy_machine -pc
```
In this case, all parsed proxies will pass through the 
checker(this will take **2-4 hours**, prepare to wait) and
only working proxies will be written to *proxies.txt*.
  However, remember that the main weakness of free proxies 
is that they rapidly expire.
#### Usage with other options
```sh
python3 -m proxy_machine -h
```

## Future Development

[x] - Add async checking of the proxy to improve timing. <br/>
[x] - Improve cli options and args. <br/>
[ ] - Upload to pypi. <br/>
[ ] - Add proxy response time to the results by calculating execution in the checker <br />
[ ] - Add proxy location to the results <br/>
[ ] - Add filtering and sorting options to the results <br/>
[ ] - Add early stop, if the required number of proxies are reached with given constrains <br/>
[ ] - Add more websites to retrieve proxies

## License
**This project is GNU [General Public License v3.0](https://github.com/batiscuff/proxy_machine/blob/main/LICENSE) licensed**
