from flask import Flask, render_template, request, jsonify, make_response
import requests
from datetime import datetime
import hashlib

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cyber-weather-2077'

POPULAR_CITIES = {
    "beijing": {"name": "北京", "country": "CN", "latitude": 39.9042, "longitude": 116.4074},
    "shanghai": {"name": "上海", "country": "CN", "latitude": 31.2304, "longitude": 121.4737},
    "guangzhou": {"name": "广州", "country": "CN", "latitude": 23.1291, "longitude": 113.2644},
    "shenzhen": {"name": "深圳", "country": "CN", "latitude": 22.5431, "longitude": 114.0579},
    "chengdu": {"name": "成都", "country": "CN", "latitude": 30.5728, "longitude": 104.0668},
    "hangzhou": {"name": "杭州", "country": "CN", "latitude": 30.2741, "longitude": 120.1551},
    "xian": {"name": "西安", "country": "CN", "latitude": 34.3416, "longitude": 108.9398},
    "chongqing": {"name": "重庆", "country": "CN", "latitude": 29.4316, "longitude": 106.9123},
    "nanjing": {"name": "南京", "country": "CN", "latitude": 32.0603, "longitude": 118.7969},
    "wuhan": {"name": "武汉", "country": "CN", "latitude": 30.5928, "longitude": 114.3055},
    "qingdao": {"name": "青岛", "country": "CN", "latitude": 36.0671, "longitude": 120.3826},
    "xiamen": {"name": "厦门", "country": "CN", "latitude": 24.4798, "longitude": 118.0894},
    "harbin": {"name": "哈尔滨", "country": "CN", "latitude": 45.8038, "longitude": 126.5350},
    "sanya": {"name": "三亚", "country": "CN", "latitude": 18.2528, "longitude": 109.5119},
    "hongkong": {"name": "香港", "country": "HK", "latitude": 22.3193, "longitude": 114.1694},
    "taipei": {"name": "台北", "country": "TW", "latitude": 25.0330, "longitude": 121.5654},
    "macau": {"name": "澳门", "country": "MO", "latitude": 22.1987, "longitude": 113.5439},
    "tokyo": {"name": "东京", "country": "JP", "latitude": 35.6762, "longitude": 139.6503},
    "seoul": {"name": "首尔", "country": "KR", "latitude": 37.5665, "longitude": 126.9780},
    "singapore": {"name": "新加坡", "country": "SG", "latitude": 1.3521, "longitude": 103.8198},
    "newyork": {"name": "纽约", "country": "US", "latitude": 40.7128, "longitude": -74.0060},
    "london": {"name": "伦敦", "country": "UK", "latitude": 51.5074, "longitude": -0.1278},
    "paris": {"name": "巴黎", "country": "FR", "latitude": 48.8566, "longitude": 2.3522},
    "sydney": {"name": "悉尼", "country": "AU", "latitude": -33.8688, "longitude": 151.2093},
    "dubai": {"name": "迪拜", "country": "AE", "latitude": 25.2048, "longitude": 55.2708},
    "bangkok": {"name": "曼谷", "country": "TH", "latitude": 13.7563, "longitude": 100.5018},
}

COUNTRY_NAMES = {
    "CN": "中国", "HK": "香港", "TW": "台湾", "MO": "澳门",
    "JP": "日本", "KR": "韩国", "SG": "新加坡", "TH": "泰国",
    "US": "美国", "UK": "英国", "FR": "法国", "DE": "德国",
    "RU": "俄罗斯", "AU": "澳大利亚", "AE": "阿联酋",
    "CA": "加拿大", "BR": "巴西", "IN": "印度", "VN": "越南",
    "MY": "马来西亚", "ID": "印尼", "PH": "菲律宾", "NZ": "新西兰",
    "IT": "意大利", "ES": "西班牙", "NL": "荷兰", "SE": "瑞典",
    "CH": "瑞士", "NO": "挪威", "DK": "丹麦", "FI": "芬兰",
    "PL": "波兰", "CZ": "捷克", "PT": "葡萄牙", "GR": "希腊",
    "TR": "土耳其", "EG": "埃及", "ZA": "南非", "AR": "阿根廷",
    "MX": "墨西哥", "CL": "智利", "PE": "秘鲁", "CO": "哥伦比亚",
}

