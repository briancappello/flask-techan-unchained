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

import './bbands.scss'


export default class BBands {
  init({ svg, xScale, yScale }) {
    this.svg = svg
    this.xScale = xScale
    this.yScale = yScale
  }

  draw(clipId) {
    this.accessor = techan.accessor.bollinger()
      .upper((d) => d.bbands_upper)
      .lower((d) => Math.max(0.01, d.bbands_lower))

    this.bbands = techan.plot.bollinger()
      .xScale(this.xScale)
      .yScale(this.yScale)
      .accessor(this.accessor)

    this.svg.append('g')
      .attr('class', 'plot-indicator bbands')
      .attr('clip-path', `url(#${clipId})`)
  }

  drawChartData(data) {
    this.svg.select('g.plot-indicator.bbands').datum(data).call(this.bbands)
  }
}
