import requests
import os
from datetime import datetime

# 从GitHub密钥读取配置
APPID = os.getenv("APPID")
APPSECRET = os.getenv("APPSECRET")
TEMPLATE_ID = os.getenv("TEMPLATE_ID")
OPENID = os.getenv("OPENID")

# 获取access_token
def get_token():
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={APPSECRET}"
    res = requests.get(url).json()
    return res.get("access_token")

# 发送模板消息
def send_msg(token):
    url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={token}"
    data = {
        "touser": OPENID,
        "template_id": TEMPLATE_ID,
        "data": {
            "date": {"value": datetime.now().strftime("%Y-%m-%d")},
            "weather": {"value": "晴天"},
            "message": {"value": "新的一天也要开心呀☀️"}
        }
    }
    res = requests.post(url, json=data)
    print("推送结果：", res.json())

if __name__ == "__main__":
    token = get_token()
    send_msg(token)
