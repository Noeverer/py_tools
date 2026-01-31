
#!/usr/bin/python3.6
#coding:utf-8

"""
@author: Ante Liu
@contact: robotliu0327@gmail.com
@software: PyCharm
@file: git_publichouse.py
@time: 12/2/2022 10:47 PM
"""


# coding=utf-8
import requests
from bs4 import BeautifulSoup
import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

suport_type = '供应对象：家庭'
need = ['东书房路',
        '永泰路',
        '公租房艾东苑',
        '浦三路',
        '上南路']

pageSize = 15


header = {
    'Referer': 'http://select.pdgzf.com/Index.aspx?qy=',
    'Cookie': 'ASP.NET_SessionId=jwo5eqenqz3eh0oo33eb5302'
}

URL = 'http://select.pdgzf.com/Admin/personalUser.aspx?qy=&'



def getHouseName(page, cookie):
    url = URL+'page='+str(page)
    print ('url:'+url)
    session = requests.session()
    header['Cookie'] = cookie
    sessionResult = session.get(url, headers=header)
    soup = BeautifulSoup(sessionResult.content, "html.parser")
    house_list_soup = soup.find('ol', attrs={'class': 'list'})
    house_list = house_list_soup.find_all('li')
    size = len(house_list)
    for house in house_list:
        name = house.span.next
        if not check(name, page):
            continue
        return name
    if(size == pageSize):
        return getHouseName(page+1, cookie)


def check(name, page):
    house_type = name.next.next.next.next.next.next.next.next.next.next
    print ('第%s页，%s，房源:%s' % (page, house_type, name))
    for support in need:
        if support in name and house_type == suport_type:
            return True
    return False

getHouseName(pageSize)