WEATHER_CODES = {
    0: {"description": "晴", "icon": "sunny", "cyber": "CLEAR_SKY"},
    1: {"description": "大部晴朗", "icon": "sunny", "cyber": "MOSTLY_CLEAR"},
    2: {"description": "局部多云", "icon": "partly-cloudy", "cyber": "PARTLY_CLOUDY"},
    3: {"description": "阴天", "icon": "cloudy", "cyber": "OVERCAST"},
    45: {"description": "有雾", "icon": "fog", "cyber": "FOG"},
    48: {"description": "雾凇", "icon": "fog", "cyber": "RIME_FOG"},
    51: {"description": "小毛毛雨", "icon": "drizzle", "cyber": "LIGHT_DRIZZLE"},
    53: {"description": "毛毛雨", "icon": "drizzle", "cyber": "DRIZZLE"},
    55: {"description": "大毛毛雨", "icon": "drizzle", "cyber": "HEAVY_DRIZZLE"},
    56: {"description": "冻毛毛雨", "icon": "drizzle", "cyber": "FREEZING_DRIZZLE_L"},
    57: {"description": "强冻毛毛雨", "icon": "drizzle", "cyber": "FREEZING_DRIZZLE_H"},
    61: {"description": "小雨", "icon": "rain", "cyber": "LIGHT_RAIN"},
    63: {"description": "中雨", "icon": "rain", "cyber": "RAIN"},
    65: {"description": "大雨", "icon": "rain", "cyber": "HEAVY_RAIN"},
    66: {"description": "冻雨", "icon": "rain", "cyber": "FREEZING_RAIN_L"},
    67: {"description": "强冻雨", "icon": "rain", "cyber": "FREEZING_RAIN_H"},
    71: {"description": "小雪", "icon": "snow", "cyber": "LIGHT_SNOW"},
    73: {"description": "中雪", "icon": "snow", "cyber": "SNOW"},
    75: {"description": "大雪", "icon": "snow", "cyber": "HEAVY_SNOW"},
    77: {"description": "雪粒", "icon": "snow", "cyber": "SNOW_GRAINS"},
    80: {"description": "小阵雨", "icon": "rain", "cyber": "LIGHT_SHOWERS"},
    81: {"description": "阵雨", "icon": "rain", "cyber": "SHOWERS"},
    82: {"description": "强阵雨", "icon": "rain", "cyber": "HEAVY_SHOWERS"},
    85: {"description": "小阵雪", "icon": "snow", "cyber": "LIGHT_SNOW_SHOWERS"},
    86: {"description": "强阵雪", "icon": "snow", "cyber": "HEAVY_SNOW_SHOWERS"},
    95: {"description": "雷暴", "icon": "thunder", "cyber": "THUNDERSTORM"},
    96: {"description": "雷暴伴有小冰雹", "icon": "thunder", "cyber": "THUNDER_HAIL_L"},
    99: {"description": "雷暴伴有大冰雹", "icon": "thunder", "cyber": "THUNDER_HAIL_H"},
}


def make_city_key(name, lat, lon):
    raw = f"{name}_{lat:.2f}_{lon:.2f}"
    return hashlib.md5(raw.encode()).hexdigest()[:12]


def geocode_search(query, count=15):
    params = {
        "name": query,
        "count": count,
        "language": "zh",
        "format": "json",
    }
    url = "https://geocoding-api.open-meteo.com/v1/search"
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code != 200:
            return []
        data = response.json()
        results = data.get("results", [])
        if not results:
            return []
        cities = []
        for item in results:
            name = item.get("name", "未知")
            country_code = item.get("country_code", "")
            admin1 = item.get("admin1", "")
            admin2 = item.get("admin2", "")
            lat = item.get("latitude")
            lon = item.get("longitude")
            if lat is None or lon is None:
                continue
            display_name = name
            extra = []
            if admin1 and admin1 != name:
                extra.append(admin1)
            if admin2 and admin2 != name and admin2 != admin1:
                extra.append(admin2)
            country_display = COUNTRY_NAMES.get(country_code, country_code)
            extra.append(country_display)
            if extra:
                display_full = f"{name} ({', '.join(extra[:2])})"
            else:
                display_full = name
            key = make_city_key(name, lat, lon)
            cities.append({
                "key": key,
                "name": display_name,
                "display_name": display_full,
                "country": country_code,
                "country_name": country_display,
                "admin1": admin1,
                "admin2": admin2,
                "latitude": round(lat, 4),
                "longitude": round(lon, 4),
                "population": item.get("population", 0),
            })
        return cities
    except Exception:
        return []


