const {
  // debug levels in vertical order from least verbose to most
  CRITICAL,
  ERROR,
  WARNING,
  INFO,
  DEBUG,
} = require('constants')

const isProd = process.env.NODE_ENV === 'production'
const isTest = process.env.NODE_ENV === 'test'
const isDev = !(isProd || isTest)

const LOGGING_ENABLED = isDev
const LOG_LEVEL = DEBUG

const SERVER_URL = '' // set this if your API server is different from the frontend server

const SITE_NAME = 'Flask Techan Unchained'
const COPYRIGHT = 'Company Name'

module.exports = {
  LOGGING_ENABLED,
  LOG_LEVEL,
  SERVER_URL,
  SITE_NAME,
  COPYRIGHT,
}
