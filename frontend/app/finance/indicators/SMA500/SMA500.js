import techan from 'techan'

import './sma500.scss'


export default class SMA500 {
  init({ svg, xScale, yScale }) {
    this.svg = svg
    this.xScale = xScale
    this.yScale = yScale
  }

  draw(clipId) {
    this.sma500 = techan.plot.sma()
      .xScale(this.xScale)
      .yScale(this.yScale)

    this.sma500.accessor()
      .value((d) => d.sma500)

    this.svg.append('g')
      .attr('class', 'plot-indicator ma sma500')
      .attr('clip-path', `url(#${clipId})`)
  }

  drawChartData(data) {
    this.svg.select('g.plot-indicator.sma500').datum(data).call(this.sma500)
  }
}
