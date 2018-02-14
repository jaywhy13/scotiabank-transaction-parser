<template>
    <div class="row">
        <h2 v-text="name"></h2>
        <table class="table table-hover">
            <thead>
                <tr>
                    <th>Date</th>
                    <th>Transaction</th>
                    <th>Amount</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="transaction in transactions" v-bind:key="transaction.description">
                    <td v-text="transaction.date">
                    </td>
                    <td v-text="transaction.description"></td>
                    <td v-text="transaction.amount"></td>
                </tr>
            </tbody>
        </table>
    </div>
</template>
<script>
import { sendMessage, setupSocket } from '../base'

export default {
  name: 'Account',
  data () {
    return {
      loading: true,
      name: '...',
      accountNumber: this.$route.params.accountNumber,
      branchCode: this.$route.params.branchCode,
      transactions: []
    }
  },
  mounted: function () {
    setupSocket(this, (data) => {
      var messageType = data.messageType
      var params = data.params || {}
      this.loading = false
      if (messageType === 'transactions') {
        this.transactions = params.transactions
      }
    })
    // Request accounts
    this.requestAccountTransactions()
  },
  methods: {
    requestAccountTransactions: function () {
      this.loading = true
      sendMessage({
        'messageType': 'get-transactions',
        'params': {
          'account_number': this.accountNumber,
          'branch_code': this.branchCode
        }
      })
    }
  }
}
</script>
<style scoped>

</style>
