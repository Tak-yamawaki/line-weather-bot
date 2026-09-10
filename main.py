import os
import requests
from dotenv import load_dotenv

# =========================
# .envを読み込む
# =========================

load_dotenv()

LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_USER_ID = os.getenv("LINE_USER_ID")


# =========================
# 天気API
# =========================

url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": 35.6895,
    "longitude": 139.6917,

    # 現在の情報
    "current": "temperature_2m,weather_code",

    # 今日の情報
    "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max",

    # 時間ごとの情報
    "hourly": "weather_code,precipitation_probability",

    # 日本時間
    "timezone": "Asia/Tokyo",

    # 今日＋明日のデータ
    "forecast_days": 2,
}


# APIにアクセス
response = requests.get(url, params=params)

print("天気API:", response.status_code)

data = response.json()


# =========================
# 天気コードを日本語に変換
# =========================

def get_weather_name(weather_code):

    if weather_code == 0:
        return "快晴"

    elif weather_code == 1:
        return "晴れ"

    elif weather_code == 2:
        return "晴れ時々曇り"

    elif weather_code == 3:
        return "曇り"

    elif weather_code in [45, 48]:
        return "霧"

    elif weather_code in [51, 53, 55, 56, 57]:
        return "霧雨"

    elif weather_code in [61, 63, 65, 66, 67]:
        return "雨"

    elif weather_code in [71, 73, 75, 77]:
        return "雪"

    elif weather_code in [80, 81, 82]:
        return "にわか雨"

    elif weather_code in [85, 86]:
        return "にわか雪"

    elif weather_code in [95, 96, 99]:
        return "雷雨"

    else:
        return "不明"


# =========================
# 現在の情報
# =========================

temperature = data["current"]["temperature_2m"]
current_weather_code = data["current"]["weather_code"]

current_weather = get_weather_name(current_weather_code)


# =========================
# 今日の情報
# =========================

today_weather_code = data["daily"]["weather_code"][0]
max_temperature = data["daily"]["temperature_2m_max"][0]
min_temperature = data["daily"]["temperature_2m_min"][0]
today_rain_probability = data["daily"]["precipitation_probability_max"][0]

today_weather = get_weather_name(today_weather_code)


# =========================
# 時間帯別の天気を取得
# =========================

hourly_times = data["hourly"]["time"]
hourly_weather_codes = data["hourly"]["weather_code"]
hourly_rain_probabilities = data["hourly"]["precipitation_probability"]


# 朝・昼・夕方の代表時間を調べる
target_hours = {
    "朝": 8,
    "昼": 12,
    "夕方": 18,
}


period_weather = {}

for period, target_hour in target_hours.items():

    for i, time in enumerate(hourly_times):

        # 例：2026-09-09T08:00
        hour = int(time[11:13])

        # 今日の8時、12時、18時を探す
        if time.startswith(hourly_times[0][:10]) and hour == target_hour:

            weather = get_weather_name(hourly_weather_codes[i])
            rain_probability = hourly_rain_probabilities[i]

            period_weather[period] = {
                "weather": weather,
                "rain_probability": rain_probability,
            }

            break


# =========================
# 傘が必要か判定
# =========================

max_rain_probability = max(
    item["rain_probability"]
    for item in period_weather.values()
)


if max_rain_probability >= 60:
    umbrella_message = "☔ 傘を持っていくことをおすすめします。"

elif max_rain_probability >= 30:
    umbrella_message = "🌂 折りたたみ傘があると安心です。"

else:
    umbrella_message = "☀️ 傘は必要なさそうです。"


# =========================
# 「雨のち晴れ」などを判定
# =========================

morning_weather = period_weather["朝"]["weather"]
afternoon_weather = period_weather["昼"]["weather"]
evening_weather = period_weather["夕方"]["weather"]


if morning_weather == "雨" and afternoon_weather in ["晴れ", "快晴"]:
    day_weather_message = "🌧️ 雨のち晴れ"

elif morning_weather in ["晴れ", "快晴"] and afternoon_weather == "雨":
    day_weather_message = "☀️ 晴れのち雨"

elif morning_weather == "曇り" and afternoon_weather in ["晴れ", "快晴"]:
    day_weather_message = "🌤️ 曇りのち晴れ"

elif morning_weather in ["晴れ", "快晴"] and afternoon_weather == "曇り":
    day_weather_message = "🌤️ 晴れのち曇り"

else:
    day_weather_message = f"{morning_weather} → {afternoon_weather}"


# =========================
# LINEに送るメッセージ
# =========================

message = f"""🌤️ 東京の天気予報

【今日の予報】
{day_weather_message}

🌡️ 現在：{temperature}℃
🔺 最高：{max_temperature}℃
🔻 最低：{min_temperature}℃

☔ 今日の最大降水確率：{today_rain_probability}%

【時間帯別】
🌅 朝：{morning_weather}
☀️ 昼：{afternoon_weather}
🌆 夕方：{evening_weather}

【傘判定】
{umbrella_message}
"""


# =========================
# コンソールに表示
# =========================

print(message)


# =========================
# LINEへ送信
# =========================

headers = {
    "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
    "Content-Type": "application/json",
}

payload = {
    "to": LINE_USER_ID,
    "messages": [
        {
            "type": "text",
            "text": message,
        }
    ],
}


line_response = requests.post(
    "https://api.line.me/v2/bot/message/push",
    headers=headers,
    json=payload,
)


print("LINE送信:", line_response.status_code)
print(line_response.text)