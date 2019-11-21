const API_VERSION = 'v1'
export const APP_VERSION = '1.0.0.0'
export const API_URL = process.env.NODE_ENV === 'development' ? `http://127.0.0.1:8000/api/${API_VERSION}` : `http://dev.com/api/${API_VERSION}`
