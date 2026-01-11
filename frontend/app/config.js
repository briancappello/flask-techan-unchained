// Debug levels in vertical order from least verbose to most
export const CRITICAL = 50
export const ERROR = 40
export const WARNING = 30
export const INFO = 20
export const DEBUG = 10

export const isProd = import.meta.env.MODE === 'production'
export const isTest = import.meta.env.MODE === 'test'
export const isDev = !(isProd || isTest)

export const LOGGING_ENABLED = isDev
export const LOG_LEVEL = DEBUG

export const SERVER_URL = '' // set this if your API server is different from the frontend server

export const SITE_NAME = 'Flask Techan Unchained'
export const COPYRIGHT = 'Company Name'
