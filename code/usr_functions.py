from urllib import request


def cyrillic_url(cyr_str):
    return request.quote(cyr_str.encode('cp1251'))
