def get(l, i, default=None):
    """Safe version of list[:i]"""
    try:
        return l[i]
    except IndexError:
        return default


def get_rem(l, i, default=[]):
    """Safe version of list[i:]"""
    try:
        return l[i:]
    except IndexError:
        return default


def get_prev(l, i, default=[]):
    """Safe version of list[:i]"""
    try:
        return l[:i]
    except IndexError:
        return default
