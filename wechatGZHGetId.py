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

def get_gzh_article_info(keyword):
    ws_api =wechatsogou.WechatSogouAPI()
    #搜索公众号
    #print(ws_api.search_gzh(keyword))
    #获取特定一个公众号信息
    #print(ws_api.get_gzh_info('腾讯'))
    #【搜索】微信文章
    #print(ws_api.search_article('腾讯'))
    get_gzh_info=ws_api.get_gzh_info(keyword)
    item_list = []
    item={}
    #gzh info
    item['name'] = keyword
    item['gzh_wechat_name'] = get_gzh_info['wechat_name']
    item['gzh_wechat_id'] = get_gzh_info['wechat_id']
    item_list.append(item)
    return item_list


def writeData(item_list):
    with open('wechat_gzh_id.csv', 'a', encoding='UTF-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['name','gzh_wechat_name','gzh_wechat_id'])
        writer.writeheader()
        for each in item_list:
            print(each)
            writer.writerow(each)

if __name__ == '__main__':
    item_list = []
    for each in ['安图生物','璞泰来','苏州科达','恒林股份','三祥新材','康隆达','五洲新春','天马科技','灵康药业','卫信康','奇精机械','火炬电子','华体科技','晶华新材','晨丰科技','龙马环卫','石英股份','皖天然气','至纯科技','安记食品','航天工程','纽威股份','德宏股份','盛洋科技','健友股份','家家悦','香飘飘','塞力斯','天域生态','海利生物','中广天择','阿科力','天安新材','朗迪集团','博迈科','鸣志电器','龙韵股份','岱美股份','三棵树','泰晶科技','大元泵业','秦安股份','隆鑫通用','中马传动','常青股份','永安行','来伊份','乾景园林','威龙股份','新日股份','宁波高发','星光农机','联泰环保','康普顿','华友钴业','道森股份','志邦股份','瑞斯康达','福斯特','歌力思','豪能股份','诚意药业','原尚股份','顾家家居','海峡环保','曲美家居','神力股份','嘉澳环保','百合花','华扬联众','坤彩科技','柯利达','洛凯股份','欧派家居','四通股份','安正时尚','正平股份','好太太','华荣股份','东宏股份','步长制药','能科股份','中公高科','白云电器','桃李面包','飞科电器','北部湾旅','太平鸟','武进不锈','永悦科技','南卫股份','数据港','金域医学','老百姓','吉祥航空','元祖股份','城地股份','新华网','新澳股份','春秋电子','寿仙谷','好莱客','晨光文具','莱绅通灵','永创智能','中持股份','龙蟠科技','牧高笛','合诚股份','佳力图','苏博特','合力科技','金桥信息','金徽酒','世运电路','金鸿顺','铁流股份','兴业股份','亚翔集成','睿能科技','博敏电子','丽岛新材','三孚股份','益丰药房','大千生态','哈森股份','百利科技','克来机电','大理药业','法兰泰克','醋化股份','银龙股份','中农立华','正川股份','国泰集团','深圳新星','金诚信','吉华集团','恒润股份','兆易创新','康德莱','中电电机','艾华集团','麦迪科技','至正股份','洛阳钼业','中新科技','继峰股份','方盛制药','读者传媒']:
        print(each)
        item_list += get_gzh_article_info(each)
        time.sleep(random.randint(5, 15) / 10.0)
    writeData(item_list)




