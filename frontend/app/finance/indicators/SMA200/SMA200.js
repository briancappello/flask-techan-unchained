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

import './sma200.scss'


export default class SMA200 {
  init({ svg, xScale, yScale }) {
    this.svg = svg
    this.xScale = xScale
    this.yScale = yScale
  }

  draw(clipId) {
    this.sma200 = techan.plot.sma()
      .xScale(this.xScale)
      .yScale(this.yScale)

    this.sma200.accessor()
      .value((d) => d.sma200)

    this.svg.append('g')
      .attr('class', 'plot-indicator ma sma200')
      .attr('clip-path', `url(#${clipId})`)
  }

  drawChartData(data) {
    this.svg.select('g.plot-indicator.sma200').datum(data).call(this.sma200)
  }
}
