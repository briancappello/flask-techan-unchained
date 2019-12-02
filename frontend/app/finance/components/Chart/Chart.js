import React from 'react'
import PropTypes from 'prop-types'

import isFunction from 'lodash/isFunction'
import techan from 'techan'

import { log_debug, log_critical } from 'logging'

import {
  CHART_HEADER_HEIGHT, CHART_SIDEBAR_WIDTH,
  BAR_CHART, CANDLE_CHART, LINE_CHART,
  LINEAR_SCALE, LOG_SCALE,
  FREQUENCY,
  FORMATS,
  CHART_INDICATOR,
} from 'finance/constants'
import { niceLogMin, niceLogMax, getLogTickValues } from 'finance/utils/logScale'

import './chart.scss'


const CHART_TYPES = {
  [LINE_CHART]: techan.plot.close(),
  [CANDLE_CHART]: techan.plot.candlestick(),
  [BAR_CHART]: techan.plot.ohlc(),
}

const SCALES = {
  [LINEAR_SCALE]: d3.scaleLinear(),
  [LOG_SCALE]: d3.scaleLog(),
}

const MAX_BARS = 300

export default class Chart extends React.Component {

  static propTypes = {
    id: PropTypes.string.isRequired,
    ticker: PropTypes.string.isRequired,
    frequency: PropTypes.string.isRequired,
    scale: PropTypes.string.isRequired,
    type: PropTypes.string.isRequired,
  }

  static defaultProps = {
    showCrosshairs: true,
    upperIndicators: ['Volume', 'BBands', 'SMA100', 'SMA200'],
    indicatorHeight: 100,
    indicators: ['MACD', 'RSI', 'Stochastics'],
    scale: LINEAR_SCALE,
    chartId: 'chart',
    type: CANDLE_CHART,
  }

  constructor(props) {
    super(props)
    log_debug('Chart: constructor')

    this.margin = { top: 10, right: 45, bottom: 20, left: 45 }

    let visibleBars = 0
    let startIdx = 0
    if (props.data && props.data.length) {
      visibleBars = Math.min(props.data.length, MAX_BARS)
      startIdx = Math.max(props.data.length - visibleBars, 0)
    }

    const { chartId, data, indicators, indicatorHeight, upperIndicators } = props

    this.state = {
      clipId: chartId + '-plotClip',
      visibleBars,
      startIdx,
      totalHeight: this._getTotalHeight(),
      currentBar: null,
      latestBar: data ? data[data.length - 1] : {},
      upperIndicators: upperIndicators.map((indicatorName) => {
        const Indicator = require(`finance/indicators/${indicatorName}`).default
        return new Indicator()
      }),
      indicators: indicators.map((indicatorName) => {
        const Indicator = require(`finance/indicators/${indicatorName}`).default
        return new Indicator()
      }),
      indicatorHeight: indicatorHeight,
    }
  }

  _isIntraday() {
    return ![FREQUENCY.Daily,
                    FREQUENCY.Weekly,
                    FREQUENCY.Monthly,
                    FREQUENCY.Yearly].includes(this.props.frequency)
  }

  componentDidMount() {
    log_debug('Chart: componentDidMount')

    this.state.totalWidth = this._getTotalWidth()
    window.addEventListener('resize', this.handleResize)

    const { data } = this.props
    if (data && data.length) {
      this.refreshChart()
    }
  }

  componentWillReceiveProps(nextProps) {
    log_debug('Chart: componentWillReceiveProps')

    const { data } = nextProps

    let visibleBars = 0
    let startIdx = 0
    let latestBar = {}

    if (data && data.length) {
      visibleBars = Math.min(data.length, MAX_BARS)
      startIdx = Math.max(data.length - visibleBars, 0)
      latestBar = data[data.length - 1]
    }

    this.setState({ visibleBars, startIdx, latestBar })
  }

  shouldChartUpdate(prevProps, prevState) {
    const propKeys = ['data', 'type', 'scale']
    for (let key of propKeys) {
      if (this.props[key] != prevProps[key]) {
        return true
      }
    }

    const stateKeys = ['startIdx', 'totalHeight', 'totalWidth']
    for (let key of stateKeys) {
      if (this.state[key] != prevState[key]) {
        return true
      }
    }

    return false
  }

  componentDidUpdate(prevProps, prevState) {
    log_debug('Chart: componentDidUpdate')

    if (this.shouldChartUpdate(prevProps, prevState)) {
      this.refreshChart()
    }
  }

