#!/usr/bin/python3.6
#coding:utf-8

"""
@author: Ante Liu
@contact: robotliu0327@gmail.com
@software: PyCharm
@file: send_iphone.py
@time: 12/3/2022 12:15 AM
"""
# coding: utf-8
import warnings
# warnings.filterwarnings('ignore')
from urllib import request
import datetime,requests,string,re
from urllib.parse import quote

str1 = '川和路399弄（张江兴科苑）/11-12号/04楼/403<>所属区域：张江镇<>0 月租金<>2022-12-03 01:05:42.043579'
str1 = re.sub('[^\u4e00-\u9fa5^a-z^A-Z^0-9]','',str1)
url = "https://api.day.app/65H5UU3wpmLwSAzxn7PVb6/%s?group=%s" % (str1,'公租房')

"""响应"""
# 范围时间
d_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '00:30', '%Y-%m-%d%H:%M')
d_time1 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '01:34', '%Y-%m-%d%H:%M')
n_time = datetime.datetime.now()

# 判断当前时间是否在范围时间内
if n_time > d_time and n_time < d_time1:

    resp = requests.get(url)
    print(url)
else:
    print(1212)