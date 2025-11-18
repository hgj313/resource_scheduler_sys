let ws
let listeners = []

export function connectNotifications(userId) {
  const url = `ws://${window.location.hostname}:8000/api/v1/notifications/ws?user_id=${encodeURIComponent(userId)}`
  ws = new WebSocket(url)
  
  ws.onopen = () => {
    console.log('WebSocket连接已建立')
  }
  
  ws.onmessage = (ev) => {
    try {
      const msg = JSON.parse(ev.data)
      listeners.forEach((fn) => fn(msg))
    } catch (error) {
      console.error('解析WebSocket消息失败:', error)
    }
  }
  
  ws.onerror = (error) => {
    console.error('WebSocket错误:', error)
  }
  
  ws.onclose = () => {
    console.log('WebSocket连接已关闭')
  }
}

export function onNotify(fn) {
  listeners.push(fn)
}

export function disconnectNotifications() {
  if (ws) {
    ws.close()
    ws = null
  }
  listeners = []
}