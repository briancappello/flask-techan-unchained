import React, { useState, useEffect, useCallback } from 'react'
import { compose } from 'redux'
import { useSelector, useDispatch } from 'react-redux'

import injectSagas from 'utils/async/injectSagas'
import * as loadWatchlistSagas from 'finance/sagas/loadWatchlist'
import * as loadWatchlistsSagas from 'finance/sagas/loadWatchlists'

import { loadWatchlists, loadWatchlist } from 'finance/actions'
import { selectWatchlists, selectWatchlistComponents } from 'finance/selectors'

import Watchlist from '../Watchlist'
import './watchlists.scss'


const getSidebarListHeight = () => {
  const height = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0)
  const formHeight = 106 // unclear where this number comes from, as the form is only 48 high
  return height - formHeight
}

const Watchlists = ({ queryParams }) => {
  const dispatch = useDispatch()
  const watchlists = useSelector(selectWatchlists)
  const [watchlist, setWatchlist] = useState(undefined)
  const [sidebarListHeight, setSidebarListHeight] = useState(getSidebarListHeight())

  const currentWatchlistKey = watchlist || (watchlists.length > 0 ? watchlists[0].key : undefined)
  const currentWatchlistData = useSelector(state => {
    const components = selectWatchlistComponents(state)
    return currentWatchlistKey ? components[currentWatchlistKey] : undefined
  })

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
    if (currentWatchlistKey) {
      boundLoadWatchlist({ key: currentWatchlistKey })
    }
  }, [currentWatchlistKey, boundLoadWatchlist])

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
    setWatchlist(e.target.value)
  }

  if (!currentWatchlistKey || !currentWatchlistData) {
    return <p>Loading...</p>
  }

  const { label, components } = currentWatchlistData
  return (
    <div className="watchlists" style={{ height: sidebarListHeight }}>
      <form>
        <select onChange={onChange} value={currentWatchlistKey}>
          {watchlists.map((wl) => {
            return <option key={wl.key} value={wl.key}>{wl.label}</option>
          })}
        </select>
      </form>
      <Watchlist key={currentWatchlistKey}
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
