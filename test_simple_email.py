#!/usr/bin/env python3
"""
简单邮件发送测试 - 使用smtplib直接发送
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from app.core.config import settings

def send_simple_email():
    """使用smtplib直接发送邮件"""
    print("=== 简单邮件发送测试 ===")
    print(f"SMTP主机: {settings.SMTP_HOST}")
    print(f"SMTP端口: {settings.SMTP_PORT}")
    print(f"发件人: {settings.SMTP_USER}")
    print(f"收件人: 2486575431@qq.com")
    
    # 创建邮件内容
    msg = MIMEMultipart()
    msg['From'] = settings.SMTP_USER
    msg['To'] = "2486575431@qq.com"
    msg['Subject'] = "【HRC系统测试】简单邮件发送测试"
    
    body = """
    HRC人力资源调度系统 - 邮件功能测试
    
    这是一封测试邮件，用于验证系统邮件发送功能。
    
    配置信息：
    - SMTP服务器: {host}
    - SMTP端口: {port}
    - 发件人: {sender}
    
    如果收到此邮件，说明邮件配置正确！
    """.format(
        host=settings.SMTP_HOST,
        port=settings.SMTP_PORT,
        sender=settings.SMTP_USER
    )
    
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        # 连接SMTP服务器
        print("正在连接SMTP服务器...")
        server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=30)
        
        # 调试信息
        server.set_debuglevel(1)
        
        print("发送EHLO...")
        server.ehlo()
        
        print("启动TLS加密...")
        server.starttls()
        
        print("再次EHLO...")
        server.ehlo()
        
        print("登录邮箱...")
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        
        print("发送邮件...")
        server.sendmail(
            settings.SMTP_USER,
            "2486575431@qq.com",
            msg.as_string()
        )
        
        print("关闭连接...")
        server.quit()
        
        print("✅ 邮件发送成功！")
        print("请检查邮箱（包括垃圾邮件文件夹）确认是否收到测试邮件。")
        return True
        
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # 检查配置
    if not all([settings.SMTP_HOST, settings.SMTP_USER, settings.SMTP_PASSWORD]):
        print("❌ SMTP配置不完整")
        sys.exit(1)
    
    success = send_simple_email()
    
    if success:
        print("\n🎉 邮件功能测试完成！")
    else:
        print("\n💥 邮件功能测试失败！")
        sys.exit(1)