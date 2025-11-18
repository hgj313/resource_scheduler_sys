import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/notifications.css';
import { getCurrentUser, isAuthenticated } from '../services/authService';

const NotificationsPage = () => {
  const navigate = useNavigate();
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const authed = isAuthenticated();
  const user = getCurrentUser();

  // 模拟获取通知数据
  useEffect(() => {
    if (authed) {
      // 这里应该从API获取真实的通知数据
      const mockNotifications = [
        {
          id: 1,
          title: '新任务分配',
          message: '您已被分配到项目 "华南区域数据分析"',
          type: 'assignment',
          timestamp: new Date(Date.now() - 1000 * 60 * 30), // 30分钟前
          read: false
        },
        {
          id: 2,
          title: '系统通知',
          message: '系统维护将于今晚23:00进行',
          type: 'system',
          timestamp: new Date(Date.now() - 1000 * 60 * 120), // 2小时前
          read: true
        },
        {
          id: 3,
          title: '任务提醒',
          message: '您的任务 "数据收集" 将于3天后到期',
          type: 'reminder',
          timestamp: new Date(Date.now() - 1000 * 60 * 60 * 24), // 1天前
          read: true
        }
      ];
      setNotifications(mockNotifications);
    }
    setLoading(false);
  }, [authed]);

  const markAsRead = (id) => {
    setNotifications(prev => 
      prev.map(notif => 
        notif.id === id ? { ...notif, read: true } : notif
      )
    );
  };

  const markAllAsRead = () => {
    setNotifications(prev => 
      prev.map(notif => ({ ...notif, read: true }))
    );
  };

  const deleteNotification = (id) => {
    setNotifications(prev => prev.filter(notif => notif.id !== id));
  };

  const formatTime = (date) => {
    const now = new Date();
    const diff = now - date;
    
    if (diff < 1000 * 60) { // 小于1分钟
      return '刚刚';
    } else if (diff < 1000 * 60 * 60) { // 小于1小时
      return `${Math.floor(diff / (1000 * 60))}分钟前`;
    } else if (diff < 1000 * 60 * 60 * 24) { // 小于1天
      return `${Math.floor(diff / (1000 * 60 * 60))}小时前`;
    } else {
      return `${Math.floor(diff / (1000 * 60 * 60 * 24))}天前`;
    }
  };

  if (!authed) {
    return (
      <div className="notifications-container">
        <div className="notifications-header">
          <h2>通知中心</h2>
          <button className="btn" onClick={() => navigate('/login')}>去登录</button>
        </div>
        <div className="notifications-content">
          <p>请先登录以查看通知</p>
        </div>
      </div>
    );
  }

  return (
    <div className="notifications-container">
      <div className="notifications-header">
        <h2>通知中心</h2>
        <div className="header-actions">
          <button className="btn btn-secondary" onClick={markAllAsRead}>
            全部标记为已读
          </button>
          <button className="btn" onClick={() => navigate('/main')}>
            返回主页
          </button>
        </div>
      </div>

      <div className="notifications-content">
        {loading ? (
          <div className="loading">加载中...</div>
        ) : notifications.length === 0 ? (
          <div className="empty-state">
            <p>暂无通知</p>
          </div>
        ) : (
          <div className="notifications-list">
            {notifications.map(notification => (
              <div
                key={notification.id}
                className={`notification-item ${notification.read ? 'read' : 'unread'} ${notification.type}`}
              >
                <div className="notification-content">
                  <h4 className="notification-title">{notification.title}</h4>
                  <p className="notification-message">{notification.message}</p>
                  <span className="notification-time">
                    {formatTime(notification.timestamp)}
                  </span>
                </div>
                <div className="notification-actions">
                  {!notification.read && (
                    <button
                      className="btn btn-sm btn-primary"
                      onClick={() => markAsRead(notification.id)}
                    >
                      标记已读
                    </button>
                  )}
                  <button
                    className="btn btn-sm"
                    onClick={() => deleteNotification(notification.id)}
                  >
                    删除
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="notifications-footer">
        <p>共 {notifications.length} 条通知，其中 {notifications.filter(n => !n.read).length} 条未读</p>
      </div>
    </div>
  );
};

export default NotificationsPage;