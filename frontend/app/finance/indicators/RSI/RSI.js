import techan from 'techan'

import { FORMATS, CHART_INDICATOR_LABEL } from 'finance/constants'

import './RSI.scss'


export default class RSI {
  init({ svg, xScale, yScale }) {
    this.svg = svg
    this.xScale = xScale
    this.yScale = yScale
    this.chartWidth = this.xScale.range()[1]
    this.indicatorLabelY = this.yScale.range()[1] - CHART_INDICATOR_LABEL.padding
  }

  draw() {
    // axes
    const rsiTicks = [0, 30, 50, 70, 100]
    this.yAxisLeft = d3.axisLeft(this.yScale)
      .tickValues(rsiTicks)
      .tickSizeOuter(-this.chartWidth)

    this.svg.append('g')
      .attr('class', 'rsi axis')

    this.yAxisRight = d3.axisRight(this.yScale)
      .tickValues(rsiTicks)

    this.svg.append('g')
      .attr('class', 'rsi axis right')
      .attr('transform', `translate(${this.chartWidth}, 0)`)

    // indicator
    this.rsi = techan.plot.rsi()
      .xScale(this.xScale)
      .yScale(this.yScale)

    this.rsi.accessor()
      .rsi(d => d.rsi)
      .overbought(d => 70)
      .middle(d => 50)
      .oversold(d => 30)

    this.svg.append('g')
      .attr('class', 'indicator rsi')
  }

  drawCrosshairs() {
    this.yAnnotationLeft = techan.plot.axisannotation()
      .axis(this.yAxisLeft)
      .orient('left')

    this.yAnnotationRight = techan.plot.axisannotation()
      .axis(this.yAxisRight)
      .orient('right')
      .translate([this.chartWidth, 0])

    this.crosshair = techan.plot.crosshair()
      .xScale(this.xScale)
      .yScale(this.yScale)
      .yAnnotation([this.yAnnotationLeft, this.yAnnotationRight])

    this.svg.append('g')
      .attr('class', 'rsi crosshair')

    return this.crosshair
  }

  connectCrosshairs() {
    this.svg.select('g.rsi.crosshair').call(this.crosshair)
  }

  drawChartData(data) {
    this.svg.select('g.rsi.axis').call(this.yAxisLeft)
    this.svg.select('g.rsi.axis.right').call(this.yAxisRight)
    this.svg.select('g.rsi.indicator').datum(data).call(this.rsi)
  }

  drawLegend(latestBar) {
    this.legendLabel = this.svg.append('text')
      .attr('x', CHART_INDICATOR_LABEL.padding)
      .attr('y', this.indicatorLabelY)
      .text('RSI ( 14 )')

    let legendBox = this.legendLabel.node().getBBox()

    this.legendValue = this.svg.append('text')
      .attr('class', 'rsi legend')
      .attr('x', legendBox.x + legendBox.width + (CHART_INDICATOR_LABEL.padding * 2))
      .attr('y', this.indicatorLabelY)
      .text(FORMATS.DEC1(latestBar.rsi))
  }

  crosshairMove(currentBar) {
    this.legendValue.text(FORMATS.DEC1(currentBar.rsi))
  }

  crosshairOut(latestBar) {
    this.legendValue.text(FORMATS.DEC1(latestBar.rsi))
  }
}
