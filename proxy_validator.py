import logging


def read_proxies(filename):
    with open(filename) as f:
        proxies = [line.strip() for line in f.readlines()]


return proxies


def validate_proxy_format(proxy):

    try:
        parts = proxy.split("://")
    except ValueError:
        logging.error(f"Invalid proxy format: {proxy}")
        return False

    if len(parts) != 2:
        logging.error(f"Invalid proxy format: {proxy}")
        return False

    if "@" not in parts[1]:
        logging.error(f"Invalid proxy format: {proxy}")
        return False

    return True
