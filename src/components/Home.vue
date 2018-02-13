<template>
<div class="row">
  <i class="fas fa-circle-notch fa-spin"></i> Loading
</div>
</template>

<script>
import { sendMessage, setupSocket } from '../base'

export default {
  name: 'Home',
  data () {
    return {
    }
  },
  mounted: function () {
    setupSocket(this, (data) => {
      this.socketMessage(data)
    })

    if (this.getLocalSessionKey()) {
      this.sendSessionKey()
      sendMessage({
        'messageType': 'get-current-page'
      })
    } else {
      this.requestSessionKey()
    }
  },
  methods: {
    socketMessage: function (data) {
      var messageType = data.messageType
      var params = data.params || {}
      var page = params.page
      if (messageType === 'current-page') {
        if (page === 'login') {
          this.$router.push('/login')
        } else if (page === 'security-question') {
          this.$router.push('/security-question')
        } else if (page === 'accounts') {
          this.$router.push('/accounts')
        }
      } else if (messageType === 'session-key') {
        self.saveSessionKey(params.key)
      }
    },
    getLocalSessionKey: function () {
      let key = localStorage.getItem('session-key')
      return key
    },
    sendSessionKey: function () {
      if (this.getLocalSessionKey()) {
        sendMessage({
          'messageType': 'session-key',
          'params': {
            'key': this.getLocalSessionKey()
          }
        })
      }
    },
    requestSessionKey: function () {
      sendMessage({
        'messageType': 'request-session-key'
      })
    },
    saveSessionKey: function (key) {
      localStorage.setItem('session-key', key)
    }
  }
}
</script>

<style scoped>

</style>
