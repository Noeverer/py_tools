import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

def send_email():
    smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", 587))
    sender_email = os.environ.get("EMAIL_USER")
    sender_password = os.environ.get("EMAIL_PASS")
    receiver_email = os.environ.get("RECEIVER_EMAIL", sender_email)
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f"[公租房爬虫]任务执行状态通知 - {os.environ.get('RUN_TIME')}"

    body = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>公租房爬虫任务状态通知</title>
</head>
<body>
    <div style="font-family: Arial, sans-serif; border: 1px solid #eaeaea; padding: 20px; border-radius: 8px;">
        <h2 style="color: #2c3e50;">公租房爬虫任务执行状态通知</h2>
        <table style="border-collapse: collapse; width: 100%;">
            <tr style="background-color: #f8f9fa;">
                <td style="padding: 8px; border: 1px solid #ddd;"><strong>项目名称</strong></td>
                <td style="padding: 8px; border: 1px solid #ddd;">{os.environ.get('GITHUB_REPOSITORY')}</td>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;"><strong>工作流名称</strong></td>
                <td style="padding: 8px; border: 1px solid #ddd;">{os.environ.get('GITHUB_WORKFLOW')}</td>
            </tr>
            <tr style="background-color: #f8f9fa;">
                <td style="padding: 8px; border: 1px solid #ddd;"><strong>执行状态</strong></td>
                <td style="padding: 8px; border: 1px solid #ddd; color: {'#e74c3c' if os.environ.get('JOB_STATUS') == 'failure' else '#2ecc71'};">{os.environ.get('JOB_STATUS')}</td>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd;"><strong>执行时间</strong></td>
                <td style="padding: 8px; border: 1px solid #ddd;">{os.environ.get('RUN_TIME')}</td>
            </tr>
            <tr style="background-color: #f8f9fa;">
                <td style="padding: 8px; border: 1px solid #ddd;"><strong>运行ID</strong></td>
                <td style="padding: 8px; border: 1px solid #ddd;">{os.environ.get('GITHUB_RUN_ID')}</td>
            </tr>
        </table>
        <br>
        <p>请检查任务执行情况，如有问题请及时处理。</p>
    </div>
</body>
</html>"""
    
    msg.attach(MIMEText(body, 'html', 'utf-8'))
    
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("Email notification sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

if __name__ == "__main__":
    send_email()