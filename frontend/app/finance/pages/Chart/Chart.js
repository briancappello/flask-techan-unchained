import React from 'react'
import { useParams, useLocation } from 'react-router-dom'
import { parse } from 'query-string'

import ChartContainer from 'finance/components/ChartContainer'
import { FREQUENCY, LINEAR_SCALE, CANDLE_CHART } from 'finance/constants'

// https://stackoverflow.com/questions/105034/create-guid-uuid-in-javascript#answer-2117523
function uuid4() {
  return ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, (c) =>
    (c ^ (crypto.getRandomValues(new Uint8Array(1))[0] & (15 >> (c / 4)))).toString(16),
  )
}

const Chart = ({
  frequency: defaultFrequency = FREQUENCY.Daily,
  scale: defaultScale = LINEAR_SCALE,
  type: defaultType = CANDLE_CHART,
  datetime: defaultDatetime,
  barWidth: defaultBarWidth = 10,
  ...props
}) => {
  const { ticker } = useParams()
  const { search } = useLocation()
  const queryParams = parse(search)

  const frequency = queryParams.frequency || defaultFrequency
  const datetime = queryParams.datetime || defaultDatetime
  const scale = queryParams.scale || defaultScale
  const type = queryParams.type || defaultType
  const barWidth = queryParams.barWidth
    ? parseFloat(queryParams.barWidth)
    : defaultBarWidth

  return (
    <ChartContainer
      {...props}
      ticker={ticker}
      frequency={frequency}
      datetime={datetime}
      scale={scale}
      type={type}
      barWidth={barWidth}
      id={uuid4()}
    />
  )
}

export default Chart
