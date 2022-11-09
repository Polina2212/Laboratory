import requests

city = "Moscow, RU"
appid = "07df54970140a8e6c0160e19b889c1d5"
res = requests.get("http://api.openweathermap.org/data/2.5/weather",
    params={'q': city, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
data1 = res.json()

print("Москва:", city)
print("Погодные условия:", data1['weather'][0]['description'])
print("Температура:", data1['main']['temp'])
print("Минимальная температура:", data1['main']['temp_min'])
print("Максимальная температура", data1['main']['temp_max'])
print("Скорость ветра", data1['wind']['speed'])
print("Видимость", data1['visibility'])

res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
    params={'q': city, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
data2 = res.json()

print("Прогноз погоды на неделю:")
for i in data2['list']:
    print("Дата <", i['dt_txt'], "> \r\nТемпература <", '{0:+3.0f}'.format(i['main']['temp']),
            "> \r\nПогодные условия <", i['weather'][0]['description'], ">")
    print("Скорость ветра <", i['wind']['speed'], "> \r\nВидимость <", i['visibility'],">")
