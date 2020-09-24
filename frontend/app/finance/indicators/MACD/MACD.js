import techan from 'techan'

import { FORMATS, CHART_INDICATOR_LABEL } from 'finance/constants'

import './MACD.scss'


export default class MACD {
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
      .attr('class', 'macd x grid')
      .attr('transform', `translate(0, ${this.indicatorY})`)

    // axes
    this.yAxisLeft = d3.axisLeft(this.yScale)
      .ticks(5)
      .tickSizeOuter(-this.chartWidth)

    this.svg.append('g')
      .attr('class', 'macd axis')

    this.yAxisRight = d3.axisRight(this.yScale)
      .ticks(5)
      .tickSizeOuter(0)

    this.svg.append('g')
      .attr('class', 'macd axis right')
      .attr('transform', `translate(${this.chartWidth}, 0)`)

    // indicator
    this.accessor = techan.accessor.macd()
      .macd((d) => d.macd)
      .signal((d) => d.macd_signal)

    this.macd = techan.plot.macd()
      .xScale(this.xScale)
      .yScale(this.yScale)
      .accessor(this.accessor)

    this.svg.append('g')
      .attr('class', 'indicator macd')
  }

  drawCrosshairs() {
    this.yAnnotationLeft = techan.plot.axisannotation()
      .axis(this.yAxisLeft)
      .orient('left')
      .format(FORMATS.DEC)

    this.yAnnotationRight = techan.plot.axisannotation()
      .axis(this.yAxisRight)
      .orient('right')
      .translate([this.chartWidth, 0])
      .format(FORMATS.DEC)

    this.crosshair = techan.plot.crosshair()
      .xScale(this.xScale)
      .yScale(this.yScale)
      .yAnnotation([this.yAnnotationLeft, this.yAnnotationRight])

    this.svg.append('g')
      .attr('class', 'macd crosshair')

    return this.crosshair
  }

  connectCrosshairs() {
    this.svg.select('g.macd.crosshair').call(this.crosshair)
  }

  drawChartData(data) {
    const yDomain = techan.scale.plot.macd(data, this.accessor).domain()
    if (yDomain[0] > 0) {
      yDomain[0] = 0
    } else if (yDomain[1] < 0) {
      yDomain[1] = 0
    }
    this.yScale.domain(yDomain).nice()
    this.svg.select('g.macd.x.grid').call(this.xGrid)
    this.svg.select('g.macd.axis').call(this.yAxisLeft)
    this.svg.select('g.macd.axis.right').call(this.yAxisRight)
    this.svg.select('g.macd.indicator').datum(data).call(this.macd)
  }

  drawLegend(latestBar) {
    this.legendLabel = this.svg.append('text')
      .attr('x', CHART_INDICATOR_LABEL.padding)
      .attr('y', this.indicatorLabelY)
      .text('MACD ( 12, 26, 9 )')

    let legendBox = this.legendLabel.node().getBBox()

    this.legendValue = this.svg.append('text')
      .attr('class', 'macd legend value')
      .attr('x', legendBox.x + legendBox.width + (CHART_INDICATOR_LABEL.padding * 2))
      .attr('y', this.indicatorLabelY)
      .text(FORMATS.DEC(latestBar.macd))

    legendBox = this.legendValue.node().getBBox()

    this.legendSignalValue = this.svg.append('text')
      .attr('class', 'macd legend signal')
      .attr('x', legendBox.x + legendBox.width + (CHART_INDICATOR_LABEL.padding * 2))
      .attr('y', this.indicatorLabelY)
      .text(FORMATS.DEC(latestBar.macd_signal))
  }

  crosshairMove(currentBar) {
    this.legendValue.text(FORMATS.DEC(currentBar.macd))
    this.legendSignalValue.text(FORMATS.DEC(currentBar.macd_signal))
  }

  crosshairOut(latestBar) {
    this.legendValue.text(FORMATS.DEC(latestBar.macd))
    this.legendSignalValue.text(FORMATS.DEC(latestBar.macd_signal))
  }
}
