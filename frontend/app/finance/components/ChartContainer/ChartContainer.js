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
    datetime: '',
    scale: LINEAR_SCALE,
    type: CANDLE_CHART,
  }

  constructor(props) {
    super(props)
    const { datetime } = props
    this.state = {
      ticker: '',
      datetime: datetime,
    }
  }

  componentWillMount() {
    const { loadTickerHistory, ticker, frequency, datetime } = this.props
    loadTickerHistory.maybeTrigger({ ticker, frequency, datetime })
  }

  componentWillReceiveProps(nextProps) {
    const { loadTickerHistory, ticker: prevTicker, frequency: prevFrequency, datetime: prevDatetime } = this.props
    const { ticker, frequency, datetime } = nextProps

    if (prevTicker !== ticker || prevFrequency !== frequency || prevDatetime !== datetime) {
      loadTickerHistory.maybeTrigger({ ticker, frequency, datetime })
      this.setState({ ticker: '', datetime: datetime })
    }
  }

  componentDidMount() {
    window.addEventListener('keydown', (e) => {
      switch (e.key) {
        case "ArrowLeft":
          break
        case "ArrowRight":
          break
        case "ArrowUp":
          break
        case "ArrowDown":
          break
      }
      console.log(`keydown event listener: ${e.key}`)
    })
  }

  onClick = (key, value) => {
    const { ticker, frequency, datetime, scale, type } = this.props
    const args = { ticker, frequency, datetime, scale, type }
    args[key] = value
    this.pushNewUrl(args)
  }

  onSubmit = (e) => {
    e.preventDefault()
    const { ticker: currentTicker } = this.props
    const { ticker, datetime } = this.state
    const { frequency, scale, type } = this.props
    this.pushNewUrl({ ticker: ticker && ticker || currentTicker, datetime, frequency, scale, type })
  }

  pushNewUrl({ ticker, ...queryParams }) {
    queryParams = this._filterQueryParams(queryParams)
    this.props.push({
      pathname: ROUTE_MAP[ROUTES.Chart].toPath({ ticker: ticker.toUpperCase() }),
      search: Object.keys(queryParams).length ? `?${stringify(queryParams)}` : '',
    })
  }

  _filterQueryParams(queryParams) {
    ['frequency', 'scale', 'type', 'datetime'].forEach(paramName => {
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
    const { id, ticker, datetime, history, frequency, scale, type } = this.props

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
                   autoFocus={true}
                   onChange={(e) => this.setState({ ticker: e.target.value })}
            />
            <input type="text"
                   placeholder="Datetime"
                   value={this.state.datetime}
                   onChange={(e) => this.setState({ datetime: e.target.value })}
            />
            <input type="submit" style={{ display: "none" }} />
          </form>
          <Watchlists queryParams={this._filterQueryParams({ frequency, datetime, scale, type })} />
        </aside>
      </div>
    )
  }
}

const withHistoryReducer = injectReducer(require('finance/reducers/loadTickerHistory'))
const withHistorySagas = injectSagas(require('finance/sagas/loadTickerHistory'))

const withConnect = connect(
  (state, props) => {
    const { ticker, frequency, datetime } = props
    return {
      history: selectHistoryByTicker(state, ticker, frequency, datetime),
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
