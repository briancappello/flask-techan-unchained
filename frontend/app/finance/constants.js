export const CHART_HEADER_HEIGHT = 100 // should match $chart-header-height in chart.scss
export const CHART_SIDEBAR_WIDTH = 200 // should match $sidebar-width in chart-container.scss

export const BAR_CHART = 'BAR'
export const CANDLE_CHART = 'CANDLE'
export const LINE_CHART = 'LINE'

export const LINEAR_SCALE = 'LINEAR'
export const LOG_SCALE = 'LOG'

export const FREQUENCY = {
  Minutely: '1min',
  FiveMinutely: '5min',
  TenMinutely: '10min',
  FifteenMinutely: '15min',
  ThirtyMinutely: '30min',
  Hourly: 'h',
  Daily: 'D',
  Weekly: 'W',
  Monthly: 'M',
  Quarter: 'Q',
  Yearly: 'Y',
}

// https://github.com/d3/d3-format#api-reference
const DEC = ',.2f',
      DEC1 = ',.1f',
      DEC4 = ',.4f',
      INT = ',.0f',
      SI = ',.3s',

      // https://github.com/d3/d3-time-format#locale_format
      DATE = '%b %d, %Y',
      DATETIME = '%b %d, %Y %_I:%M %p'

let dateFormatter = new Intl.DateTimeFormat("en-US", {
  month: "short",
  day: "numeric",
  year: "numeric",
  timeZone: "America/New_York",
}).format

let timeFormatter = new Intl.DateTimeFormat("en-US", {
  hour: "numeric",
  minute: "2-digit",
  timeZone: "America/New_York",
  dayPeriod: undefined,
}).format

let tzOffset = ((new Date().getTimezoneOffset()) / 60) - 5;

function minutelyTickFormat(dt, i, nodes) {
  if (i > 0) {
    const getX = function(node) {
      const transform = node.parentElement.attributes.transform.value
      const re = /translate\(([\d\.]+),([\d\.]+)\)/
      const matches = transform.match(re)
      return parseFloat(matches[1])
    }

    const prevX = getX(nodes[i-1]),
          thisX = getX(nodes[i])

    if ((thisX - prevX) < 30) {
      return null
    }
  }

  const date = d3.timeFormat('%_m/%d')(dt)
  const time = timeFormatter(dt).replace(" AM", "a").replace(" PM", "p")

  if (dt.getMinutes() === 0) {
    return time.replace(":00", "")
  } else if (dt.getHours() === (9 - tzOffset) && dt.getMinutes() === 30) {
    return date + " " + time
  }
  return time;
}

function dailyTickFormat(dt) {
  if (dt.getMonth() === 0) {
    return d3.timeFormat('%b %Y')(dt)
  }
  return d3.timeFormat('%b')(dt)
}

export const FORMATS = {
  DEC: d3.format(DEC),
  DEC1: d3.format(DEC1),
  INT: d3.format(INT),
  SI: d3.format(SI),
  SMART: function (num) {
    if (num < 2) {
      let d4 = d3.format(DEC4)(num)
      let d2 = d3.format(DEC)(num)
      if (Number(d2) === Number(d4)) {
        return d2
      }
      return d4
    } else if (num < 100) {
      return d3.format(DEC)(num)
    } else if (num < 10000) {
      return d3.format(INT)(num)
    } else {
      return d3.format(SI)(num)
    }
  },
  DATE: dateFormatter,
  DATETIME: (dt) => `${dateFormatter(dt)} ${timeFormatter(dt)}`,
  [FREQUENCY.Minutely]: minutelyTickFormat,
  [FREQUENCY.FiveMinutely]: minutelyTickFormat,
  [FREQUENCY.TenMinutely]: minutelyTickFormat,
  [FREQUENCY.FifteenMinutely]: minutelyTickFormat,
  [FREQUENCY.ThirtyMinutely]: d3.timeFormat('%_m/%d'),
  [FREQUENCY.Hourly]: d3.timeFormat('%_m/%d'),
  [FREQUENCY.Daily]: dailyTickFormat,
  [FREQUENCY.Weekly]: dailyTickFormat,
  [FREQUENCY.Monthly]: d3.timeFormat('%Y'),
  [FREQUENCY.Yearly]: d3.timeFormat('%Y'),
}

export const CHART_INDICATOR_LABEL = {
  fontSize: 10,
  padding: 5,
}

export const CHART_INDICATOR = {
  padding: CHART_INDICATOR_LABEL.fontSize + CHART_INDICATOR_LABEL.padding,
}
