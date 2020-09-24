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

      // https://github.com/d3/d3-time-format#locale_format
      DATE = '%b %d, %Y',
      DATETIME = '%a %_m/%d %_I:%M %p',
      MINUTELY_TICK_FMT = '%_I:%M %p'

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
  MINUTELY_TICK_FMT: function (date, i, nodes) {
    if (i > 0) {
      const getX = function(node) {
        const transform = node.parentElement.attributes.transform.value
        const re = /translate\(([\d\.]+),([\d\.]+)\)/
        const matches = transform.match(re)
        return parseFloat(matches[1])
      }

      const prevX = getX(nodes[i-1]),
            thisX = getX(nodes[i])
      if ((thisX - prevX) < 50) {
        return null
      }
    }
    return d3.timeFormat(MINUTELY_TICK_FMT)(date)
  },
  DAILY_TICK_FMT: function (d) {
    if (d.getMonth() === 0) {
      return d3.timeFormat('%b %Y')(d)
    }
    return d3.timeFormat('%b')(d)
  },
}

export const CHART_INDICATOR_LABEL = {
  fontSize: 10,
  padding: 5,
}

export const CHART_INDICATOR = {
  padding: CHART_INDICATOR_LABEL.fontSize + CHART_INDICATOR_LABEL.padding,
}
