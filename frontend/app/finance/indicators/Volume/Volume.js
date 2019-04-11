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
