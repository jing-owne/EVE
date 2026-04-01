# -*- coding: utf-8 -*-
"""发送格式化邮件"""
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr
from email.mime.image import MIMEImage
import sys

def load_config():
    config = {}
    config_path = r'C:\Users\admin\.qclaw\workspace\email_config.txt'
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    k, v = line.split('=', 1)
                    config[k.strip()] = v.strip()
    return config

def send_email(to_addr, subject, html_content, config):
    # SMTP配置
    host = config.get('SMTP_HOST', 'smtp.qq.com')
    port = int(config.get('SMTP_PORT', 465))
    user = config.get('SMTP_USER', '')
    password = config.get('SMTP_PASS', '')
    from_name = config.get('FROM_NAME', 'Marcus')

    # 构建邮件
    msg = MIMEMultipart('alternative')
    msg['From'] = formataddr([from_name, user])
    msg['To'] = to_addr
    msg['Subject'] = Header(subject, 'utf-8')

    # HTML正文
    html_part = MIMEText(html_content, 'html', 'utf-8')
    msg.attach(html_part)

    # 发送
    with smtplib.SMTP_SSL(host, port) as server:
        server.login(user, password)
        server.sendmail(user, [to_addr], msg.as_string())
    print(f'发送成功: {to_addr}')

if __name__ == '__main__':
    config = load_config()
    to = sys.argv[1] if len(sys.argv) > 1 else '18339435211@139.com'
    subject = sys.argv[2] if len(sys.argv) > 2 else '五大策略综合选股'
    html = sys.argv[3] if len(sys.argv) > 3 else '<h1>测试</h1>'
    send_email(to, subject, html, config)
