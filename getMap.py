import requests


def get_weather(lons, lats):
    lons = lons
    lats = lats
    url_yandex = f'https://api.weather.yandex.ru/v2/forecast/?lat={lons}&lon={lats}&[lang=ru_RU]'
    yandex_req = requests.get(url_yandex, headers={'X-Yandex-API-Key': 'b5abe2c2-418a-405e-9cce-d1e7d1a2505a'})
    weather = yandex_req.json()
    precs = ['без осадков', 'дождь', 'дождь со снегом', 'снег', 'град']
    temp = weather['fact']['temp']
    wind_speed = weather['fact']['wind_speed']
    humidity = weather['fact']['humidity']
    pressure_mm = weather['fact']['pressure_mm']
    if weather['fact']['prec_strength'] == 0:
        prec = "Без осадков"
    elif weather['fact']['prec_strength'] == 0.25:
        prec = f"Слабый {precs[weather['fact']['prec_type']]}"
    elif weather['fact']['prec_strength'] == 0.5:
        prec = f"{precs[weather['fact']['prec_type']]}"
    elif weather['fact']['prec_strength'] == 0.75:
        prec = f"Сильный {precs[weather['fact']['prec_type']]}"
    elif weather['fact']['prec_strength'] == 1:
        prec = f"Очень сильный {precs[weather['fact']['prec_type']]}"