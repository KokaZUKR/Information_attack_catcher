from urllib import request


def cyrillic_url(cyr_str):
    return request.quote("нато".encode('cp1251'))
