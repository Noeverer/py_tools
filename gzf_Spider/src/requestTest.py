#!/usr/bin/python3.6
#coding:utf-8

"""
@author: Ante Liu
@contact: robotliu0327@gmail.com
@software: PyCharm
@file: requestTest.py
@time: 12/2/2022 9:18 PM
"""

# -*- coding: utf-8 -*-

import requests

userAgent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
header = {
    # "origin": "https://passport.mafengwo.cn",
    "Referer": "https://select.pdgzf.com/houseLists",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'Content-Type': 'application/json',
    'token': 'LGWMRELGC1R9G6Q9BBBBXCJYQKJSK9EB',
    'signature': '1JEGVLYVDGBDVCTSCJEM28MMA4N8B1EY'
}


def mafengwoLogin(account, password):
    # 马蜂窝模仿 登录
    print("开始模拟登录马蜂窝")

    postUrl = "https://miao.baidu.com/abdr?_o=https%3A%2F%2Fselect.pdgzf.com"
    # postData = {"where":
    #                 {"keywords":"",
    #                  "township":"null",
    #                  "projectId":"null",
    #                  "typeName":"null",
    #                  "rent":"null"},
    #             "pageIndex":0,"pageSize":10}

    postData = {'_o': 'https://select.pdgzf.com'}
    responseRes = requests.post(postUrl, data=postData, headers=header)
    # 无论是否登录成功，状态码一般都是 statusCode = 200
    print(f"statusCode = {responseRes.status_code}")
    print(f"text = {responseRes.text}")


if __name__ == "__main__":
    # 从返回结果来看，有登录成功
    mafengwoLogin("13756567832", "000000001")




