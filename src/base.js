var API_BASE = 'ws://localhost:3000'
var WEBSOCKET_URL = API_BASE + '/ws'
const socket = new WebSocket(WEBSOCKET_URL)

export default function sendMessage (data) {
  console.log('Socket send: ', JSON.stringify(data))
  socket.send(JSON.stringify(data))
}

function setupSocket (vm) {
  socket.addEventListener('message', function (event) {
    console.log('Socket receive: ', event.data)
    vm.$emit('socketMessage', JSON.parse(event.data))
  })
}

export { sendMessage, socket, setupSocket }
