import React, { useState, useEffect, useCallback } from 'react'
import { Helmet } from 'react-helmet-async'
import { compose } from 'redux'
import { useSelector, useDispatch } from 'react-redux'
import { push } from 'redux-first-history'
import { stringify } from 'query-string'
import classnames from 'classnames'

import { ROUTES, ROUTE_MAP } from 'routes'
import injectSagas from 'utils/async/injectSagas'
import injectReducer from 'utils/async/injectReducer'
import * as loadTickerHistoryReducer from 'finance/reducers/loadTickerHistory'
import * as loadTickerHistorySagas from 'finance/sagas/loadTickerHistory'

import { loadTickerHistory } from 'finance/actions'
import {
  BAR_CHART,
  CANDLE_CHART,
  LINE_CHART,
  LINEAR_SCALE,
  LOG_SCALE,
  FREQUENCY,
} from 'finance/constants'
import { selectHistoryByTicker } from 'finance/reducers/loadTickerHistory'
import Chart from 'finance/components/Chart'
import Watchlists from 'finance/components/Watchlists'

import './chart-container.scss'

const DEFAULT_PROPS = {
  frequency: FREQUENCY.Daily,
  datetime: '',
  scale: LINEAR_SCALE,
  type: CANDLE_CHART,
  barWidth: 3,
}

const filterQueryParams = (queryParams) => {
  const filtered = { ...queryParams }
  ;['frequency', 'scale', 'type', 'datetime', 'barWidth'].forEach((paramName) => {
    if (filtered[paramName] === DEFAULT_PROPS[paramName]) {
      delete filtered[paramName]
    }
  })
  return filtered
}

const ChartContainer = ({
  id,
  ticker,
  frequency = DEFAULT_PROPS.frequency,
  datetime: initialDatetime = DEFAULT_PROPS.datetime,
  scale = DEFAULT_PROPS.scale,
  type = DEFAULT_PROPS.type,
  barWidth = DEFAULT_PROPS.barWidth,
}) => {
  const dispatch = useDispatch()
  const [tickerInput, setTickerInput] = useState('')
  const [datetimeInput, setDatetimeInput] = useState(initialDatetime)

  const history = useSelector((state) =>
    selectHistoryByTicker(state, ticker, frequency, initialDatetime),
  )

  // Load ticker history when props change
  useEffect(() => {
    dispatch(
      loadTickerHistory.trigger({ ticker, frequency, datetime: initialDatetime }),
    )
    setTickerInput('')
    setDatetimeInput(initialDatetime)
  }, [ticker, frequency, initialDatetime, dispatch])

  // Handle keydown events
  useEffect(() => {
    const handleKeyDown = (e) => {
      switch (e.key) {
        case 'ArrowLeft':
        case 'ArrowRight':
        case 'ArrowUp':
        case 'ArrowDown':
          break
      }
      console.log(`keydown event listener: ${e.key}`)
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [])

  const pushNewUrl = useCallback(
    ({ ticker: newTicker, ...queryParams }) => {
      const filteredParams = filterQueryParams(queryParams)
      dispatch(
        push({
          pathname: ROUTE_MAP[ROUTES.Chart].toPath({ ticker: newTicker.toUpperCase() }),
          search: Object.keys(filteredParams).length
            ? `?${stringify(filteredParams)}`
            : '',
        }),
      )
    },
    [dispatch],
  )

  const onClick = useCallback(
    (key, value) => {
      const args = {
        ticker,
        frequency,
        datetime: initialDatetime,
        scale,
        type,
        barWidth,
      }
      args[key] = value
      pushNewUrl(args)
    },
    [ticker, frequency, initialDatetime, scale, type, barWidth, pushNewUrl],
  )

  const onSubmit = useCallback(
    (e) => {
      e.preventDefault()
      pushNewUrl({
        ticker: tickerInput || ticker,
        datetime: datetimeInput,
        frequency,
        scale,
        type,
        barWidth,
      })
    },
    [tickerInput, ticker, datetimeInput, frequency, scale, type, barWidth, pushNewUrl],
  )

  const onZoom = useCallback(
    (delta) => {
      const newWidth = Math.max(0.1, barWidth + delta)
      onClick('barWidth', newWidth.toFixed(1))
    },
    [barWidth, onClick],
  )

  const renderButton = (key, value, label) => {
    const currentValue = { frequency, scale, type }[key]
    const active = value === currentValue
    return (
      <button onClick={() => onClick(key, value)} className={classnames({ active })}>
        {label}
      </button>
    )
  }

  return (
    <div className="chart-container-wrap">
      <Helmet>
        <title>{ticker}</title>
      </Helmet>
      <div className="chart-container">
        <div className="chart-controls">
          <div className="row frequencies">
            {renderButton('frequency', FREQUENCY.Minutely, '1m')}
            {renderButton('frequency', FREQUENCY.FiveMinutely, '5m')}
            {renderButton('frequency', FREQUENCY.TenMinutely, '10m')}
            {renderButton('frequency', FREQUENCY.FifteenMinutely, '15m')}
            {renderButton('frequency', FREQUENCY.ThirtyMinutely, '30m')}
            {renderButton('frequency', FREQUENCY.Hourly, '1hr')}
            {renderButton('frequency', FREQUENCY.Daily, 'D')}
            {renderButton('frequency', FREQUENCY.Weekly, 'W')}
            {renderButton('frequency', FREQUENCY.Monthly, 'M')}
            {renderButton('frequency', FREQUENCY.Yearly, 'Y')}
          </div>
          <div className="row chart-types">
            {renderButton('type', BAR_CHART, 'Bar')}
            {renderButton('type', CANDLE_CHART, 'Candle')}
            {renderButton('type', LINE_CHART, 'Line')}
          </div>
          <div className="row chart-scales">
            {renderButton('scale', LINEAR_SCALE, 'Linear')}
            {renderButton('scale', LOG_SCALE, 'Log')}
          </div>
        </div>
        <div className="chart-controls zoom-controls">
          <div className="row">
            <button className="plus" onClick={() => onZoom(0.1)}>+</button>
          </div>
          <div className="row">
            <button className="minus" onClick={() => onZoom(-0.1)}>-</button>
          </div>
        </div>
        <Chart
          id={id}
          data={history}
          ticker={ticker}
          frequency={frequency}
          scale={scale}
          type={type}
          barWidth={barWidth}
        />
      </div>
      <aside className="sidebar">
        <form onSubmit={onSubmit}>
          <input
            type="text"
            placeholder="Ticker Symbol"
            value={tickerInput}
            autoFocus={true}
            onChange={(e) => setTickerInput(e.target.value)}
          />
          <input
            type="text"
            placeholder="Datetime"
            value={datetimeInput}
            onChange={(e) => setDatetimeInput(e.target.value)}
          />
          <input type="submit" style={{ display: 'none' }} />
        </form>
        <Watchlists
          queryParams={filterQueryParams({
            frequency,
            datetime: initialDatetime,
            scale,
            type,
            barWidth,
          })}
        />
      </aside>
    </div>
  )
}

const withHistoryReducer = injectReducer(loadTickerHistoryReducer)
const withHistorySagas = injectSagas(loadTickerHistorySagas)

export default compose(withHistoryReducer, withHistorySagas)(ChartContainer)
