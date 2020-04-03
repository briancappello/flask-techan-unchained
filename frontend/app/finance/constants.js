// Flask Techan Unchained
//
// Copyright (C) 2020  Brian Cappello
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Affero General Public License for more details.
//
// You should have received a copy of the GNU Affero General Public License
// along with this program.  If not, see <https://www.gnu.org/licenses/>.

export const CHART_HEADER_HEIGHT = 100 // should match $chart-header-height in chart.scss
export const CHART_SIDEBAR_WIDTH = 200 // should match $sidebar-width in chart-container.scss

export const BAR_CHART = 'BAR'
export const CANDLE_CHART = 'CANDLE'
export const LINE_CHART = 'LINE'

export const LINEAR_SCALE = 'LINEAR'
export const LOG_SCALE = 'LOG'

export const FREQUENCY = {
  Minutely: '1m',
  FiveMinutely: '5m',
  TenMinutely: '10m',
  FifteenMinutely: '15m',
  ThirtyMinutely: '30m',
  Hourly: '1hr',
  Daily: 'D',
  Weekly: 'W',
  Monthly: 'M',
  Yearly: 'Y',
}

// https://github.com/d3/d3-format#api-reference
const DEC = ',.2f',
      DEC1 = ',.1f',
      INT = ',.0f',
      SI = ',.3s',
      DATE = '%b %d, %Y', // https://github.com/d3/d3-time-format#locale_format
      DATETIME = '%a %m/%d %I:%M%p'

export const FORMATS = {
  DEC: d3.format(DEC),
  DEC1: d3.format(DEC1),
  INT: d3.format(INT),
  SI: d3.format(SI),
  SMART: function (num) {
    if (num < 100) {
      return d3.format(DEC)(num)
    } else if (num < 10000) {
      return d3.format(INT)(num)
    } else {
      return d3.format(SI)(num)
    }
  },
  DATE: d3.timeFormat(DATE),
  DATETIME: d3.timeFormat(DATETIME),
}

export const CHART_INDICATOR_LABEL = {
  fontSize: 10,
  padding: 5,
}

export const CHART_INDICATOR = {
  padding: CHART_INDICATOR_LABEL.fontSize + (CHART_INDICATOR_LABEL.padding * 2)
}
