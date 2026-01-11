import React, { useState, useEffect, useCallback } from 'react'
import { compose } from 'redux'
import { useSelector, useDispatch } from 'react-redux'

import { bindRoutineCreators } from 'actions'
import injectSagas from 'utils/async/injectSagas'
import * as loadWatchlistSagas from 'finance/sagas/loadWatchlist'
import * as loadWatchlistsSagas from 'finance/sagas/loadWatchlists'

import { loadWatchlists, loadWatchlist } from 'finance/actions'
import { selectWatchlists, selectWatchlistComponents } from 'finance/selectors'

import Watchlist from '../Watchlist'
import './watchlists.scss'


const getSidebarListHeight = () => {
  const height = Math.max(document.documentElement.clientHeight, window.innerHeight)
  const formHeight = 48
  const paddingTop = 10
  return height - (formHeight + paddingTop)
}

const Watchlists = ({ queryParams }) => {
  const dispatch = useDispatch()
  const watchlists = useSelector(selectWatchlists)
  const watchlistComponents = useSelector(selectWatchlistComponents)

  const [watchlist, setWatchlist] = useState(undefined)
  const [sidebarListHeight, setSidebarListHeight] = useState(getSidebarListHeight())

  // Create bound action creators
  const boundLoadWatchlists = useCallback(
    () => dispatch(loadWatchlists.maybeTrigger ? loadWatchlists.maybeTrigger() : loadWatchlists.trigger()),
    [dispatch]
  )
  const boundLoadWatchlist = useCallback(
    (params) => dispatch(loadWatchlist.maybeTrigger ? loadWatchlist.maybeTrigger(params) : loadWatchlist.trigger(params)),
    [dispatch]
  )

  // Load watchlists on mount
  useEffect(() => {
    boundLoadWatchlists()
  }, [boundLoadWatchlists])

  // Load first watchlist when watchlists are available
  useEffect(() => {
    if (watchlist === undefined && watchlists && watchlists.length) {
      const firstWatchlist = watchlists[0].key
      boundLoadWatchlist({ key: firstWatchlist })
      setWatchlist(firstWatchlist)
    }
  }, [watchlists, watchlist, boundLoadWatchlist])

  // Handle resize
  useEffect(() => {
    const handleResize = () => {
      setSidebarListHeight(getSidebarListHeight())
    }
    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [])

  const onChange = (e) => {
    e.preventDefault()
    boundLoadWatchlist({ key: e.target.value })
    setWatchlist(e.target.value)
  }

  let currentWatchlist = watchlist
  // FIXME save current watchlist in query params?
  if (currentWatchlist === undefined && watchlists.length > 0) {
    currentWatchlist = watchlists[0].key
  }

  if (!currentWatchlist || !watchlistComponents || watchlistComponents[currentWatchlist] === undefined) {
    return <p>Loading...</p>
  }

  const { label, components } = watchlistComponents[currentWatchlist]
  return (
    <div className="watchlists" style={{ height: sidebarListHeight }}>
      <form>
        <select onChange={onChange} value={currentWatchlist}>
          {watchlists.map((wl) => {
            return <option key={wl.key} value={wl.key}>{wl.label}</option>
          })}
        </select>
      </form>
      <Watchlist key={currentWatchlist}
                 watchlist={label}
                 quotes={components}
                 queryParams={queryParams} />
    </div>
  )
}

const withWatchlistSagas = injectSagas(loadWatchlistSagas)
const withWatchlistsSagas = injectSagas(loadWatchlistsSagas)

export default compose(
  withWatchlistSagas,
  withWatchlistsSagas,
)(Watchlists)
