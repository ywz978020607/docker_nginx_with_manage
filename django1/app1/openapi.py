# Create your views here.
from django.http import HttpResponse,JsonResponse

import datetime
import os
import json
import base64
import requests

from app1.models import * #引用
from smtplib import SMTP, SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText
def send_email(receivers,alert_context, send_email, api_key):
	# 请自行修改下面的邮件发送者和接收者
	sender = send_email  # 发送者的邮箱地址
	# receivers = [receiver]  # 接收者的邮箱地址
	message = MIMEText('Alert:'+str(alert_context), _subtype='plain', _charset='utf-8')
	message['From'] = sender #Header(sender, 'utf-8')  # 邮件的发送者
	message['To'] = Header('Hello', 'utf-8')  # 邮件的接收者
	message['Subject'] = Header(alert_context, 'utf-8')  # 邮件的标题
	# smtper = SMTP('smtp.qq.com',465)
	smtper = SMTP_SSL("smtp.qq.com", 465)
	# 请自行修改下面的登录口令
	smtper.login(sender, api_key)  # QQ邮箱smtp的授权码
	smtper.sendmail(sender, receivers, message.as_string())
	print('邮件发送完成!')

# 剪贴板
def test(request):
    return JsonResponse({'status': 'ok'})

def trigger(request, type=''):
    print(type)
    recv_json = request.POST.dict() or request.GET.dict() or json.loads(request.body)
    print(recv_json)

    if type == 'onenet':
        # onenet 触发器
        # {'trigger': {'id': 1672193, 'threshold': 1, 'type': '=='}, 'current_data': [{'user_id': 234533, 'dev_id': '1048953737', 'ds_id': 'data0', 'at': '2023-05-16 22:23:49.580', 'value': 1}]}
        id = recv_json['id']
        current_data = recv_json['current_data'][0]
        ds_id = current_data['ds_id']
        value = current_data['value']
        at_time = current_data['at']

    elif type == 'email':
        to_emails = request.GET.dict().get("r", "")
        text = request.GET.dict().get("t", "")
        print("send email", to_emails, text)
        send_email_api = TextKeyVal.objects.filter(keyname="email_api")
        # python manage.py shell
        # from app1.models import *
        # TextKeyVal.objects.create(keyname=keyname, value=value)
        if to_emails and text and send_email_api:
            send_email(to_emails, text, send_email_api[0].value.split(",")[0], send_email_api[0].value.split(",")[1])

    return JsonResponse({'status': 'ok'})

