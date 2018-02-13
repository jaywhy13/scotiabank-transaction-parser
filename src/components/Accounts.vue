<template>
    <div class="row">
        <table class="table table-hover">
            <thead>
                <tr>
                    <th>Account</th>
                    <th>Balance</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="account in accounts" v-bind:key="account.name">
                    <td v-text="account.name"></td>
                    <td v-text="account.balance"></td>
                </tr>
            </tbody>
        </table>
    </div>
</template>
<script>
import { sendMessage, setupSocket } from '../base'

export default {
  name: 'Accounts',
  data () {
    return {
      loading: true,
      accounts: []
    }
  },
  mounted: function () {
    setupSocket(this, (data) => {
      var messageType = data.messageType
      var params = data.params || {}
      this.loading = false
      if (messageType === 'account-list') {
        this.accounts = params.accounts
      }
    })
    // Request accounts
    this.requestAccountListing()
  },
  methods: {
    requestAccountListing: function () {
      this.loading = true
      sendMessage({
        'messageType': 'get-accounts'
      })
    }
  }
}
</script>
<style scoped>

</style>
