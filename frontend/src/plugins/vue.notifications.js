import Vue from 'vue'
import AWN from 'awesome-notifications'
import VueAWN from 'vue-awesome-notifications'
require('vue-awesome-notifications/dist/styles/style.css')

const options = {
  durations: {
    global: 5000

  },
  animationDuration: 250,
  maxNotifications: 7,
  position: 'top-right',
  labels: {
    tip: 'Подсказка',
    info: 'Уведомление',
    warning: 'Внимание',
    success: 'Сохранено',
    async: 'Загрузка...'
  }
}
Vue.use(VueAWN, options)

export const notifier = new AWN(options)
