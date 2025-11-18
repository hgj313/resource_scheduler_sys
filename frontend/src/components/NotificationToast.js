import React, { useState, useEffect } from 'react'
import './NotificationToast.css'

const NotificationToast = ({ message, type = 'info', duration = 5000, onClose }) => {
  const [isVisible, setIsVisible] = useState(true)

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsVisible(false)
      setTimeout(() => onClose(), 300)
    }, duration)

    return () => clearTimeout(timer)
  }, [duration, onClose])

  const getIcon = () => {
    switch (type) {
      case 'assign':
        return '📋'
      case 'reminder':
        return '⏰'
      default:
        return '💬'
    }
  }

  const getTitle = () => {
    switch (type) {
      case 'assign':
        return '派遣通知'
      case 'reminder':
        return `到期提醒 (D-${message.days_before || 0})`
      default:
        return '系统通知'
    }
  }

  if (!isVisible) return null

  return (
    <div className={`notification-toast notification-toast--${type}`}>
      <div className="notification-toast__icon">{getIcon()}</div>
      <div className="notification-toast__content">
        <div className="notification-toast__title">{getTitle()}</div>
        <div className="notification-toast__message">
          {type === 'assign' && (
            <span>员工 {message.employee_name} 被派往 {message.region}/{message.project_name}</span>
          )}
          {type === 'reminder' && (
            <span>员工 {message.employee_name} 在 {message.region}/{message.project_name} 的任务还有 {message.days_before} 天到期</span>
          )}
        </div>
      </div>
      <button className="notification-toast__close" onClick={() => {
        setIsVisible(false)
        setTimeout(() => onClose(), 300)
      }}>×</button>
    </div>
  )
}

export default NotificationToast