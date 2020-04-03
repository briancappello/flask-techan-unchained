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

from flask_unchained import injectable
from flask_unchained.cli import click

from .group import finance
from ..services import DataService, EquityManager, MarketstoreService
from ..vendors import yahoo


@finance.command()
def init():
    data_service = DataService(click.echo)
    data_service.init()


@finance.command()
@click.argument('symbols', nargs=-1)
def sync(
    symbols,
    equity_manager: EquityManager = injectable,
    marketstore_service: MarketstoreService = injectable,
):
    if not symbols:
        symbols = [equity.ticker for equity in equity_manager.all()]

    for i, symbol in enumerate(symbols):
        click.echo(f'{i+1}/{len(symbols)}: Syncing data for {symbol}')

        df = yahoo.get_daily_df(symbol)
        if df is None:
            print(f'no data for {symbol}')
            continue

        resp = marketstore_service.write(df, f'{symbol}/1D/OHLCV')
        if resp['responses'] is not None:
            print(resp)

    click.echo('Done.')
