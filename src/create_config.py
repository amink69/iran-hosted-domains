import json
from typing import Iterable

import constants as consts
import utils


def shadowrocket(domains: Iterable[str]):
    config = (
        "#Shadowrocket\n"
        "[General]\n"
        "bypass-system = true\n"
        "skip-proxy = 192.168.0.0/16, 10.0.0.0/8, 172.16.0.0/12, localhost, *.local, captive.apple.com\n"
        "tun-excluded-routes = 10.0.0.0/8, 100.64.0.0/10, 127.0.0.0/8, 169.254.0.0/16, 172.16.0.0/12, 192.0.0.0/24, 192.0.2.0/24, 192.88.99.0/24, 192.168.0.0/16, 198.18.0.0/15, 198.51.100.0/24, 203.0.113.0/24, 224.0.0.0/4, 255.255.255.255/32\n"
        "dns-server = system\n"
        "ipv6 = true\n"
        "[Rule]\n"
    )
    config += "".join(f"DOMAIN-SUFFIX,{domain},DIRECT\n" for domain in domains)
    config += (
        "USER-AGENT,Line*,PROXY\n"
        "IP-CIDR,192.168.0.0/16,DIRECT\n"
        "IP-CIDR,10.0.0.0/8,DIRECT\n"
        "IP-CIDR,172.16.0.0/12,DIRECT\n"
        "IP-CIDR,127.0.0.0/8,DIRECT\n"
        "GEOIP,IR,DIRECT\n"
        "FINAL,PROXY\n"
        "[Host]\n"
        "localhost = 127.0.0.1\n"
    )

    utils.save_to_file(consts.shadowrocket_path, config)


def qv2ray(directs: Iterable[str], proxies: Iterable[str], ads: Iterable[str]):
    schema = {
        "description": "Iran hosted domains",
        "domainStrategy": "AsIs",
        "domains": {
            "direct": ["regexp:^.+\\.ir$"] + list(directs),
            "proxy": list(proxies),
            "block": ["geosite:category-ads-all"] + list(ads),
        },
        "ips": {"direct": ["geoip:ir"]},
        "name": "ir_hosted",
    }

    utils.save_to_file(consts.qv2ray_schema_path, json.dumps(schema))


def clash(domains: Iterable[str]):
    config = (
        "# Clash\n"
        "# Wiki: https://github.com/Dreamacro/clash/wiki/premium-core-features#rule-providers\n"
        "payload:\n"
    )
    config += "".join(f"  - DOMAIN-SUFFIX,{domain}\n" for domain in domains)
    config += (
        "  - IP-CIDR,192.168.0.0/16\n"
        "  - IP-CIDR,10.0.0.0/8\n"
        "  - IP-CIDR,172.16.0.0/12\n"
        "  - IP-CIDR,127.0.0.0/8\n"
        "  - GEOIP,IR\n"
    )

    utils.save_to_file(consts.clash_path, config)


def switchy_omega(others: Iterable[str]):
    config = "127.0.0.1\n" "::1\n" "localhost\n" "*.ir\n"
    config += "".join(f"*{domain}\n" for domain in others)

    utils.save_to_file(consts.switchy_omega_path, config)
