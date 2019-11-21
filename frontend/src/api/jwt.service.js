const ID_TOKEN_KEY = 'token'
const APP_VERSION = 'version'

export const getToken = () => {
  return localStorage.getItem(ID_TOKEN_KEY)
}

export const saveToken = token => {
  localStorage.setItem(ID_TOKEN_KEY, token)
}

export const destroyToken = () => {
  localStorage.removeItem(ID_TOKEN_KEY)
}

export const getAppVersion = () => {
  return localStorage.getItem(APP_VERSION)
}

export const saveAppVersion = id => {
  localStorage.setItem(APP_VERSION, id)
}

export const destroyAppVersion = () => {
  localStorage.removeItem(APP_VERSION)
}

export default {
  getToken,
  saveToken,
  destroyToken,
  getAppVersion,
  saveAppVersion,
  destroyAppVersion
}
