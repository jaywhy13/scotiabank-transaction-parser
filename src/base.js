var API_BASE = 'ws://localhost:3000'
var WEBSOCKET_URL = API_BASE + '/ws'
const socket = new WebSocket(WEBSOCKET_URL)

export default function sendMessage (data) {
  console.log('Socket send: ', JSON.stringify(data))
  if (socket.readyState === 0) {
    socket.onopen = () => {
      socket.send(JSON.stringify(data))
    }
  } else {
    socket.send(JSON.stringify(data))
  }
}

function setupSocket (vm, callback) {
  socket.addEventListener('message', function (event) {
    console.log('Socket receive: ', event.data)
    let obj = JSON.parse(event.data)
    vm.$emit('socketMessage', obj)
    callback(obj)
  })
}

export { sendMessage, socket, setupSocket }
