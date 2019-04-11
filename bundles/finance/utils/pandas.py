import html


def str_strip(s):
    try:
        return s.strip()
    except AttributeError:
        return s


def to_float(f):
    try:
        return float(f)
    except ValueError:
        return f


def to_int(i):
    try:
        return int(i)
    except ValueError:
        return i


def kmbt_to_int(s):
    multipliers = {'K': 1e3, 'M': 1e6, 'B': 1e9, 'T': 1e12}
    for suffix, multiplier in multipliers.items():
        if s.endswith(suffix):
            return int(float(s.replace(',', '').replace(suffix, '')) * multiplier)
    return int(s.replace(',', ''))


def to_percent(s):
    try:
        return float(s.rstrip('%'))
    except ValueError:
        return s


def html_unescape(s):
    try:
        return html.unescape(s)
    except TypeError:
        return s
