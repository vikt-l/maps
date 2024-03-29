import requests
from PIL import Image
from io import BytesIO

# # пример данных для поиска
# toponym_longitude = 37.617188
# toponym_lattitude = 55.755713
# delta = 21
# text = 'аптека'
# toponym_to_find = 'Москва, Театральная пл.'


def get_info(toponym_longitude, toponym_lattitude, delta):
    try:
        # получить карту по координатам
        map_params = {
            "ll": ",".join([str(toponym_longitude), str(toponym_lattitude)]),
            "spn": ",".join([str(delta), str(delta)]),
            "l": "map"
        }

        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)
        im = Image.open(BytesIO(response.content))
        im.resize((720, 720))
        im.save('static/img/map.png')
        return 'static/img/map.png'
    except Exception:
        return 'static/img/default_img.png'


def get_address(toponym_to_find, delta):
    try:
        # получить карту по адресу
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": toponym_to_find,
            "format": "json"}

        response = requests.get(geocoder_api_server, params=geocoder_params)

        if not response:
            pass
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"]
        toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
        toponym_index = toponym["metaDataProperty"]["GeocoderMetaData"]['Address']

        map_params = {
            "ll": ",".join([str(toponym_longitude), str(toponym_lattitude)]),
            "spn": ",".join([str(delta), str(delta)]),
            "l": "map",
        }

        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)

        im = Image.open(BytesIO(response.content))
        im.resize((720, 720))
        im.save('static/img/map.png')
        return 'static/img/map.png', toponym_longitude, toponym_lattitude
    except Exception:
        return 'static/img/default_img.png'



def get_weather(lons, lats):
    try:
        url_yandex = f'https://api.weather.yandex.ru/v2/forecast/?lat={lons}&lon={lats}&[lang=ru_RU]'
        yandex_req = requests.get(url_yandex, headers={'X-Yandex-API-Key': 'b5abe2c2-418a-405e-9cce-d1e7d1a2505a'})
        weather = yandex_req.json()
        precs = ['без осадков', 'дождь', 'дождь со снегом', 'снег', 'град']

        prognoz1 = []

        for i in range(0, 3):
            weth = {}
            weth['dates'] = f"{weather['forecasts'][i]['date']}"
            weth['temp'] = f"{weather['forecasts'][i]['parts']['day']['temp_avg']}"
            weth['wind'] = f"{weather['forecasts'][i]['parts']['day']['wind_speed']}"
            weth['humidity'] = f"{weather['forecasts'][i]['parts']['day']['humidity']}"
            weth['pressure'] = f"{weather['forecasts'][i]['parts']['day']['pressure_mm']}"
            if weather['forecasts'][i]['parts']['day']['prec_strength'] == 0:
                weth['prec'] = 'Осадки: Без осадков'
            elif weather['forecasts'][i]['parts']['day']['prec_strength'] == 0.25:
                weth['prec'] = f"Осадки: Слабый {precs[weather['forecasts'][i]['parts']['day']['prec_type']]}"
            elif weather['forecasts'][i]['parts']['day']['prec_strength'] == 0.5:
                weth['prec'] = f"Осадки: {precs[weather['forecasts'][i]['parts']['day']['prec_type']]}"
            elif weather['forecasts'][i]['parts']['day']['prec_strength'] == 0.75:
                weth['prec'] = f"Осадки: Сильный {precs[weather['forecasts'][i]['parts']['day']['prec_type']]}"
            elif weather['forecasts'][i]['parts']['day']['prec_strength'] == 1:
                weth['prec'] = f"Осадки: Очень сильный {precs[weather['forecasts'][i]['parts']['day']['prec_type']]}"
            prognoz1.append(weth)

        prognoz2 = []

        for i in range(3, 6):
            weth = {}
            weth['dates'] = f"{weather['forecasts'][i]['date']}"
            weth['temp'] = f"{weather['forecasts'][i]['parts']['day']['temp_avg']}"
            weth['wind'] = f"{weather['forecasts'][i]['parts']['day']['wind_speed']}"
            weth['humidity'] = f"{weather['forecasts'][i]['parts']['day']['humidity']}"
            weth['pressure'] = f"{weather['forecasts'][i]['parts']['day']['pressure_mm']}"
            if weather['forecasts'][i]['parts']['day']['prec_strength'] == 0:
                weth['prec'] = 'Осадки: Без осадков'
            elif weather['forecasts'][i]['parts']['day']['prec_strength'] == 0.25:
                weth['prec'] = f"Осадки: Слабый {precs[weather['forecasts'][i]['parts']['day']['prec_type']]}"
            elif weather['forecasts'][i]['parts']['day']['prec_strength'] == 0.5:
                weth['prec'] = f"Осадки: {precs[weather['forecasts'][i]['parts']['day']['prec_type']]}"
            elif weather['forecasts'][i]['parts']['day']['prec_strength'] == 0.75:
                weth['prec'] = f"Осадки: Сильный {precs[weather['forecasts'][i]['parts']['day']['prec_type']]}"
            elif weather['forecasts'][i]['parts']['day']['prec_strength'] == 1:
                weth['prec'] = f"Осадки: Очень сильный {precs[weather['forecasts'][i]['parts']['day']['prec_type']]}"
            prognoz2.append(weth)

        return prognoz1, prognoz2
    except Exception:
        return False, False
            
            
def get_obj(toponym_longitude, toponym_lattitude, text, delta):
    try:
        # ищет ближайший указанный объект
        search_api_server = "https://search-maps.yandex.ru/v1/"
        api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

        address_ll = ",".join([str(toponym_longitude), str(toponym_lattitude)])

        search_params = {
            "apikey": api_key,
            "text": text,
            "lang": "ru_RU",
            "ll": address_ll,
            "type": "biz"
        }

        response = requests.get(search_api_server, params=search_params)

        if response:
            json_response = response.json()

            organization = json_response["features"][0]
            org_address = organization["properties"]["CompanyMetaData"]["address"]
            number = org_address[org_address.rfind(','):]
            point = organization["geometry"]["coordinates"]
            org_point = "{0},{1}".format(point[0], point[1])

            map_params = {
                "ll": org_point,
                "spn": ",".join([str(delta), str(delta)]),
                "l": "map",
                "pt": "{0},pm2dgl".format(org_point)
            }

            map_api_server = "http://static-maps.yandex.ru/1.x/"
            response = requests.get(map_api_server, params=map_params)

            im = Image.open(BytesIO(response.content))
            im.resize((720, 720))
            im.save('static/img/map.png')
            return 'static/img/map.png', point[0], point[1]
    except Exception:
        return 'static/img/default_img.png'