  refreshChart() {
    log_debug('Chart (d3): refreshChart')

    const { chartId, data } = this.props

    // remove old chart, then draw a new one
    d3.select(`#${chartId} svg`).remove()
    this.drawChart()

    if (data && data.length) {
      const { startIdx, visibleBars } = this.state
      const endIdx = startIdx + visibleBars
      if (endIdx != 0) {
        this.drawChartData(data.slice(startIdx, endIdx))
      } else {
        this.drawChartData(data.slice(startIdx))
      }
    }
  }

  drawChart() {
    log_debug('Chart (d3): drawChart')

    const { chartId, showCrosshairs } = this.props
    const { totalHeight, totalWidth, indicators, indicatorHeight } = this.state

    this.chartHeight = totalHeight - this.margin.top - this.margin.bottom
    this.chartWidth = totalWidth - this.margin.left - this.margin.right

    this.priceChartWidth = this.chartWidth
    this.priceChartHeight = this.chartHeight - ((indicatorHeight + CHART_INDICATOR.padding) * indicators.length)

    let rootSvg = d3.select(`#${chartId}`).append('svg')
      .attr('height', totalHeight)
      .attr('width', totalWidth)

    // the chart viewport (everything inside the declared margins)
    this.svg = rootSvg.append('g')
      .attr('transform', `translate(${this.margin.left}, ${this.margin.top})`)
      .call(d3.zoom().on('zoom', this.handleScroll))

    this._drawAxes()  // must come before priceChart & indicators
    this._drawPriceChart()

    indicators.forEach((indicator, i) => {
      indicator.init({
        svg: this.svg,
        xScale: this.xScale,
        yScale: this._getIndicatorScale(i + 1),
      })

      indicator.draw()
    })

    if (showCrosshairs) {
      this._drawPriceChartCrosshairs()
      for (let indicator of indicators) {
        indicator.drawCrosshairs()
          .xAnnotation([this.dateAnnotation])
          .verticalWireRange([0, this.chartHeight])
          .on('move', this.crosshairMove)
          .on('out', this.crosshairOut)
        indicator.connectCrosshairs()
      }
    }
  }

  drawChartData(data) {
    log_debug('Chart (d3): drawChartData')
    const { latestBar, indicators, upperIndicators } = this.state

    // DOMAINS
    this.xScale.domain(techan.scale.plot.time(data).domain())

    // calculate y domain based on min/max of both price and bbands (if possible)
    let yMin = Math.min(...data.map(d => d.low))
    let yMax = Math.max(...data.map(d => d.high))
    let yDomain = [yMin, yMax]

    if (this.props.upperIndicators.includes('BBands')) {
      let bbandsMin = Math.min(...data.map(d => d.bbands_lower))
      let bbandsMax = Math.max(...data.map(d => d.bbands_upper))
      yDomain = [
        bbandsMin > 0
          ? Math.min(yMin, bbandsMin)
          : yMin,
        Math.max(yMax, bbandsMax),
      ]
    }

    if (this.props.scale == LINEAR_SCALE) {
      this.yScale.domain(yDomain).nice()
    } else {
      // d3's nice() doesn't work so well with logarithmic scale
      const logMin = niceLogMin(yDomain[0])
      const logMax = niceLogMax(yDomain[1])
      this.yScale.domain([logMin, logMax])

      const logTickValues = getLogTickValues(logMin, logMax)
      this.yGrid.tickValues(logTickValues)
      this.yAxis.tickValues(logTickValues)
      this.yAxisRight.tickValues(logTickValues)
    }

    // AXES
    this.svg.select('g.x.axis').call(this.xAxis)
    this.svg.select('g.x.grid').call(this.xGrid)
    this.svg.select('g.y.axis').call(this.yAxis)
    this.svg.select('g.y.axis.right').call(this.yAxisRight)
    this.svg.select('g.y.grid').call(this.yGrid)

    // OHLC
    this.svg.select('g.price-chart').datum(data).call(this.priceChart)

    if (this.props.showCrosshairs) {
      this.svg.select('g.price-chart.crosshair').call(this.priceChartCrosshair)
    }

    // INDICATORS
    for (let indicator of upperIndicators) {
      indicator.drawChartData(data)
      isFunction(indicator.drawLegend) && indicator.drawLegend(latestBar)
    }

    for (let indicator of indicators) {
      indicator.drawChartData(data)
      indicator.drawLegend(latestBar)
    }
  }

