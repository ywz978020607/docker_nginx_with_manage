# Create your views here.
# 敏感信息使用数据库存储-注意nginx权限不要让数据库能够直接访问
# 1.email
# python manage.py shell
# from app1.models import *
# TextKeyVal.objects.create(keyname="email_api", value="xxx@qq.com,xxxx")
# 2.location
# from app1.models import *
# TextKeyVal.objects.create(keyname="xxxgps_idxxx", value=json.dumps({"name": "xx车","target":[lat,lon], "cmd_id":"xxx", "api_key":"xxx", "dis": 1000}))
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

#########################
# onenet
#cmd
def send_onenet_cmd(device_id, api_key, key_name = "data0", action = "t_off", period = 1):
    url = "http://api.heclouds.com/cmds?device_id=" + device_id
    headers={'api-key': api_key}
    downdata = {
        "key_name": key_name,
        "action": action,
        "period": period
    }
    res = requests.post(url, headers=headers, data=json.dumps(downdata))
    cnt = 0
    while json.loads(res.text).get('errno', 0) != 0 and cnt < 3:
        print("error: {}, resent waiting...".format(json.loads(res.text)))
        time.sleep(3)
        res = requests.post(url, headers=headers, data=json.dumps(downdata))
        cnt += 1

# #status
# def check_status(device_id):
#     url = "http://api.heclouds.com/devices/" + device_id
#     res = requests.get(url, headers=headers)
#     name = res.json()['data']['auth_info']
#     online_status = res.json()['data']['online']
#     last_time = res.json()['data']['last_ct']
#     return res.json()['data']

# def check_latest_datapoints(device_id):
#     #datapoints
#     url="http://api.heclouds.com/devices/{}/datapoints".format(device_id)
#     r=requests.get(url,headers=headers)
#     latest_val = r.json()['data']['datastreams'][0]['datapoints'][0]['value']
#     last_time = r.json()['data']['datastreams'][0]['datapoints'][0]['at']
#     return r.json()['data']['datastreams'][0]['datapoints']

# def check_datastream(device_id, stream_id, limit = 1):
#     url="http://api.heclouds.com/devices/{}/datapoints?datastream_id={}&limit={}".format(device_id, stream_id, limit)
#     r=requests.get(url,headers=headers)
#     # print(r.json()['data']['datastreams'][0]['datapoints'])
#     return r.json()['data']['datastreams'][0]['datapoints']


# dis
from math import sin, asin, cos, radians, fabs, sqrt
EARTH_RADIUS = 6371  # 地球平均半径，6371km
def hav(theta):
    s = sin(theta / 2)
    return s * s
def get_distance_hav(lat0, lng0, lat1, lng1):
    """用haversine公式计算球面两点间的距离。"""
    # 经纬度转换成弧度
    lat0 = radians(lat0)
    lat1 = radians(lat1)
    lng0 = radians(lng0)
    lng1 = radians(lng1)
    dlng = fabs(lng0 - lng1)
    dlat = fabs(lat0 - lat1)
    h = hav(dlat) + cos(lat0) * cos(lat1) * hav(dlng)
    distance = 2 * EARTH_RADIUS * asin(sqrt(h))
    return distance 
# print(get_distance_hav(30.28708, 120.12802999999997, 28.7427, 115.86572000000001))
#########################




#########################
# entrance
#########################
# 剪贴板
def test(request):
    return JsonResponse({'status': 'ok'})

def trigger(request, type=''):
    print(type)
    recv_json = request.POST.dict() or request.GET.dict() or json.loads(request.body)
    print(recv_json)

    # onenet 触发器 m, r, t
    if type == 'onenet' and False:
        mode = request.GET.dict().get("r", "")
        to_emails = request.GET.dict().get("r", "").split(",")
        text = request.GET.dict().get("t", "")
        print("onenet send email", to_emails, text)
        # {'trigger': {'id': 1672193, 'threshold': 1, 'type': '=='}, 'current_data': [{'user_id': 234533, 'dev_id': '1048953737', 'ds_id': 'data0', 'at': '2023-05-16 22:23:49.580', 'value': 1}]}
        current_data = recv_json['current_data'][0]
        ds_id = current_data['ds_id']
        value = current_data['value']
        at_time = current_data['at']
        print(ds_id, value)
        if mode == "location":
            db_find_device = TextKeyVal.objects.filter(keyname=ds_id)
            if db_find_device:
                device_info = json.loads(db_find_device[0].value)
                now_dis = get_distance_hav(value['lat'],value['lon'],device_info["target"][0],device_info["target"][1]) * 1000
                # if now_dis < 50 and device_info["dis"] >= 50:
                if now_dis < 50:
                    print("触发一次")
                    send_onenet_cmd(device_info["cmd_id"], device_info["api_key"])
                    send_email_api = TextKeyVal.objects.filter(keyname="email_api")
                    if to_emails and text and send_email_api:
                        send_email(to_emails, device_info["name"] + text, send_email_api[0].value.split(",")[0], send_email_api[0].value.split(",")[1])
                device_info["dis"] = now_dis
                db_find_device[0].value = json.dumps(device_info)
                db_find_device[0].save()

    elif type == 'email':
        to_emails = request.GET.dict().get("r", "")
        text = request.GET.dict().get("t", "")
        print("send email", to_emails, text)
        send_email_api = TextKeyVal.objects.filter(keyname="email_api")
        if to_emails and text and send_email_api:
            send_email(to_emails, text, send_email_api[0].value.split(",")[0], send_email_api[0].value.split(",")[1])

    return JsonResponse({'status': 'ok'})

