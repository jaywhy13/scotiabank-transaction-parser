<template>
<div class="row">
  <div class="alert alert-danger" v-if="error" v-text="error"></div>

  <form action="">
    <div class="form-group">
      <label for="security-question" v-text="question"></label>
      <input type="text" name="security-question" class="form-control" value="" required="required" pattern="" title="" v-model="answer">
      <button type="button" class="btn btn-success" v-on:click="answerQuestion" v-bind:disabled="loading">
        <i class="fas fa-circle-notch fa-spin" v-if="loading"></i>
        Submit
      </button>
    </div>
  </form>
</div>
</template>
<script>
import { sendMessage, setupSocket } from '../base'

export default {
  name: 'SecurityQuestion',
  data () {
    return {
      question: '',
      answer: '',
      loading: false,
      error: ''
    }
  },
  mounted: function () {
    window.localStorage.setItem('questions', [])
    setupSocket(this, (data) => {
      var messageType = data.messageType
      var params = data.params || {}
      this.loading = false
      if (messageType === 'security-question') {
        this.question = data.params['security-question']
        let answer = this.getAnswer()
        if (answer) {
          this.answer = answer
          this.answerQuestion()
        }
      } else if (messageType === 'security-question-correct') {
        this.saveAnswer()
        this.$router.push('/accounts')
      } else if (messageType === 'security-question-incorrect') {
        this.error = params.message
      }
    })
    // Request a question as soon as this page loads
    this.requestSecurityQuestion()
  },
  methods: {
    answerQuestion: function () {
      this.loading = true
      sendMessage({
        'messageType': 'security-question-answer',
        'params': {
          'answer': this.answer
        }
      })
    },
    requestSecurityQuestion: function () {
      this.loading = true
      console.log('Requesting a question')
      sendMessage({
        'messageType': 'request-security-question'
      })
    },
    saveAnswer: function () {
      let questions = window.localStorage.getItem('questions') || []
      questions.push({
        question: this.question,
        answer: this.anwer
      })
      window.localStorage.setItem('questions', questions)
    },
    getAnswer: function () {
      let questions = window.localStorage.getItem('questions') || []
      for (let i = 0; i < questions.length; i++) {
        let question = questions[i]
        if (question['question'] === this.question) {
          return question['answer']
        }
      }
    }
  }
}
</script>
<style scoped>

</style>
