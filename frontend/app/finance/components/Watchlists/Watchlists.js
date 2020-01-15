import React from 'react'
import { bindActionCreators, compose } from 'redux'
import { connect } from 'react-redux'
import { push } from 'react-router-redux'

import { bindRoutineCreators } from 'actions'
import injectSagas from 'utils/async/injectSagas'

import { loadWatchlists, loadWatchlist } from 'finance/actions'
import { selectWatchlists, selectWatchlistComponents } from 'finance/selectors'

import Watchlist from '../Watchlist'
import './watchlists.scss'


class Watchlists extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      sidebarListHeight: this._getSidebarListHeight(),
    }
  }

  componentWillMount() {
    this.props.loadWatchlists.maybeTrigger()
  }

  componentWillReceiveProps(nextProps) {
    const { watchlists, loadWatchlist } = nextProps;
    const { watchlist } = this.state;
    if (watchlist === undefined && watchlists && watchlists.length) {
      const watchlist = watchlists[0].key
      loadWatchlist.maybeTrigger({ key: watchlist })
      this.setState({ watchlist })
    }
  }

  componentDidMount() {
    window.addEventListener('resize', this.handleResize)
  }

  handleResize = () => {
    this.setState({
      sidebarListHeight: this._getSidebarListHeight(),
    })
  }

  _getSidebarListHeight() {
    const height = Math.max(document.documentElement.clientHeight, window.innerHeight)
    const formHeight = 48
    const paddingTop = 10

    return height - (formHeight + paddingTop)
  }

  onChange = (e) => {
    e.preventDefault()
    this.props.loadWatchlist.maybeTrigger({ key: e.target.value })
    this.setState({ watchlist: e.target.value })
  }

  render() {
    const { watchlists, watchlistComponents, queryParams } = this.props
    const { watchlist, sidebarListHeight } = this.state
    if (!watchlist || !watchlistComponents || watchlistComponents[watchlist] === undefined) {
      return <p>Loading...</p>
    }

    const { label, components } = watchlistComponents[watchlist]
    return (
      <div className="watchlists" style={{ height: sidebarListHeight }}>
        <form>
          <select onChange={this.onChange} value={watchlist}>
            {watchlists.map((watchlist) => {
              return <option key={watchlist.key} value={watchlist.key}>{watchlist.label}</option>
            })}
          </select>
        </form>
        <Watchlist key={watchlist}
                   watchlist={label}
                   quotes={components}
                   queryParams={queryParams} />
      </div>
    )
  }
}

const withWatchlistSagas = injectSagas(require('finance/sagas/loadWatchlist'))
const withWatchlistsSagas = injectSagas(require('finance/sagas/loadWatchlists'))

const withConnect = connect(
  (state) => ({
    watchlistComponents: selectWatchlistComponents(state),
    watchlists: selectWatchlists(state),
  }),
  (dispatch) => ({
    ...bindActionCreators({ push }, dispatch),
    ...bindRoutineCreators({ loadWatchlist, loadWatchlists }, dispatch),
  })
)

export default compose(
  withWatchlistSagas,
  withWatchlistsSagas,
  withConnect,
)(Watchlists)
