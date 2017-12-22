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

import wechatsogou

# 可配置参数
# 直连
ws_api = wechatsogou.WechatSogouAPI()
# 验证码输入错误的重试次数，默认为1
ws_api = wechatsogou.WechatSogouAPI(captcha_break_time=3)
# 所有requests库的参数都能在这用
# 如 配置代理，代理列表中至少需包含1个 HTTPS 协议的代理, 并确保代理可用
ws_api = wechatsogou.WechatSogouAPI(proxies={
    "http": "127.0.0.1:8888",
    "https": "127.0.0.1:8888",
})
# 如 设置超时
ws_api = wechatsogou.WechatSogouAPI(timeout=0.1)

def get_gzh_article_info(keyword):
    '''【搜索】公众号信息及公众号文章信息
    input:keywords
    output:
{
    'gzh': {
        'wechat_name': '',  # 名称
        'wechat_id': '',  # 微信id
        'introduction': '',  # 简介
        'authentication': '',  # 认证
        'headimage': ''  # 头像
            },
    'article': [
        {
            'send_id': int,  # 群发id，注意不唯一，因为同一次群发多个消息，而群发id一致
            'datetime': int,  # 群发datatime 10位时间戳
            'type': '',  # 消息类型，均是49（在手机端历史消息页有其他类型，网页端最近10条消息页只有49），表示图文
            'main': int,  # 是否是一次群发的第一次消息 1 or 0
            'title': '',  # 文章标题
            'abstract': '',  # 摘要
            'fileid': int,  #
            'content_url': '',  # 文章链接
            'source_url': '',  # 阅读原文的链接 #null
            'cover': '',  # 封面图
            'author': '',  # 作者
            'copyright_stat': int,  # 文章类型，例如：原创啊
        },
        ...
    ]
}
    '''
    ws_api =wechatsogou.WechatSogouAPI()
    #搜索公众号
    #print(ws_api.search_gzh(keyword))
    #获取特定一个公众号信息
    #print(ws_api.get_gzh_info('腾讯'))
    #【搜索】微信文章
    #print(ws_api.search_article('腾讯'))
    gzh_article_by_history=ws_api.get_gzh_article_by_history(keyword)
    item_list = []
    for each in gzh_article_by_history['article']:
        item={}
        #gzh info
        item['name'] = keyword
        item['gzh_wechat_name'] = gzh_article_by_history['gzh']['wechat_name']
        item['gzh_wechat_id'] = gzh_article_by_history['gzh']['wechat_id']
        item['gzh_introduction'] = gzh_article_by_history['gzh']['introduction']
        item['gzh_authentication'] = gzh_article_by_history['gzh']['authentication']
        item['gzh_headimage'] = gzh_article_by_history['gzh']['headimage']
        #ten_article info
        item['article_send_id'] = each['send_id']
        item['article_datetime'] = each['datetime']
        item['article_type'] = each['type']
        item['article_main'] = each['main']
        item['article_title'] = each['title']
        item['article_abstract'] = each['abstract']
        item['article_fileid'] = each['fileid']
        item['article_content_url'] = each['content_url']
        content = requests.get(each['content_url']).content
        content = content.decode('utf-8')  # python3
        selector = lxml.html.fromstring(content)
        if selector is not None and len(selector) != 0:
            data_pre0 = selector.xpath('//*[ @ id = "js_content"]')
            if data_pre0 is not None and len(data_pre0) != 0:
                data_pre = data_pre0[0]
                item['article_content'] = data_pre.xpath('string(.)').replace('\n', '').replace(' ', '')
            else:
                item['article_content'] = [' ']
        else:
            item['article_content'] = [' ']
        item['article_source_url'] = each['source_url']
        item['article_cover'] = each['cover']
        item['author'] = each['author']
        item['copyright_stat'] = each['copyright_stat']
        item_list.append(item)
    return item_list


def writeData(item_list):
    with open('wechat_gzh.csv', 'w', encoding='UTF-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['name','gzh_wechat_name','gzh_wechat_id','gzh_introduction','gzh_authentication','gzh_headimage',
                                               'article_send_id','article_datetime','article_type','article_main','article_title',
                                               'article_abstract','article_fileid','article_content_url',
                                               'article_content','article_source_url',
                                               'article_cover','author','copyright_stat'])
        writer.writeheader()
        for each in item_list:
            print(each)
            writer.writerow(each)

if __name__ == '__main__':
    item_list = []
    # 获取指定目录下的xlsx，并打开操作
    for file in glob.glob(r"C:/Users/anhan/programmingfiles/wechat/*.xlsx"):
        df_pre = pd.read_excel(file)
        df = df_pre[df_pre['行业3']=='饮料']
        industry3 = df["行业3"]
        keywordList = df["名称"]
        for each in keywordList:
            print(each)
            item_list += get_gzh_article_info(each)
    writeData(item_list)



