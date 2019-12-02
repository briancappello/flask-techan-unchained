import React from 'react'
import Helmet from 'react-helmet'
import { bindActionCreators, compose } from 'redux'
import { connect } from 'react-redux'
import { push } from 'react-router-redux'
import { stringify } from 'query-string'
import classnames from 'classnames'

import { bindRoutineCreators } from 'actions'
import { ROUTES, ROUTE_MAP } from 'routes'
import injectSagas from 'utils/async/injectSagas'
import injectReducer from 'utils/async/injectReducer'

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


class ChartContainer extends React.Component {

  static defaultProps = {
    frequency: FREQUENCY.Daily,
    scale: LINEAR_SCALE,
    type: CANDLE_CHART,
  }

  constructor(props) {
    super(props)
    this.state = {
      ticker: '',
    }
  }

  componentWillMount() {
    const { loadTickerHistory, ticker, frequency } = this.props
    loadTickerHistory.maybeTrigger({ ticker, frequency })
  }

  componentWillReceiveProps(nextProps) {
    const { loadTickerHistory, ticker: prevTicker, frequency: prevFrequency } = this.props
    const { ticker, frequency } = nextProps

    if (prevTicker !== ticker || prevFrequency !== frequency) {
      loadTickerHistory.maybeTrigger({ ticker, frequency })
      this.setState({ ticker: '' })
    }
  }

  onClick = (key, value) => {
    const { ticker, frequency, scale, type } = this.props
    const args = { ticker, frequency, scale, type }
    args[key] = value
    this.pushNewUrl(args)
  }

  onSubmit = (e) => {
    e.preventDefault()
    const { ticker } = this.state
    const { frequency, scale, type } = this.props
    this.pushNewUrl({ ticker, frequency, scale, type })
  }

  pushNewUrl({ ticker, ...queryParams }) {
    queryParams = this._filterQueryParams(queryParams)
    this.props.push({
      pathname: ROUTE_MAP[ROUTES.Chart].toPath({ ticker: ticker.toUpperCase() }),
      search: Object.keys(queryParams).length ? `?${stringify(queryParams)}` : '',
    })
  }

  _filterQueryParams(queryParams) {
    ['frequency', 'scale', 'type'].forEach(paramName => {
      if (queryParams[paramName] == ChartContainer.defaultProps[paramName]) {
        delete queryParams[paramName]
      }
    })
    return queryParams
  }

  renderButton(key, value, label) {
    const active = value === this.props[key]
    return (
      <button onClick={() => this.onClick(key, value)}
              className={classnames({ active })}
      >
        {label}
      </button>
    )
  }

  render() {
    const { id, ticker, history, frequency, scale, type } = this.props

    return (
      <div className="chart-container-wrap">
        <Helmet>
          <title>{ticker}</title>
        </Helmet>
        <div className="chart-container">
          <div className="chart-controls">
            <div className="row frequencies">
              {this.renderButton('frequency', FREQUENCY.Minutely, '1m')}
              {this.renderButton('frequency', FREQUENCY.FiveMinutely, '5m')}
              {this.renderButton('frequency', FREQUENCY.TenMinutely, '10m')}
              {this.renderButton('frequency', FREQUENCY.FifteenMinutely, '15m')}
              {this.renderButton('frequency', FREQUENCY.ThirtyMinutely, '30m')}
              {this.renderButton('frequency', FREQUENCY.Hourly, '1hr')}
              {this.renderButton('frequency', FREQUENCY.Daily, 'D')}
              {this.renderButton('frequency', FREQUENCY.Weekly, 'W')}
              {this.renderButton('frequency', FREQUENCY.Monthly, 'M')}
              {this.renderButton('frequency', FREQUENCY.Yearly, 'Y')}
            </div>
            <div className="row chart-types">
              {this.renderButton('type', BAR_CHART, 'Bar')}
              {this.renderButton('type', CANDLE_CHART, 'Candle')}
              {this.renderButton('type', LINE_CHART, 'Line')}
            </div>
            <div className="row chart-scales">
              {this.renderButton('scale', LINEAR_SCALE, 'Linear')}
              {this.renderButton('scale', LOG_SCALE, 'Log')}
            </div>
          </div>
          <Chart id={id} data={history} ticker={ticker} frequency={frequency} scale={scale} type={type} />
        </div>
        <aside className="sidebar">
          <form onSubmit={this.onSubmit}>
            <input type="text"
                   placeholder="Ticker Symbol"
                   value={this.state.ticker}
                   onChange={(e) => this.setState({ ticker: e.target.value })}
            />
          </form>
          <Watchlists queryParams={this._filterQueryParams({ frequency, scale, type })} />
        </aside>
      </div>
    )
  }
}

const withHistoryReducer = injectReducer(require('finance/reducers/loadTickerHistory'))
const withHistorySagas = injectSagas(require('finance/sagas/loadTickerHistory'))

const withConnect = connect(
  (state, props) => {
    const { ticker, frequency } = props
    return {
      history: selectHistoryByTicker(state, ticker, frequency),
    }
  },
  (dispatch) => ({
    ...bindActionCreators({ push }, dispatch),
    ...bindRoutineCreators({ loadTickerHistory }, dispatch),
  }),
)

export default compose(
  withHistoryReducer,
  withHistorySagas,
  withConnect,
)(ChartContainer)
