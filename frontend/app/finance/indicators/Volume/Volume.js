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

import './volume.scss'


export default class Volume {
  init({ svg, xScale, yScale, priceChart }) {
    this.svg = svg
    this.xScale = xScale
    this.yScale = yScale
    this.priceChart = priceChart

    let [y0, y1] = yScale.range()
    this.plotHeight = Math.abs(y0 - y1)
  }

  draw() {
    this.volumeScale = d3.scaleLinear()
      .range([this.plotHeight, this.plotHeight * 0.8])

    // volume axis is invisible, but used by crosshair annotations to show volume values on hover
    this.volumeAxis = d3.axisRight(this.volumeScale)
      .tickFormat(() => null)
      .tickSizeOuter(0)

    this.svg.append('g')
      .attr('class', 'volume axis')

    this.volumePlot = techan.plot.volume()
      .accessor(this.priceChart.accessor())  // for determining whether up or down bar
      .xScale(this.xScale)
      .yScale(this.volumeScale)

    this.svg.append('g')
      .attr('class', 'volumePlot')
  }

  getCrosshairsYAnnotation() {
    return techan.plot.axisannotation()
      .axis(this.volumeAxis)
      .orient('right')
      .width(32)
      .format(FORMATS.SI)
  }

  drawChartData(data) {
    this.volumeScale.domain(techan.scale.plot.volume(data).domain()).nice()
    this.svg.select('g.volume.axis').call(this.volumeAxis)
    this.svg.select('g.volumePlot').datum(data).call(this.volumePlot)
  }
}
