import React from 'react'
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'

import { PageContent } from 'components'
import { flashSuccess } from 'site/actions'

class Home extends React.Component {
  componentWillMount() {
    if (window.location.search.indexOf('welcome') > 0) {
      this.props.flashSuccess('Welcome!')
    }
  }

  render() {
    return (
      <PageContent>
        <h1>Welcome to Flask Techan Unchained!</h1>
        <p>A demo app integrating <a href="https://github.com/alpacahq/marketstore" target="_blank">Alpaca MarketStore</a> with Python/React. Built using <a href="https://github.com/briancappello/flask-unchained" target="_blank">Flask Unchained</a> and <a href="http://techanjs.org/" target="_blank">techan.js</a>.</p>
        <div className="row">
          <h2>License</h2>
          <p>Apache 2.0</p>
        </div>
      </PageContent>
    )
  }
}

export default connect(
  (state) => ({}),
  (dispatch) => bindActionCreators({ flashSuccess }, dispatch),
)(Home)
