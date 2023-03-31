import requests
from pprint import pprint


city = input('Введите название населенного пункта ')
geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={city}" \
                   f"&format=json"

response = requests.get(geocoder_request)
if response:
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    lats = toponym_coodrinates.split()[0]
    lons = toponym_coodrinates.split()[1]
else:
    print("Ошибка выполнения запроса:")
    print(geocoder_request)
    print("Http статус:", response.status_code, "(", response.reason, ")")


url_yandex = f'https://api.weather.yandex.ru/v2/forecast/?lat={lons}&lon={lats}&[lang=ru_RU]'
yandex_req = requests.get(url_yandex, headers={'X-Yandex-API-Key': 'b5abe2c2-418a-405e-9cce-d1e7d1a2505a'})
weather = yandex_req.json()
prec = ['без осадков', 'дождь', 'дождь со снегом', 'снег', 'град']
print(f"Город: {weather['info']['url']}")
print(f"Температура: {weather['fact']['temp']}°C")
print(f"Ощущаемая температура: {weather['fact']['feels_like']}°C")
print(f"Скорость ветра: {weather['fact']['wind_speed']}м/с")
print(f"Скорость порывов ветра: {weather['fact']['wind_gust']}м/с")
print(f"Влажность: {weather['fact']['humidity']}%")
if weather['fact']['prec_strength'] == 0:
    print('Осадки: Без осадков')
elif weather['fact']['prec_strength'] == 0.25:
    print(f"Осадки: Слабый {prec[weather['fact']['prec_type']]}")
elif weather['fact']['prec_strength'] == 0.5:
    print(f"Осадки: {prec[weather['fact']['prec_type']]}")
elif weather['fact']['prec_strength'] == 0.75:
    print(f"Осадки: Сильный {prec[weather['fact']['prec_type']]}")
elif weather['fact']['prec_strength'] == 1:
    print(f"Осадки: Очень сильный {prec[weather['fact']['prec_type']]}")

