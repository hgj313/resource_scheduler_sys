#!/usr/bin/env python3
"""
邮件发送功能测试脚本
"""
import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from app.services.mailer import send_email
from app.core.config import settings

async def test_email_send():
    """测试邮件发送功能"""
    print("=== 邮件发送功能测试 ===")
    print(f"SMTP主机: {settings.SMTP_HOST}")
    print(f"SMTP端口: {settings.SMTP_PORT}")
    print(f"SMTP用户: {settings.SMTP_USER}")
    print(f"发件人: {settings.MAIL_FROM}")
    print(f"管理员邮箱: {settings.MANAGER_EMAIL}")
    print()
    
    # 测试发送邮件
    test_recipient = "2486575431@qq.com"  # 员工邮箱
    test_subject = "【测试】HRC系统邮件功能测试"
    test_html = """
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <h2 style="color: #2563eb;">HRC人力资源调度系统</h2>
        <p>这是一封测试邮件，用于验证系统邮件发送功能是否正常工作。</p>
        <div style="background-color: #f3f4f6; padding: 15px; border-radius: 5px; margin: 15px 0;">
            <h3>邮件配置信息：</h3>
            <ul>
                <li><strong>SMTP服务器:</strong> {smtp_host}</li>
                <li><strong>SMTP端口:</strong> {smtp_port}</li>
                <li><strong>发件人:</strong> {mail_from}</li>
            </ul>
        </div>
        <p>如果收到此邮件，说明系统邮件配置正确！</p>
        <p style="color: #6b7280; font-size: 12px; margin-top: 20px;">
            此邮件由HRC系统自动发送，请勿回复。
        </p>
    </div>
    """.format(
        smtp_host=settings.SMTP_HOST,
        smtp_port=settings.SMTP_PORT,
        mail_from=settings.MAIL_FROM
    )
    
    try:
        print(f"正在发送测试邮件到: {test_recipient}")
        await send_email(test_recipient, test_subject, test_html)
        print("✅ 邮件发送成功！")
        print("请检查收件箱（包括垃圾邮件文件夹）确认是否收到测试邮件。")
        return True
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        print("可能的原因：")
        print("1. SMTP配置错误（主机、端口、用户名、密码）")
        print("2. QQ邮箱授权码不正确或已过期")
        print("3. 网络连接问题")
        print("4. 邮箱服务商限制")
        return False

if __name__ == "__main__":
    # 检查配置是否完整
    if not all([settings.SMTP_HOST, settings.SMTP_USER, settings.SMTP_PASSWORD]):
        print("❌ SMTP配置不完整，请检查.env文件")
        print("必需的配置项：")
        print("  - SMTP_HOST")
        print("  - SMTP_USER") 
        print("  - SMTP_PASSWORD")
        sys.exit(1)
    
    # 运行测试
    result = asyncio.run(test_email_send())
    
    if result:
        print("\n🎉 邮件功能测试完成！")
    else:
        print("\n💥 邮件功能测试失败！")
        sys.exit(1)