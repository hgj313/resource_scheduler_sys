#!/usr/bin/env python3
"""
邮件发送功能调试脚本
"""
import asyncio
import sys
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from app.core.config import settings

def test_smtp_connection():
    """测试SMTP连接"""
    print("=== SMTP连接测试 ===")
    print(f"主机: {settings.SMTP_HOST}")
    print(f"端口: {settings.SMTP_PORT}")
    print(f"用户: {settings.SMTP_USER}")
    
    try:
        # 测试直接SMTP连接
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=10) as server:
            print("✅ SMTP连接成功")
            
            # 测试EHLO
            ehlo_response = server.ehlo()
            print(f"EHLO响应: {ehlo_response[0]}")
            
            # 检查STARTTLS支持
            if server.has_extn('STARTTLS'):
                print("✅ 服务器支持STARTTLS")
                server.starttls()
                print("✅ STARTTLS加密成功")
                # 再次EHLO
                server.ehlo()
            else:
                print("❌ 服务器不支持STARTTLS")
                
            # 尝试登录
            try:
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                print("✅ SMTP登录成功")
                return True
            except Exception as login_error:
                print(f"❌ SMTP登录失败: {login_error}")
                return False
                
    except Exception as e:
        print(f"❌ SMTP连接失败: {e}")
        return False

async def test_fastapi_mail():
    """测试FastAPI-Mail发送"""
    print("\n=== FastAPI-Mail发送测试 ===")
    
    from app.services.mailer import send_email
    
    test_recipient = "2486575431@qq.com"
    test_subject = "【FastAPI-Mail测试】HRC系统邮件功能测试"
    test_html = "<p>这是一封通过FastAPI-Mail发送的测试邮件</p>"
    
    try:
        print(f"正在发送测试邮件到: {test_recipient}")
        await send_email(test_recipient, test_subject, test_html)
        print("✅ FastAPI-Mail发送成功！")
        return True
    except Exception as e:
        print(f"❌ FastAPI-Mail发送失败: {e}")
        return False

def test_direct_smtp_send():
    """测试直接SMTP发送"""
    print("\n=== 直接SMTP发送测试 ===")
    
    # 创建邮件
    msg = MIMEMultipart()
    msg['From'] = settings.MAIL_FROM
    msg['To'] = "2486575431@qq.com"
    msg['Subject'] = "【直接SMTP测试】HRC系统邮件功能测试"
    
    body = "这是一封通过直接SMTP连接发送的测试邮件"
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        # 直接使用smtplib发送
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=10) as server:
            server.ehlo()
            
            if server.has_extn('STARTTLS'):
                server.starttls()
                server.ehlo()
            
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            
            server.sendmail(
                settings.MAIL_FROM, 
                "2486575431@qq.com", 
                msg.as_string()
            )
            
            print("✅ 直接SMTP发送成功！")
            return True
            
    except Exception as e:
        print(f"❌ 直接SMTP发送失败: {e}")
        return False

if __name__ == "__main__":
    # 检查配置
    if not all([settings.SMTP_HOST, settings.SMTP_USER, settings.SMTP_PASSWORD]):
        print("❌ SMTP配置不完整")
        sys.exit(1)
    
    print("开始邮件功能调试...")
    
    # 测试1: SMTP连接
    smtp_ok = test_smtp_connection()
    
    # 测试2: 直接SMTP发送
    direct_ok = test_direct_smtp_send()
    
    # 测试3: FastAPI-Mail发送
    fastapi_ok = asyncio.run(test_fastapi_mail())
    
    print("\n=== 测试结果总结 ===")
    print(f"SMTP连接测试: {'✅ 成功' if smtp_ok else '❌ 失败'}")
    print(f"直接SMTP发送测试: {'✅ 成功' if direct_ok else '❌ 失败'}")
    print(f"FastAPI-Mail发送测试: {'✅ 成功' if fastapi_ok else '❌ 失败'}")
    
    if all([smtp_ok, direct_ok, fastapi_ok]):
        print("🎉 所有邮件测试通过！")
    else:
        print("💥 邮件功能存在問題，请检查配置")
        sys.exit(1)