  _drawAxes() {
    // x axis
    this.xScale = techan.scale.financetime()
      .range([0, this.chartWidth])
      .outerPadding(1)

    this.xAxis = d3.axisBottom(this.xScale)
      .tickSizeOuter(0)

    this.svg.append('g')
      .attr('class', 'x axis')
      .attr('transform', `translate(0, ${this.chartHeight})`)

    // x grid
    this.xGrid = d3.axisBottom(this.xScale)
      .ticks(8) // FIXME: this draws quarterly lines with daily data, what about intraday/weekly/monthly??
      .tickFormat(() => null)
      .tickSizeInner(-this.priceChartHeight)
      .tickSizeOuter(-this.priceChartHeight)

    this.svg.append('g')
      .attr('class', 'x grid')
      .attr('transform', `translate(0, ${this.priceChartHeight})`)

    // y axis
    this.yScale = SCALES[this.props.scale]
      .range([this.priceChartHeight, 0])

    this.yAxis = d3.axisLeft(this.yScale)
      .tickFormat(FORMATS.SMART)

    this.svg.append('g')
      .attr('class', 'y axis')

    this.yAxisRight = d3.axisRight(this.yScale)
      .tickSizeOuter(0)
      .tickFormat(FORMATS.SMART)

    this.svg.append('g')
      .attr('class', 'y axis right')
      .attr('transform', `translate(${this.chartWidth}, 0)`)

    // y grid
    this.yGrid = d3.axisLeft(this.yScale)
      .tickFormat(() => null)
      .tickSizeInner(-this.chartWidth)
      .tickSizeOuter(-this.chartWidth)

    this.svg.append('g')
      .attr('class', 'y grid')
  }

  _drawPriceChart() {
    const { clipId, upperIndicators } = this.state

    this.priceChart = CHART_TYPES[this.props.type]
      .xScale(this.xScale)
      .yScale(this.yScale)

    this.svg.append('g')
      .attr('class', 'price-chart')

    // create a clip path so that indicators don't visually overflow the price plot viewport
    this.svg.append('defs')
      .append('clipPath')
      .attr('id', clipId)
      .append('rect')
      .attr('x', 0)
      .attr('y', 0)
      .attr('width', this.priceChartWidth)
      .attr('height', this.priceChartHeight)

    for (let indicator of upperIndicators) {
      indicator.init({
        svg: this.svg,
        xScale: this.xScale,
        yScale: this.yScale,
        priceChart: this.priceChart,
      })
      indicator.draw(clipId)
    }
  }

  _drawPriceChartCrosshairs() {
    // crosshair current date label
    this.dateAnnotation = techan.plot.axisannotation()
      .axis(this.xAxis)
      .orient('bottom')
      .format(this._isIntraday() ? FORMATS.DATETIME : FORMATS.DATE)
      .width(this._isIntraday() ? 100 : 75)
      .translate([0, this.chartHeight])

    // crosshair current price label
    this.cursorPriceLevelAnnotation = techan.plot.axisannotation()
      .axis(this.yAxis)
      .orient('left')
      .format(FORMATS.DEC)

    this.cursorPriceLevelAnnotationRight = techan.plot.axisannotation()
      .axis(this.yAxisRight)
      .orient('right')
      .format(FORMATS.DEC)
      .translate([this.chartWidth, 0])

    let yAnnotations = [
      this.cursorPriceLevelAnnotation,
      this.cursorPriceLevelAnnotationRight,
    ]

    const { upperIndicators } = this.state
    for (let indicator of upperIndicators) {
      let yAnnotation = null
      if (isFunction(indicator.getCrosshairsYAnnotation)) {
        yAnnotation = indicator.getCrosshairsYAnnotation()
      }
      if (yAnnotation) {
        yAnnotations.push(yAnnotation)
      }
    }

    // priceChart crosshairs
    this.priceChartCrosshair = techan.plot.crosshair()
      .xScale(this.xScale)
      .yScale(this.yScale)
      .xAnnotation([this.dateAnnotation])
      .yAnnotation(yAnnotations)
      .verticalWireRange([0, this.chartHeight])
      .on('move', this.crosshairMove)
      .on('out', this.crosshairOut)

    // add crosshair group container to the svg
    this.svg.append('g')
      .attr('class', 'price-chart crosshair')

    // this serves as an index lookup for mouse events (to get the current bar)
    this.dataIndexScale = d3.scaleLinear()
      .domain([0, this.state.visibleBars])
      .range([0, this.chartWidth])
  }

