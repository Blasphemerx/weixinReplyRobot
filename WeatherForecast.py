from urllib.request import urlopen
import urllib
import json

WEATHER_FORECAST_URL = "http://t.weather.sojson.com/api/weather/city/"
WEATHER_TODAY_FORMAT = "日期：{0}， 湿度：{1}， PM2.5：{2}， PM10：{3}， 空气质量：{4}， 温度：{5}， 建议：{6}"
WEATHER_FORECAST_FORMAT = "日期：{0}， 日出时间：{1}， 最高温度：{2}， 最低温度：{3}， 日落时间：{4}， 空气指数：{5}， 风向：{6}， 风力：{7}， 天气：{8}， 建议：{9}"


class WeatherForecast:

    def __init__(self, city):
        if city is None or city == "":
            city = "101010100"
        self.url = WEATHER_FORECAST_URL + city
        self.ret_str = ""

    def get_weather_info(self):
        try:
            req = urlopen(self.url)
            info = json.loads(req.read())
        except urllib.error.URLError:
            print("暂时无法查询天气，请稍后再试！")
            return "暂时无法查询天气，请稍后再试！"
        if info.get("status") == 200:
            today_weather = info["data"]
            message_today_weather = WEATHER_TODAY_FORMAT.format(info.get("date"), today_weather.get("shidu"), today_weather.get("pm25"), today_weather.get("pm10"), today_weather.get("quality"), today_weather.get("wendu"), today_weather.get("ganmao"))
            print(message_today_weather)
            self.ret_str += message_today_weather + "\n"

            forecast_weathers = today_weather.get("forecast")
            for forecast_weather in forecast_weathers:
                message_forecast_weather = WEATHER_FORECAST_FORMAT.format(forecast_weather.get("date"), forecast_weather.get("sunrise"), forecast_weather.get("high"), forecast_weather.get("low"), forecast_weather.get("sunset"), forecast_weather.get("aqi"), forecast_weather.get("fx"), forecast_weather.get("fl"), forecast_weather.get("type"), forecast_weather.get("notice"))
                print(message_forecast_weather)
                self.ret_str += message_forecast_weather + "\n"
            return self.ret_str

        elif info.get("status") == 500:
            print(info.get("message"))
            return info.get("message")
        else:
            print(info.get("message"))
            return info.get("message")
