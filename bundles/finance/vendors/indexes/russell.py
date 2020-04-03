# Flask Techan Unchained
#
# Copyright (C) 2020  Brian Cappello
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import io
import requests

from pdfquery import PDFQuery
from pdfquery.cache import FileCache

from backend.config import Config


# urls found at http://www.ftserussell.com/supporting-documents
R1000_URL = 'http://www.ftserussell.com/files/support-documents/2017-r1000-membership-lists'
R2000_URL = 'http://www.ftserussell.com/files/support-documents/2017-ru2000-membership-list'


def load_pdf(file, pages):
    pdf = PDFQuery(file, parse_tree_cacher=FileCache(Config.APP_CACHE_FOLDER + '/'))
    pdf.load(*pages)
    return pdf


def extract_tickers(pdf):
    ticker_labels = pdf.pq('LTTextLineHorizontal:contains("Ticker")')

    ticker_left_col_label_pos = ticker_labels[0].attrib
    ticker_right_col_label_pos = ticker_labels[1].attrib

    results = pdf.extract([
        ('with_formatter', 'text'),
        ('left_col', 'LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (
            float(ticker_left_col_label_pos['x0']),
            0,
            float(ticker_left_col_label_pos['x1']) + 25,
            float(ticker_left_col_label_pos['y1']),
        )),
        ('right_col', 'LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (
            float(ticker_right_col_label_pos['x0']),
            0,
            float(ticker_right_col_label_pos['x1']) + 25,
            float(ticker_right_col_label_pos['y1']),
        ))
    ])

    tickers = set(results['left_col'].split(' ') + results['right_col'].split(' '))
    tickers.discard('Ticker')

    return tickers


def get_russell_1000_tickers():
    """A set of all the tickers in the Russell 1000"""
    r1000_pdf = load_pdf(io.BytesIO(requests.get(R1000_URL).content), range(0, 11))

    # lookup reason in left sidebar of https://www.bloomberg.com/quote/<TICKER>:US
    # search ticker changes at http://www.nasdaq.com/markets/stocks/symbol-change-history.aspx

    swaps = [
        ('TSO', 'ANDV'),    # rename
        ('DOW', 'DWDP'),    # rename/merger
        ('WFM', 'AMZN'),    # acquisition
        ('DFT', 'DLR'),     # acquisition
        ('KATE', 'COH'),    # acquisition
        ('PNRA', None),     # private acquisition
        ('WOOF', None),     # private acquisition
        ('PTHN', None),     # trading suspended
        ('RAI', None),      # acquired by BATS:LN (london)
        ('AWH', 'AWHHF'),   # OTC
        ('DD', 'DWDP'),     # acquisition
        ('SPLS', None),     # private acquisition
        ('CST', None),      # private acquisition
        ('BHI', None),      # delisted
    ]
    return extract_tickers(r1000_pdf)


def get_russell_2000_tickers():
    """A set of all the tickers in the Russell 2000"""
    r2000_pdf = load_pdf(io.BytesIO(requests.get(R2000_URL).content), range(0, 22))
    return extract_tickers(r2000_pdf)


def get_russell_3000_tickers():
    """A set of all the tickers in the Russell 3000"""
    r1000 = get_russell_1000_tickers()
    r2000 = get_russell_2000_tickers()
    return r1000.union(r2000)
