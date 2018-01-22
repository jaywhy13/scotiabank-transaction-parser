import vue from 'vue'

var API_BASE = 'ws://localhost:3000'
var WEBSOCKET_URL = API_BASE + '/ws'
const socket = new WebSocket(WEBSOCKET_URL)
socket.addEventListener('message', function (event) {
  console.log('Socket receive: ', event.data)
  vue.$emit('socket-message', event.data)
})

export default function sendMessage (data) {
  console.log('Socket send: ', JSON.stringify(data))
  socket.send(JSON.stringify(data))
}

export { sendMessage, socket }