def get_weather_data(latitude, longitude):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "is_day",
            "precipitation",
            "rain",
            "showers",
            "snowfall",
            "weather_code",
            "cloud_cover",
            "pressure_msl",
            "surface_pressure",
            "wind_speed_10m",
            "wind_direction_10m",
            "wind_gusts_10m",
        ],
        "hourly": [
            "temperature_2m",
            "weather_code",
            "wind_speed_10m",
            "relative_humidity_2m",
        ],
        "daily": [
            "weather_code",
            "temperature_2m_max",
            "temperature_2m_min",
            "sunrise",
            "sunset",
            "uv_index_max",
            "precipitation_sum",
            "rain_sum",
            "showers_sum",
            "snowfall_sum",
            "precipitation_hours",
            "wind_speed_10m_max",
            "wind_gusts_10m_max",
            "wind_direction_10m_dominant",
        ],
        "timezone": "auto",
        "forecast_days": 7,
    }
    url = "https://api.open-meteo.com/v1/forecast"
    try:
        response = requests.get(url, params=params, timeout=15)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception:
        return None


def format_weather_data(raw_data, city_name, country):
    if not raw_data or "current" not in raw_data:
        return None

    current = raw_data["current"]
    daily = raw_data["daily"]
    hourly = raw_data["hourly"]

    current_time = current.get("time", "")
    code = current.get("weather_code", 0)
    weather_info = WEATHER_CODES.get(code, {"description": "未知", "icon": "cloudy", "cyber": "UNKNOWN"})

    now = datetime.now()
    hour = now.hour

    daily_forecast = []
    for i in range(len(daily["time"])):
        d_code = daily["weather_code"][i]
        d_info = WEATHER_CODES.get(d_code, {"description": "未知", "icon": "cloudy", "cyber": "UNKNOWN"})
        date_obj = datetime.fromisoformat(daily["time"][i].replace("Z", ""))
        daily_forecast.append({
            "date": daily["time"][i],
            "day_name": ["周日", "周一", "周二", "周三", "周四", "周五", "周六"][date_obj.weekday()],
            "day_short": date_obj.strftime("%m-%d"),
            "weather_code": d_code,
            "description": d_info["description"],
            "icon": d_info["icon"],
            "cyber": d_info["cyber"],
            "temp_max": round(daily["temperature_2m_max"][i], 1),
            "temp_min": round(daily["temperature_2m_min"][i], 1),
            "precipitation": round(daily["precipitation_sum"][i], 1),
            "wind_speed": round(daily["wind_speed_10m_max"][i], 1),
            "uv_index": daily.get("uv_index_max", [0])[i] if daily.get("uv_index_max") else 0,
        })

    hourly_forecast = []
    now_str = now.strftime("%Y-%m-%dT%H:00")
    start_idx = 0
    for i, t in enumerate(hourly["time"]):
        if t >= now_str:
            start_idx = i
            break

    for i in range(start_idx, min(start_idx + 24, len(hourly["time"]))):
        h_code = hourly["weather_code"][i]
        h_info = WEATHER_CODES.get(h_code, {"description": "未知", "icon": "cloudy", "cyber": "UNKNOWN"})
        time_str = hourly["time"][i]
        hour_obj = datetime.fromisoformat(time_str.replace("Z", ""))
        hourly_forecast.append({
            "time": time_str,
            "hour": hour_obj.strftime("%H:%M"),
            "date": hour_obj.strftime("%m-%d"),
            "temp": round(hourly["temperature_2m"][i], 1),
            "weather_code": h_code,
            "description": h_info["description"],
            "icon": h_info["icon"],
            "cyber": h_info["cyber"],
            "wind_speed": round(hourly["wind_speed_10m"][i], 1),
            "humidity": hourly["relative_humidity_2m"][i],
        })

    return {
        "city": city_name,
        "country": country,
        "latitude": raw_data.get("latitude"),
        "longitude": raw_data.get("longitude"),
        "timezone": raw_data.get("timezone"),
        "current": {
            "time": current_time,
            "temperature": round(current["temperature_2m"], 1),
            "feels_like": round(current["apparent_temperature"], 1),
            "humidity": current["relative_humidity_2m"],
            "wind_speed": round(current["wind_speed_10m"], 1),
            "wind_direction": current["wind_direction_10m"],
            "wind_gusts": round(current["wind_gusts_10m"], 1),
            "precipitation": current["precipitation"],
            "cloud_cover": current["cloud_cover"],
            "pressure": round(current["pressure_msl"], 0),
            "weather_code": code,
            "description": weather_info["description"],
            "icon": weather_info["icon"],
            "cyber": weather_info["cyber"],
            "is_day": current["is_day"],
        },
        "hourly": hourly_forecast,
        "daily": daily_forecast,
        "sunrise": daily["sunrise"][0] if daily.get("sunrise") else "",
        "sunset": daily["sunset"][0] if daily.get("sunset") else "",
        "uv_index": daily.get("uv_index_max", [0])[0] if daily.get("uv_index_max") else 0,
        "query_time": now.strftime("%Y-%m-%d %H:%M:%S"),
        "hour": hour,
    }


