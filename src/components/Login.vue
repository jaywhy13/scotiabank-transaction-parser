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

        <button type="button" class="btn btn-info" v-on:click="login">Login</button>
    </form>
</div>
</template>

<script>
import sendMessage from '../base'

export default {
  name: 'Login',
  data () {
    return {
      'accountNumber': null,
      'password': null
    }
  },
  methods: {
    login: function () {
      console.log('Logging in')
      const msg = {
        'messageType': 'login',
        'params': {
          'account_number': this.accountNumber,
          'password': this.password
        }
      }
      sendMessage(msg)
    }
  }
}
</script>

<style scoped>

</style>
