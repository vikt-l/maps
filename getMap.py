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

    temps = []
    dates = []
    winds = []
    humiditys = []
    pressures = []
    precs = []
    for i in range (1, 7):
        dates.append(f"{weather['forecasts'][i]['date']}")
        temps.append(f"{weather['forecasts'][i]['parts']['day']['temp_avg']}")
        winds.append(f"{weather['forecasts'][i]['parts']['day']['wind_speed']}")
        humiditys.append(f"{weather['forecasts'][i]['parts']['day']['humidity']}")
        pressures.append(f"{weather['forecasts'][i]['parts']['day']['pressure_mm']}")
        if weather['forecasts'][i]['parts']['day']['prec_strength'] == 0:
            precs.append('Осадки: Без осадков')
        elif weather['forecasts'][i]['parts']['day']['prec_strength'] == 0.25:
            precs.append(f"Осадки: Слабый {prec[weather['forecasts'][i]['parts']['day']['prec_type']]}")
        elif weather['forecasts'][i]['parts']['day']['prec_strength'] == 0.5:
            precs.append(f"Осадки: {prec[weather['forecasts'][i]['parts']['day']['prec_type']]}")
        elif weather['forecasts'][i]['parts']['day']['prec_strength'] == 0.75:
            precs.append(f"Осадки: Сильный {prec[weather['forecasts'][i]['parts']['day']['prec_type']]}")
        elif weather['forecasts'][i]['parts']['day']['prec_strength'] == 1:
            precs.append(f"Осадки: Очень сильный {prec[weather['forecasts'][i]['parts']['day']['prec_type']]}")
