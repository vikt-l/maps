import http.client, re, time
conn = http.client.HTTPSConnection("yandex.ru")
conn.request("GET", "/pogoda/moscow")
response = conn.getresponse()
str_resp = response.read().decode("utf-8")
for i in range(1, 9):
    day1Html = re.search(r'<li class="forecast-brief__item day-anchor i-bem" data-bem="{&quot;day-anchor&quot;:{&quot;anchor&quot;:\d*?,&quot;dayIndex&quot;:'+str(i)+'}}">(.+)<\/li>',str_resp).group(1)
    day1Day = re.search(r'<span class="forecast-brief__item-day-name">(.+?)</span>',day1Html).group(1)
    day1Result = re.search(r'<div class="forecast-brief__item-temp-day" title="Максимальная температура днём">(.+?)<\/div>', day1Html).group(1)
    print(day1Day,day1Result)