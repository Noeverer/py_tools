import os
import urllib.parse
import requests

def send_bark_notification():
    bark_url = os.environ.get('BARK_URL')
    message = os.environ.get('MESSAGE')
    repo_name = os.environ.get('REPO_NAME')
    workflow_name = os.environ.get('WORKFLOW_NAME')
    status = os.environ.get('STATUS')
    run_time = os.environ.get('RUN_TIME')
    run_id = os.environ.get('RUN_ID')

    # 构建通知标题和内容
    title = f"公租房爬虫任务通知"
    content = f"Repo: {repo_name}%0AWorkflow: {workflow_name}%0AStatus: {status}%0ARun Time: {run_time}%0ARun ID: {run_id}"
    
    # 确保Bark URL格式正确
    if not bark_url.startswith(('http://', 'https://')):
        if bark_url.startswith('api.day.app'):
            bark_url = f"https://{bark_url}"
        else:
            bark_url = f"https://api.day.app/{bark_url}"
    
    # 构建完整的请求URL
    request_url = f"{bark_url}/{urllib.parse.quote(title)}/{urllib.parse.quote(content)}?icon=https://raw.githubusercontent.com/azhuge233/Pixiv-Daily-Ranking/master/icon.png&group=公租房爬虫"
    
    try:
        response = requests.get(request_url)
        if response.status_code == 200:
            print("Bark notification sent successfully!")
        else:
            print(f"Failed to send Bark notification. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending Bark notification: {str(e)}")

if __name__ == "__main__":
    send_bark_notification()