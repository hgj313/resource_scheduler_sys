class WebSocketManager {
  constructor() {
    this.ws = null
    this.listeners = new Map()
    this.currentUserId = null
    this.reconnectAttempts = 0
    this.maxReconnectAttempts = 5
    this.reconnectDelay = 1000
  }

  connect(userId) {
    if (this.ws && this.currentUserId === userId) {
      console.log('WebSocket连接已存在，无需重复连接')
      return
    }

    // 断开现有连接
    this.disconnect()

    this.currentUserId = userId
    const url = `ws://${window.location.hostname}:8000/api/v1/notifications/ws?user_id=${encodeURIComponent(userId)}`
    
    try {
      this.ws = new WebSocket(url)
      
      this.ws.onopen = () => {
        console.log('WebSocket连接已建立')
        this.reconnectAttempts = 0
      }
      
      this.ws.onmessage = (ev) => {
        try {
          const msg = JSON.parse(ev.data)
          this.listeners.forEach((listener) => {
            try {
              listener(msg)
            } catch (error) {
              console.error('监听器执行错误:', error)
            }
          })
        } catch (error) {
          console.error('解析WebSocket消息失败:', error)
        }
      }
      
      this.ws.onerror = (error) => {
        console.error('WebSocket错误:', error)
      }
      
      this.ws.onclose = (event) => {
        console.log('WebSocket连接已关闭', event.code, event.reason)
        this.attemptReconnect()
      }

    } catch (error) {
      console.error('创建WebSocket连接失败:', error)
    }
  }

  attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts && this.currentUserId) {
      this.reconnectAttempts++
      console.log(`尝试第 ${this.reconnectAttempts} 次重连...`)
      
      setTimeout(() => {
        this.connect(this.currentUserId)
      }, this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1))
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close(1000, '正常关闭')
      this.ws = null
    }
    this.currentUserId = null
  }

  onNotify(listenerId, fn) {
    this.listeners.set(listenerId, fn)
  }

  offNotify(listenerId) {
    this.listeners.delete(listenerId)
  }

  getConnectionState() {
    return this.ws ? this.ws.readyState : WebSocket.CLOSED
  }
}

// 创建全局单例实例
const wsManager = new WebSocketManager()

// 导出兼容旧接口的函数
export function connectNotifications(userId) {
  wsManager.connect(userId)
}

export function onNotify(listenerId, fn) {
  wsManager.onNotify(listenerId, fn)
}

export function offNotify(listenerId) {
  wsManager.offNotify(listenerId)
}

export function disconnectNotifications() {
  wsManager.disconnect()
}

export function getWebSocketState() {
  return wsManager.getConnectionState()
}