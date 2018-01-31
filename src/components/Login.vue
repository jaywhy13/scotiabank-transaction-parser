<template>
<div class="row">
    <div class="alert alert-danger" v-if="loginError" v-text="loginError">Had an isse
    </div>

    <form action="">
        <div class="form-group">
            <label for="account_number">Account Number</label>
            <input type="text" name="account_number" id="account_number" class="form-control" value="" required="required" placeholder="Account Number" v-model="accountNumber">
        </div>

        <div class="form-group">
            <label for="password">Password</label>
            <input type="password" name="" id="password" class="form-control" required="required" title="" placeholder="Password" v-model="password">
        </div>

        <button type="button" class="btn btn-info" v-on:click="login" v-bind:disabled="loggingIn">
          <i class="fas fa-circle-notch fa-spin" v-if="loggingIn"></i>
          Login
        </button>
    </form>
</div>
</template>

<script>
import { sendMessage, setupSocket } from '../base'

export default {
  name: 'Login',
  data () {
    return {
      'accountNumber': null,
      'password': null,
      'loginError': null,
      'loggingIn': false
    }
  },
  mounted: function () {
    this.accountNumber = window.localStorage.getItem('accountNumber')
    setupSocket(this)
    this.$on('socketMessage', function (data) {
      this.socketMessage(data)
    })
  },
  methods: {
    login: function () {
      this.loggingIn = true
      this.loginError = null
      console.log('Logging in')
      const msg = {
        'messageType': 'login',
        'params': {
          'account_number': this.accountNumber,
          'password': this.password
        }
      }
      window.localStorage.setItem('accountNumber', this.accountNumber)
      sendMessage(msg)
    },
    socketMessage: function (data) {
      var messageType = data.messageType
      if (messageType === 'login-failed') {
        this.loggingIn = false
        console.log('Setting message to', data.params.message)
        this.loginError = data.params.message
      } else if (messageType === 'login-success') {
        this.$router.push('/security-question')
      }
    }
  }
}
</script>

<style scoped>

</style>
