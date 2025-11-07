# -*- coding: utf-8 -*-
import requests
import hashlib
import time
import json
import random


class Youdao(object):
    def __init__(self, msg):
        self.msg = msg
        self.url = 'https://select.pdgzf.com/api/v1.0/app/gzf/project/list'
        # self.D = "ebSeFb%=XZ%T[KZ)c(sy!"
        # self.salt = self.get_salt()
        # self.sign = self.get_sign()

    # def get_md(self, value):
    #     '''md5加密'''
    #     m = hashlib.md5()
    #     # m.update(value)
    #     m.update(value.encode('utf-8'))
    #     return m.hexdigest()
    #
    # def get_salt(self):
    #     '''根据当前时间戳获取salt参数'''
    #     s = int(time.time() * 1000) + random.randint(0, 10)
    #     return str(s)
    #
    # def get_sign(self):
    #     '''使用md5函数和其他参数，得到sign参数'''
    #     s = "fanyideskweb" + self.msg + self.salt + self.D
    #     return self.get_md(s)


    def get_result(self):
        '''headers里面有一些参数是必须的，注释掉的可以不用带上'''
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            # 'Accept-Encoding': 'gzip, deflate',
            # 'Accept-Language': 'zh-CN,zh;q=0.9,mt;q=0.8',
            # 'Connection': 'keep-alive',
            # 'Content-Length': '240',
            # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'HWWAFSESID=2bc307367582cf4caa; HWWAFSESTIME=1669905528875; JSESSIONID=EF554E21FBADD6F26BE11DC1A1A49E54; LeSoft_V9_LoginUserKey=27CF9DAC4962C155FA5775F6597184221F3DC6A88B0A5DFE1F0D108964411A14011B210609458F3BA010C2449EB88AF522D84ADAD197516C7C1659FD1BDA6D0E1A0B589D1C69BF28A36C54B0435B334E3E7DEC6008D8854514287C1913A04E85EC1FBB1A77E9B9259661560E21D651032A671BDEFF8FDA8928AF8736A5B85C9C983AEAD01D7420BC6CA305C1008FC521CFA23C56B711D3DA63E2712F630A386C0D4DB1F08AF1AEBDB30C25D1F48B51C54226081ABABA317CC8D7D5785A46227244EA8D32B4A658356F4F48D5763B5B691DF72B5C3E4F16C93D03E006908238C12415C8668316B5FF2D23963625D9920D6F7D231E36B364E9BDA8FB46F76B9132B613AB10A3250434A4909C2AC25D435274D86A6230B07DBCFF02A91FAF3576001F1979489C13CCDB42C0607E0FE256B042EE8F884C5264863B9534C440DE01CC62E9BDBDE976EEE9AA62245EA2F363F3A746DA9AA7339C30E08010757FADA9A2CC8B0D092153D58F9327DB17AC6F3083DE6B6E15891A49B97CA83121C4EC52A76A40BFB015AA91D60037F761C8E3798050E1532C7147CB2BD903655ACD633F0CB50A9CF8C4302D69715E528D1203F12629ED88E31B19CBEA083622141493400D; SECKEY_ABVK=zf7NEna10e197KJeppxIKI1xIjKKADi8Ucph9Ag+Hdw=; BMAP_SECKEY=4hzvVtzd5cyubrF2x4jdZnslOTVfogmTkyBNLauRSwPo5OON3Y3_Wntfj-Ai3zDRp2O7L6_NVUDCxKaOcW4j0nRz5HOvFwp-Ku3rbQ-2cIy1emmOP4cz_Mvn5TWbxGaylLP2MvGuOkCFLeD2J0lBE5lB8mBkcBPPJIV1EyNHlV9z1ZS1IApvDsyj3yZCME6c',
            # 'Host': 'fanyi.youdao.com',
            # 'Origin': 'http://fanyi.youdao.com',
            'Referer': 'https://select.pdgzf.com/houseLists',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:51.0) Gecko/20100101 Firefox/51.0',
            # 'X-Requested-With': 'XMLHttpRequest'
        }
        data = {"where":
                    {"keywords": "",
                     "township": "null",
                     'projectId': "null",
                     "typeName": "null",
                     "rent": "null"},
                "pageIndex": 0, "pageSize": 10}
        html = requests.post(self.url, data=data, headers=headers).text
        print(html)
        infos = json.loads(html)
        if 'translateResult' in infos:
            try:
                result = infos['translateResult'][0][0]['tgt']
                print(result)
            except:
                pass


if __name__ == '__main__':
    y = Youdao('你是我的小苹果，我是你的优乐美')
    y.get_result()
