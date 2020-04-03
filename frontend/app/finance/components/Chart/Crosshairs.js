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

import { FORMATS } from 'finance/constants'


export default class Crosshairs {
  init({ svg, xAxis, yAxis, yAxisRight, chartHeight }) {
    this.svg = svg
    this.xAxis = xAxis
    this.yAxis = yAxis
    this.yAxisRight = yAxisRight
    this.chartHeight = chartHeight
  }

  draw() {
    // crosshair current date label
    this.dateAnnotation = techan.plot.axisannotation()
      .axis(this.xAxis)
      .orient('bottom')
      .format(FORMATS.DATE)
      .width(75)
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

    // plot crosshairs
    this.plotCrosshair = techan.plot.crosshair()
      .xScale(this.xScale)
      .yScale(this.yScale)
      .xAnnotation([this.dateAnnotation])
      .yAnnotation(yAnnotations)
      .verticalWireRange([0, this.chartHeight])
      .on('move', this.crosshairMove)
      .on('out', this.crosshairOut)

    // add crosshair group container to the svg
    this.svg.append('g')
      .attr('class', 'plot crosshair')

    // this serves as an index lookup for mouse events (to get the current bar)
    this.dataIndexScale = d3.scaleLinear()
      .domain([0, this.state.visibleBars])
      .range([0, this.chartWidth])

  }

  initIndicators(indicators) {
    if (!indicators) {
      return
    }

    for (let indicator of indicators) {

      indicator.drawCrosshairs()
        .xAnnotation([this.dateAnnotation])
        .verticalWireRange([0, this.chartHeight])
        .on('move', this.crosshairMove)
        .on('out', this.crosshairOut)
    }
  }
}
