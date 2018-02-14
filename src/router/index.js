import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import Login from '@/components/Login'
import SecurityQuestion from '@/components/SecurityQuestion'
import Accounts from '@/components/Accounts'
import Account from '@/components/Account'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/security-question',
      name: 'SecurityQuestion',
      component: SecurityQuestion
    },
    {
      path: '/accounts',
      name: 'Accounts',
      component: Accounts
    },
    {
      path: '/account/:branchCode/:accountNumber',
      name: 'Account',
      component: Account
    }
  ]
})
