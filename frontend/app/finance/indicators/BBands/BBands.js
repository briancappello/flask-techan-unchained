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
