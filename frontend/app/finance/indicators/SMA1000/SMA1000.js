import techan from 'techanjs'

import './sma1000.scss'


export default class SMA1000 {
  init({ svg, xScale, yScale }) {
    this.svg = svg
    this.xScale = xScale
    this.yScale = yScale
  }

  draw(clipId) {
    this.sma1000 = techan.plot.sma()
      .xScale(this.xScale)
      .yScale(this.yScale)

    this.sma1000.accessor()
      .value((d) => d.sma1000)

    this.svg.append('g')
      .attr('class', 'plot-indicator ma sma1000')
      .attr('clip-path', `url(#${clipId})`)
  }

  drawChartData(data) {
    this.svg.select('g.plot-indicator.sma1000').datum(data).call(this.sma1000)
  }
}
