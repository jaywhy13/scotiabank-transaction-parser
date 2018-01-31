import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/Login'
import SecurityQuestion from '@/components/SecurityQuestion'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Login',
      component: Login
    },
    {
      path: '/security-question',
      name: 'SecurityQuestion',
      component: SecurityQuestion
    }
  ]
})
