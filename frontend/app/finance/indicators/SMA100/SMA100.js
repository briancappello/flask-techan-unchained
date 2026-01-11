import techan from 'techanjs'

import './sma100.scss'

export default class SMA100 {
  init({ svg, xScale, yScale }) {
    this.svg = svg
    this.xScale = xScale
    this.yScale = yScale
  }

  draw(clipId) {
    this.sma100 = techan.plot.sma().xScale(this.xScale).yScale(this.yScale)

    this.sma100.accessor().value((d) => d.sma100)

    this.svg
      .append('g')
      .attr('class', 'plot-indicator ma sma100')
      .attr('clip-path', `url(#${clipId})`)
  }

  drawChartData(data) {
    this.svg.select('g.plot-indicator.sma100').datum(data).call(this.sma100)
  }
}
