from django_ratelimit.decorators import ratelimit
from django.shortcuts import render
from requests import get
import json
from GetCurrentUSD.models import *

def main_page(request):
    return render(request, 'main.html')


@ratelimit(key='ip', rate='1/10s', block=False)
def get_current_usd(request):
    """
    Функция обрабатывает GET запрос "/get-current-usd/"
    GET - актуальный курс доллара к рублю в формате JSON и 10 последних запросов курсов.
    Между каждым запросом предусмотрена пауза минимум 10 секунд.
    """
    if getattr(request, 'limited', False):
        context = {
            'json': 'Превышен лимит запросов, повторите через 10 секунд.',
        }
    else:
        _list = []
        data = request_usd()

        for i in USD.objects.all():
            _list.append(i.Value)

        USD.objects.create(Time=data['Date'], Value=data['Valute']['USD']['Value'])
        rate = {'ValueUSD': data['Valute']['USD']['Value'], 'CurrentDataTime': data['Date'], 'LastValue': _list[-10::]}

        context = {
            'json': json.dumps(rate),
        }
    return render(request, 'get_current_usd.html', context)


def request_usd():
    """
    Функция направляет запрос API ЦБ и возвращает "слайс" ответа с волютой USD.
    """
    response = get(url='https://www.cbr-xml-daily.ru/daily_json.js')
    result = json.loads(response.text)
    return result
