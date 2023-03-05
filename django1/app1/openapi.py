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

def onenet(request):
    return JsonResponse({'status': 'ok'})