import requests
import schedule
import time
from datetime import datetime
import os
import json

from dotenv import load_dotenv
load_dotenv()


def refresh_cookie():
    """刷新 Cookie 的逻辑（需要根据实际网站实现）"""
    global Cookie
    try:
        # 替换为实际的登录 URL 和登录数据
        login_url = "https://mxwljsq.top/auth/login"
        login_data = {
            "email": os.environ.get("MX_EMAIL"),  # 从环境变量获取邮箱
            "passwd": os.environ.get("MX_PASSWORD"),  # 从环境变量获取密码
        }

        print(login_data)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        # exit()
        # 发送登录请求
        response = requests.post(login_url, data=login_data, headers=headers)
        print(response.text)
        if response.status_code == 200:
            # 假设登录成功后 Cookie 在响应头中返回
            new_cookie = response.cookies.get_dict()
            Cookie = "; ".join([f"{k}={v}" for k, v in new_cookie.items()])
            print(f"{datetime.now()} Cookie 刷新成功")
            return True
        else:
            print(f"{datetime.now()} Cookie 刷新失败：{response.text}")
            return False
    except Exception as e:
        print(f"{datetime.now()} Cookie 刷新异常：{str(e)}")
        return False

def checkin():
    refresh_cookie()
    global Cookie
    if Cookie is None:
        print("Cookie 为空，请先刷新 Cookie")
        return False
    url = "https://mxwljsq.top/user/checkin"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Content-Type": "application/json",
        "Cookie": Cookie,
    }

    try:
        response = requests.post(url, headers=headers)
        response_json = response.json()

        if response.status_code == 200:
            print(f"{datetime.now()} 签到成功：{response_json.get('msg')}")
            return True
        else:
            print(f"{datetime.now()} 签到失败：{response_json.get('msg')}")
            # 如果是登录失效，尝试刷新 Cookie
            return False
    except Exception as e:
        print(f"{datetime.now()} 签到请求失败：{str(e)}")
        return False

if __name__ == "__main__":
    print("自动签到脚本已启动...")
    # 加载本地 Cookie，如果没有则使用环境变量中的
    # 首次运行立即签到
    print(f"{datetime.now()} 开始执行签到任务...")
    checkin()