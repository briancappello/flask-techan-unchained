import React from 'react'
import { connect } from 'react-redux'
import { parse } from 'query-string'

import ChartContainer from 'finance/components/ChartContainer'
import { FREQUENCY, LINEAR_SCALE, CANDLE_CHART } from 'finance/constants'


// https://stackoverflow.com/questions/105034/create-guid-uuid-in-javascript#answer-2117523
function uuid4() {
  return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
    (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
  )
}


const Chart = (props) => <ChartContainer {...props} />

Chart.defaultProps = {
  frequency: FREQUENCY.Daily,
  scale: LINEAR_SCALE,
  type: CANDLE_CHART,
}

export default connect(
  (state, props) => {
    const { ticker } = props.match.params
    const { frequency, datetime, scale, type } = parse(props.location.search)
    return { ticker, frequency, datetime, scale, type, id: uuid4() }
  },
)(Chart)
