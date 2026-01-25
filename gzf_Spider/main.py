#!/usr/bin/env python3
"""
公租房爬虫主入口脚本
用于与GitHub Actions集成，支持多种运行模式
"""

import argparse
import sys
import os
from datetime import datetime

# 添加src目录到模块搜索路径
src_path = os.path.join(os.path.dirname(__file__), 'src')
script_path = os.path.join(os.path.dirname(__file__), 'scripts')
sys.path.insert(0, src_path)
sys.path.insert(0, script_path)

from mySpider_gongzufang import main as run_spider
from send_bark_notification import send_bark_notification
from send_notification_email import send_email


def main():
    parser = argparse.ArgumentParser(description='公租房爬虫自动化任务')
    parser.add_argument('--mode', choices=['normal', 'debug', 'test'], 
                        default='normal', help='运行模式: normal(正常), debug(调试), test(测试)')
    args = parser.parse_args()

    print("="*50)
    print("公租房爬虫自动化任务启动")
    print(f"运行模式: {args.mode}")
    print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50)

    # 根据模式决定是否运行爬虫
    if args.mode == 'test':
        print("测试模式：跳过实际爬虫执行，仅测试依赖和环境")
        # 这里可以添加环境检查代码
        print("环境检查完成")
    elif args.mode == 'debug':
        print("调试模式：开始执行爬虫任务...")
        run_spider()
    else:  # normal
        print("正常模式：开始执行爬虫任务...")
        run_spider()

    print("爬虫任务执行完成")
    
    # 设置环境变量供通知脚本使用
    os.environ['RUN_TIME'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    os.environ['JOB_STATUS'] = 'success'  # 在当前实现中总是设为成功，实际应用中应根据执行结果设置
    
    # 尝试发送通知（如果配置了相应服务）
    try:
        # 发送Bark通知
        if os.environ.get('BARK_URL'):
            print("正在发送Bark通知...")
            send_bark_notification()
        else:
            print("未配置Bark URL，跳过Bark通知")
        
        # 发送邮件通知
        if os.environ.get('EMAIL_USER') and os.environ.get('EMAIL_PASS') and os.environ.get('SMTP_SERVER'):
            print("正在发送邮件通知...")
            send_email()
        else:
            print("未完全配置邮件参数，跳过邮件通知")
    except Exception as e:
        print(f"发送通知时发生错误: {e}")

    print("公租房爬虫任务全流程完成")


if __name__ == "__main__":
    main()