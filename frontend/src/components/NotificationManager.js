import React, { useState, useEffect, useRef } from 'react'
import NotificationToast from './NotificationToast'
import { connectNotifications, onNotify, disconnectNotifications } from '../services/notifyService'
import { isAuthenticated, getCurrentUser } from '../services/authService'

const NotificationManager = ({ userId = null }) => {
  const [notifications, setNotifications] = useState([])
  const currentUserIdRef = useRef(null)

  useEffect(() => {
    // 获取当前用户信息
    const currentUser = getCurrentUser()
    const effectiveUserId = userId || (currentUser ? currentUser.email : 'guest')
    
    // 只有在用户ID变化时才重新连接
    if (effectiveUserId !== currentUserIdRef.current) {
      currentUserIdRef.current = effectiveUserId
      
      // 断开现有连接
      disconnectNotifications()
      
      // 如果用户已认证，建立新的WebSocket连接
      if (isAuthenticated()) {
        connectNotifications(effectiveUserId)
      }
    }

    // 监听通知消息
    const handleNotify = (message) => {
      const id = Date.now() + Math.random()
      setNotifications(prev => [...prev, { id, message }])
    }

    onNotify(handleNotify)

    return () => {
      // 组件卸载时断开连接
      disconnectNotifications()
    }
  }, [userId])

  const removeNotification = (id) => {
    setNotifications(prev => prev.filter(notif => notif.id !== id))
  }

  return (
    <div className="notification-manager">
      {notifications.map((notif) => (
        <NotificationToast
          key={notif.id}
          message={notif.message}
          type={notif.message.type}
          duration={5000}
          onClose={() => removeNotification(notif.id)}
        />
      ))}
    </div>
  )
}

export default NotificationManager