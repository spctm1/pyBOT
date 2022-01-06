import requests
import datetime
from config import open_weather_token, token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Введи название города и получи сводку о погоде в ответ!")
   
   
   
@dp.message_handler()    
async def get_weather(message: types.Message):
    code_to_smile = {
        "CLear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Идет дождь \U00002614",
        "Drizzle": "Идет дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow" : "Идет снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"        
            )
        data = r.json()

        
        city = data["name"]
        cur_temp = data["main"]["temp"]
        
        weaether_description = data["weather"][0]["main"]
        if weaether_description in code_to_smile:
            wd = code_to_smile[weaether_description]
        else:
            wd = "Посмотрите в окно, возможна метель, буря, торнадо!"
        
        max_daily_temp = data["main"]["temp_max"]
        min_daily_temp = data["main"]["temp_min"]
        humidity = data["main"]["humidity"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        lenght_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        wind = data["wind"]["speed"]
        
        await message.reply(
            f"Погода на сегодня в городе: {city}\n{wd}\n\nТемпература на данный момент: {cur_temp}°C\n"
            f"Максимальная температура: {max_daily_temp}°C\nМинимальная температура: {min_daily_temp}°C\n\n"
            f"Время восхода солнца: {sunrise_timestamp}\nВремя захода солнца: {sunset_timestamp}\n"
            f"Продолжительность дня составляет: {lenght_of_the_day}\n\n"
            f"Процент влажности составляет: {humidity}%\nСкорость ветра составляет: {wind} м/с\n\n"
            f"Хорошего дня!")
        
    except:
        await message.reply("Проверьте название города!")
    
if __name__ == '__main__':
    executor.start_polling(dp)