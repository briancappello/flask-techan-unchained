import techan from 'techanjs'

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
