const rimraf = require('rimraf')

rimraf(`static/*`, {
  glob: {
    ignore: 'static/d3*.js',
  },
}, onError)

function onError(e) {
  if (!e) {
    console.log('Done cleaning static/ dir')
  } else {
    console.error(e)
  }
}
