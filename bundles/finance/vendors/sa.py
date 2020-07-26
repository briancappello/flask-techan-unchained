import json
import requests


def get_symbol_info_url(symbol):
    return f'https://seekingalpha.com/symbol/{symbol.upper()}/overview'


def get_symbol_info(symbol):
    """
    company info keys:
    company_name
    long_desc
    """
    r = requests.get(get_symbol_info_url(symbol))
    return json_string_to_dict(r.text)


def json_string_to_dict(html: str, search_start: str = '"symbolQuoteInfo":') -> dict:
    start = html.find(search_start) + len(search_start)
    end = -1
    stack = 0
    for i, char in enumerate(html[start:]):
        if char == '{':
            stack += 1
        elif char == '}':
            stack -= 1
        if stack == 0:
            end = start + i + 1
            break
    return json.loads(html[start:end])
