import ApiService from './api.service.js'

const AuthService = {
  login(payload) {
    return ApiService.post('token', payload)
  },
  verifty_token(payload) {
    return ApiService.post('token/verify', payload)
  },
  refresh_token(payload) {
    return ApiService.post('token/refresh', payload)
  }
}
export default AuthService