  _getIndicatorScale(number, domain = [0, 100]) {
    const { indicators, indicatorHeight } = this.state
    if (number < 1 || number > indicators.length) throw new Error(
      `Indicator number must be between 1 and ${indicators.length} (${number} given).`
    )

    const indicatorScaleHelper = d3.scaleLinear()
      .domain([1, indicators.length])
      .range([
        this.priceChartHeight + CHART_INDICATOR.padding, // top of first indicator
        this.chartHeight - indicatorHeight               // top of last indicator
      ])

    return d3.scaleLinear()
      .domain(domain)
      .range([
        indicatorScaleHelper(number) + indicatorHeight,
        indicatorScaleHelper(number)
      ])
  }

  handleScroll = () => {
    const e = d3.event.sourceEvent
    let barDelta = 0

    // double click
    if (e == null) {
      return
    }

    // scroll wheel
    if (e.type == 'wheel') {
      if (e.deltaY < 0) {
        barDelta = 1
      } else {
        barDelta = -1
      }

    // click'n'drag
    } else {
      barDelta = -Math.ceil(e.movementX / this._getBarWidth())
    }

    if (e.ctrlKey && e.shiftKey) {
      barDelta *= 100
    } else if (e.ctrlKey || e.shiftKey) {
      barDelta *= 10
    }

    const { startIdx, visibleBars } = this.state
    const newStartIdx = startIdx + barDelta

    if (newStartIdx <= 0) {
      this.setState({ startIdx: 0 })
    } else if (newStartIdx >= this.props.data.length - visibleBars) {
      this.setState({ startIdx: this.props.data.length - visibleBars })
    } else {
      this.setState({ startIdx: newStartIdx })
    }
  }

  crosshairMove = (coords) => {
    const { data } = this.props
    const currentBar = data[this._getBarIndex(coords.x)]
    this.setState({ currentBar })

    const { indicators } = this.state
    for (let indicator of indicators) {
      indicator.crosshairMove(currentBar)
    }
  }

  crosshairOut = () => {
    this.setState({ currentBar: null })

    const { indicators, latestBar } = this.state
    for (let indicator of indicators) {
      indicator.crosshairOut(latestBar)
    }
  }

  handleResize = () => {
    this.setState({
      totalHeight: this._getTotalHeight(),
      totalWidth: this._getTotalWidth(),
    })
  }

  _getTotalHeight = () => {
    const height = Math.max(document.documentElement.clientHeight, window.innerHeight)
    // the extra 5 is for ??? (prevents vertical scrollbar)
    // tested working in Chrome & FF as of Q1 2019
    return height - (CHART_HEADER_HEIGHT + 5)
  }

  _getTotalWidth = () => {
    const chartEl = document.getElementById(this.props.chartId).parentElement
    return Math.max(chartEl.clientWidth, window.innerWidth) - CHART_SIDEBAR_WIDTH
  }

  _getBarWidth = () => {
    return this.priceChartWidth / this.state.visibleBars
  }

  _getBarIndex = (xCoord) => {
    return this.state.startIdx + Math.floor(this.dataIndexScale.invert(this.xScale(xCoord)))
  }

  renderChartHeader() {
    const { ticker } = this.props
    const { currentBar, latestBar } = this.state
    const bar = currentBar && currentBar || latestBar

    return (
      <div className="chart-header">
        <div className="ohlc">
          <table>
          <tbody>
            <tr><th>D</th><td>{bar && FORMATS.DATE(bar.date)}</td></tr>
            <tr><th>O</th><td>{bar && FORMATS.DEC(bar.open)}</td></tr>
            <tr><th>H</th><td>{bar && FORMATS.DEC(bar.high)}</td></tr>
            <tr><th>L</th><td>{bar && FORMATS.DEC(bar.low)}</td></tr>
            <tr><th>C</th><td>{bar && FORMATS.DEC(bar.close)}</td></tr>
            <tr><th>V</th><td>{bar && FORMATS.SI(bar.volume)}</td></tr>
          </tbody>
          </table>
        </div>
        <div className="company-name">big fat old enterprise, llc</div>
        <div className="ticker">{ticker}</div>
      </div>
    )
  }

  render() {
    log_debug('Chart: render')
    const { chartId } = this.props

    return (
      <div>
        {this.renderChartHeader()}
        <div id={chartId} className="techan-chart" />
      </div>
    )
  }
}