@app.route("/")
def index():
    default_city = "beijing"
    city_info = POPULAR_CITIES.get(default_city)
    raw_data = get_weather_data(city_info["latitude"], city_info["longitude"])
    weather = format_weather_data(raw_data, city_info["name"], city_info["country"])
    return render_template("index.html", weather=weather, city_key=default_city)


@app.route("/art")
def art():
    # CyberWeather2077 - 数据诗学艺术实验页面
    # 默认使用北京天气，前端通过现有 /api/weather 动态更新
    # 关键：强制禁止浏览器 + 任何中间层缓存，确保用户每次都能拉到最新版
    resp = make_response(render_template("art.html"))
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0, private"
    resp.headers["Pragma"]        = "no-cache"
    resp.headers["Expires"]       = "0"
    resp.headers["Last-Modified"] = ""   # 避免 If-Modified-Since 命中 304
    return resp


@app.route("/api/weather")
def api_weather():
    city_key = request.args.get("city", "beijing").strip()
    latitude = request.args.get("lat")
    longitude = request.args.get("lon")
    city_name = request.args.get("name")
    country = request.args.get("country", "")

    if latitude and longitude:
        lat = float(latitude)
        lon = float(longitude)
        display_name = city_name if city_name else f"{lat:.2f}, {lon:.2f}"
    else:
        city_info = POPULAR_CITIES.get(city_key)
        if not city_info:
            return jsonify({"error": "城市未找到"}), 404
        lat = city_info["latitude"]
        lon = city_info["longitude"]
        display_name = city_info["name"]
        country = city_info.get("country", "")

    country_display = COUNTRY_NAMES.get(country, country)
    raw_data = get_weather_data(lat, lon)
    weather = format_weather_data(raw_data, display_name, country_display)
    if not weather:
        return jsonify({"error": "获取天气数据失败，请检查网络连接"}), 500
    return jsonify(weather)


@app.route("/api/search")
def api_search():
    query = request.args.get("q", "").strip()
    if len(query) < 1:
        return jsonify({"results": []})

    results = geocode_search(query, count=15)
    if not results:
        alt_results = []
        q = query.lower()
        for key, city in POPULAR_CITIES.items():
            if q in city["name"].lower() or q in key:
                alt_results.append({
                    "key": key,
                    "name": city["name"],
                    "display_name": f'{city["name"]} ({COUNTRY_NAMES.get(city["country"], city["country"])})',
                    "country": city["country"],
                    "country_name": COUNTRY_NAMES.get(city["country"], city["country"]),
                    "admin1": "",
                    "admin2": "",
                    "latitude": city["latitude"],
                    "longitude": city["longitude"],
                    "population": 0,
                })
        return jsonify({"results": alt_results, "source": "local"})
    return jsonify({"results": results, "source": "geocoding"})


@app.route("/api/cities")
def api_cities():
    cities = []
    for key, city in POPULAR_CITIES.items():
        cities.append({
            "key": key,
            "name": city["name"],
            "country": city["country"],
            "country_name": COUNTRY_NAMES.get(city["country"], city["country"]),
            "latitude": city["latitude"],
            "longitude": city["longitude"],
        })
    return jsonify({"cities": cities})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)
