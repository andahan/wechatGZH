#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' wehcatGZH_info v1.0 '

__author__ = 'Xiao Zhuangzhuang'

import requests
import lxml.html
import urllib.parse
import re
import csv
import glob
import pandas as pd
from captcha_solver import CaptchaSolver
import time,random

import wechatsogou

def get_gzh_info(keyword,page):
    ws_api =wechatsogou.WechatSogouAPI()
    #搜索公众号
    search_gzh=ws_api.search_gzh(keyword,page)
    return search_gzh


def writeData(item_list):
    with open('wechat_gzh_search_id.csv', 'a', encoding='UTF-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['headimage', 'wechat_id', 'profile_url', 'post_perm', 'wechat_name', 'open_id', 'qrcode', 'introduction', 'authentication'])
        writer.writeheader()
        for each in item_list:
            print(each)
            writer.writerow(each)

if __name__ == '__main__':
    item_list = []
    for each in ["白酒"]:
        print(each)
        page = 19  #需要输入
        for page in range(1, page + 1):
            print("Page %i ..." % page)
            item_list += get_gzh_info(each,page)
            time.sleep(random.randint(5, 15) / 10.0)
    writeData(item_list)




