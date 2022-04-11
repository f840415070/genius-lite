import hashlib


def md5(data):
    return hashlib.md5(data.encode()).hexdigest()[8:24]


def obj_to_str(data):
    if isinstance(data, dict):
        return '&'.join(['{}={}'.format(key, val) for key, val in data.items()])
    if isinstance(data, list):
        return ', '.join(data)
    return str(data)


def str_sort(data):
    return ''.join((lambda x: (x.sort(), x)[1])(list(data)))
