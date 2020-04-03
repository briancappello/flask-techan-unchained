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

import techan from 'techan'

import { FORMATS, CHART_INDICATOR_LABEL } from 'finance/constants'

import './stochastics.scss'


export default class Stochastics {
  init({ svg, xScale, yScale }) {
    this.svg = svg
    this.xScale = xScale
    this.yScale = yScale
    this.chartWidth = this.xScale.range()[1]
    this.indicatorLabelY = this.yScale.range()[1] - CHART_INDICATOR_LABEL.padding
  }

  draw() {
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
