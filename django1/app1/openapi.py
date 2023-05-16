# Create your views here.
from django.http import HttpResponse,JsonResponse

import datetime
import os
import json
import base64
import requests

from app1.models import * #引用

# 剪贴板
def test(request):
    return JsonResponse({'status': 'ok'})

def trigger(request, type=''):
    print(type)
    recv_json = request.POST.dict() or request.GET.dict() or json.loads(request.body)
    if type == 'onenet':
        # onenet 触发器
        # {'trigger': {'id': 1672193, 'threshold': 1, 'type': '=='}, 'current_data': [{'user_id': 234533, 'dev_id': '1048953737', 'ds_id': 'data0', 'at': '2023-05-16 22:23:49.580', 'value': 1}]}
        id = recv_json['id']
        current_data = recv_json['current_data'][0]
        ds_id = current_data['ds_id']
        value = current_data['value']
        at_time = current_data['at']

    return JsonResponse({'status': 'ok'})

