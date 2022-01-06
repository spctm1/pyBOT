from os import name
import datetime
import config
from config import open_weather_token
from pprint import pprint
import telebot
import requests

def get_weather(city, get_weather_token):
    
    code_to_smile = {
        "CLear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow" : "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
        }
    
    
    
    
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        #pprint(data)
        
        city = data["name"]
        cur_temp = data["main"]["temp"]
        
        weaether_description = data["weather"][0]["main"]
        if weaether_description in code_to_smile:
            wd = code_to_smile[weaether_description]
        else:
            wd = "Посмотрите в окно, возможно катастрофическое явление!"
        
        max_daily_temp = data["main"]["temp_max"]
        min_daily_temp = data["main"]["temp_min"]
        humidity = data["main"]["humidity"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        lenght_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        wind = data["wind"]["speed"]
        
        print(f"*****{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}*****\n"
              f"Погода в городе: {city}\n {wd} Температура на данный момент: {cur_temp}°C\n"
              f"Максимальная температура: {max_daily_temp}°C\n Минимальная температура: {min_daily_temp}°C\n"
              f"Время восхода солнца: {sunrise_timestamp}\n Время захода солнца: {sunset_timestamp}\n"
              f"Продолжительность дня составляет: {lenght_of_the_day}\n"
              f"Процент влажности составляет: {humidity}%\n Скорость ветра составляет: {wind} м/с\n"
              f"")
        
    except Exception as ex:
            print(ex)
            print("Проверьте название города!")

def main():
    city = input("Введите город: ")
    get_weather(city, open_weather_token)
    
