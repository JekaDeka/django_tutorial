import Vue from 'vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import JwtService from '@/api/jwt.service'
import {
  API_URL
} from '@/api/config'
import {
  notifier
} from '@/plugins/vue.notifications'

axios.interceptors.response.use(function(response) {
  return response
}, function(error) {
  if (error.response) {
    switch (error.response.status) {
      case 400:
        error.response.data.errors.forEach((error) => {
          notifier.warning(`${error.message}`)
        })
        break
      case 401:
        notifier.warning('Ошибка авторизации: Не удалось получить доступ к сервису.')
        break
      case 403:
        notifier.warning('Ошибка авторизации: Недостаточно прав.')
        break
      case 404:
        if (typeof (error.response.data) !== 'object') {
          notifier.warning(`${error.response.data}`)
        }
        break
      case 500:
        notifier.warning(
          'Внутренняя ошибка сервера. Обратитесь к администратору.'
        )
        break
      default:
        notifier.warning(
          'Неизвестная ошибка. Обратитесь к администратору.'
        )
        break
    }
  }
  return Promise.reject(error)
})

const ApiService = {
  init() {
    Vue.$log.debug('init api service')
    Vue.use(VueAxios, axios)
    Vue.axios.defaults.baseURL = API_URL
    Vue.axios.defaults.timeout = 15000
  },

  setHeader() {
    if (JwtService.getToken()) {
      Vue.$log.debug('init api service header token')
      Vue.axios.defaults.headers.common[
        'Authorization'
      ] = `Bearer ${JwtService.getToken()}`
    }
  },

  query(resource, params) {
    return Vue.axios.get(`${resource}/`, params)
  },

  get(resource, slug = '', extra_route = '') {
    const params = [`${resource}`, `${slug}`, `${extra_route}`]
    let url = params.join('/').replace(/\/\/$/, '/')
    url = url[url.length - 1] !== '/' ? url = url.concat('/') : url
    return Vue.axios.get(url)
  },
  get_file(resource, slug = '', extra_route = '') {
    const params = [`${resource}`, `${slug}`, `${extra_route}`]
    const url = params.join('/').replace(/\/\/$/, '/')
    return Vue.axios.get(url, {
      responseType: 'blob'
    })
  },
  update_extra_route(resource, slug, params, extra_route, config = {}) {
    return Vue.axios.put(`${resource}/${slug}/${extra_route}/`, params, config)
  },
  post_extra_route(resource, slug, params, extra_route, config = {}) {
    return Vue.axios.post(`${resource}/${slug}/${extra_route}/`, params, config)
  },
  post(resource, params, config = {}) {
    return Vue.axios.post(`${resource}/`, params, config)
  },
  put(resource, params, config = {}) {
    return Vue.axios.put(`${resource}/`, params, config)
  },
  update(resource, slug, params) {
    return Vue.axios.put(`${resource}/${slug}/`, params)
  },
  patch(resource, slug, params) {
    return Vue.axios.patch(`${resource}/${slug}/`, params)
  },
  delete(resource) {
    return Vue.axios.delete(resource).catch(error => {
      notifier.warning(JSON.stringify(error.response.data))
    })
  },
  get_app_version() {
    return Vue.axios.get('get_app_version/')
  }
}

export default ApiService
