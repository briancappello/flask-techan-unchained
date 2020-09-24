import techan from 'techan'

import { FORMATS, CHART_INDICATOR_LABEL } from 'finance/constants'

import './stochastics.scss'


export default class Stochastics {
  init({ svg, xScale, yScale, frequency }) {
    this.svg = svg
    this.xScale = xScale
    this.yScale = yScale
    this.frequency = frequency
    this.chartWidth = this.xScale.range()[1]
    this.indicatorHeight = this.yScale.range()[0] - this.yScale.range()[1]
    this.indicatorY = this.yScale.range()[1]
    this.indicatorLabelY = this.indicatorY - CHART_INDICATOR_LABEL.padding
  }

  draw() {
    this.xGrid = d3.axisBottom(this.xScale)
      .ticks(this.frequency)
      .tickFormat(() => null)
      .tickSizeInner(this.indicatorHeight)
      .tickSizeOuter(this.indicatorHeight)

    this.svg.append('g')
      .attr('class', 'stochastic x grid')
      .attr('transform', `translate(0, ${this.indicatorY})`)

    this.yAxisLeft = d3.axisLeft(this.yScale)
      .ticks(5)
      .tickSizeOuter(-this.chartWidth)

    this.svg.append('g')
      .attr('class', 'stochastic axis')

    this.yAxisRight = d3.axisRight(this.yScale)
      .ticks(5)

    this.svg.append('g')
      .attr('class', 'stochastic axis right')
      .attr('transform', `translate(${this.chartWidth}, 0)`)

    this.accessor = techan.accessor.stochastic()
      .stochasticK((d) => d.stoch_k)
      .stochasticD((d) => d.stoch_d)

    this.stochastics = techan.plot.stochastic()
      .xScale(this.xScale)
      .yScale(this.yScale)
      .accessor(this.accessor)

    this.svg.append('g')
      .attr('class', 'indicator stochastic')
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
      .attr('class', 'stochastic crosshair')

    return this.crosshair
  }

  connectCrosshairs() {
    this.svg.select('g.stochastic.crosshair').call(this.crosshair)
  }

  drawChartData(data) {
    this.svg.select('g.stochastic.x.grid').call(this.xGrid)
    this.svg.select('g.stochastic.axis').call(this.yAxisLeft)
    this.svg.select('g.stochastic.axis.right').call(this.yAxisRight)
    this.svg.select('g.stochastic.indicator').datum(data).call(this.stochastics)
  }

  drawLegend(latestBar) {
    this.legendLabel = this.svg.append('text')
      .attr('class', 'stochastic legend label')
      .attr('x', CHART_INDICATOR_LABEL.padding)
      .attr('y', this.indicatorLabelY)
      .text('STOCHASTICS ( 14, 3, 3 )')

    let legendBox = this.legendLabel.node().getBBox()

    this.legendKValue = this.svg.append('text')
      .attr('class', 'stochastic legend k')
      .attr('x', legendBox.x + legendBox.width + (CHART_INDICATOR_LABEL.padding * 2))
      .attr('y', this.indicatorLabelY)
      .text(FORMATS.DEC1(latestBar.stoch_k))

    legendBox = this.legendKValue.node().getBBox()

    this.legendDValue = this.svg.append('text')
      .attr('class', 'stochastic legend d')
      .attr('x', legendBox.x + legendBox.width + (CHART_INDICATOR_LABEL.padding * 2))
      .attr('y', this.indicatorLabelY)
      .text(FORMATS.DEC1(latestBar.stoch_d))
  }

  crosshairMove(currentBar) {
    this.legendKValue.text(FORMATS.DEC1(currentBar.stoch_k))
    this.legendDValue.text(FORMATS.DEC1(currentBar.stoch_d))
  }

  crosshairOut(latestBar) {
    this.legendKValue.text(FORMATS.DEC1(latestBar.stoch_k))
    this.legendDValue.text(FORMATS.DEC1(latestBar.stoch_d))
  }
}
