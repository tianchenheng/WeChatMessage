import requests
import os
import zhdate
from datetime import datetime

# ==================== 【请手动修改这里的日期】====================
# 1. 在一起第一天
LOVE_START = "2024-01-01"
# 2. 宝宝生日（每年循环倒计时）
BIRTHDAY = "2025-06-01"
# 3. 下次见面日期
MEET_DATE = "2026-06-10"
# =================================================================

# 读取GitHub密钥
APPID = os.getenv("APPID")
APPSECRET = os.getenv("APPSECRET")
TEMPLATE_ID = os.getenv("TEMPLATE_ID")
OPENID = os.getenv("OPENID")
WEATHER_KEY = os.getenv("WEATHER_KEY")

# 获取微信 access_token
def get_wx_token():
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={APPSECRET}"
    return requests.get(url).json().get("access_token")

# 获取单个城市天气：返回 天气状况, 温度
def get_city_weather(city):
    url = f"https://api.seniverse.com/v3/weather/now.json?key={WEATHER_KEY}&location={city}&language=zh-Hans&unit=c"
    res = requests.get(url).json()
    now = res["results"][0]["now"]
    return now["text"], now["temperature"]

# 计算两个日期相差天数
def calc_day_diff(start_date, end_date):
    s = datetime.strptime(start_date, "%Y-%m-%d")
    e = datetime.strptime(end_date, "%Y-%m-%d")
    diff = e - s
    return diff.days

# 计算生日倒计时（每年循环）
def get_birthday_count(birth_str):
    today = datetime.now()
    birth = datetime.strptime(birth_str, "%Y-%m-%d")
    # 今年生日
    this_year_birth = datetime(today.year, birth.month, birth.day)
    if this_year_birth < today:
        # 今年已过，计算明年
        next_year_birth = datetime(today.year + 1, birth.month, birth.day)
        return (next_year_birth - today).days
    else:
        return (this_year_birth - today).days

# 主逻辑：组装数据 + 发送消息
def send_msg():
    token = get_wx_token()
    today = datetime.now()

    # 1. 公历、农历日期
    year = today.year
    g_date = today.strftime("%m月%d日")
    lunar = zhdate.ZhDate.from_datetime(today).chinese()

    # 2. 双城市天气
    ty_weather, ty_temp = get_city_weather("太原")
    bj_weather, bj_temp = get_city_weather("北京")

    # 3. 各项倒计时
    love_days = calc_day_diff(LOVE_START, today.strftime("%Y-%m-%d"))
    birth_days = get_birthday_count(BIRTHDAY)
    meet_days = calc_day_diff(today.strftime("%Y-%m-%d"), MEET_DATE)

    # 组装推送数据
    post_data = {
        "touser": OPENID,
        "template_id": TEMPLATE_ID,
        "data": {
            "year": {"value": str(year)},
            "date": {"value": g_date},
            "lunar": {"value": lunar},
            "ty_weather": {"value": ty_weather},
            "ty_temp": {"value": ty_temp},
            "bj_weather": {"value": bj_weather},
            "bj_temp": {"value": bj_temp},
            "love_day": {"value": str(love_days)},
            "birth_day": {"value": str(birth_days)},
            "meet_day": {"value": str(meet_days)}
        }
    }

    # 发送请求
    send_url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={token}"
    res = requests.post(send_url, json=post_data)
    print("推送结果：", res.json())

if __name__ == "__main__":
    send_msg()
