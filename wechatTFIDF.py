#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' wehcatTFIDF v1.0 '

__author__ = 'Xiao Zhuangzhuang'

import glob
import numpy as np
from pandas import DataFrame
import pandas as pd
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import csv

def chinese_word_cut(text):
    '''
    jieba中文分词
    '''
    return " ".join(jieba.cut(text))

def vectorizer(text, method):
    '''
    文本向量化
    input:
        v1=(1,1)
        v2=(-1,-1)
    output:
        print(cos(v1,v2))
    '''
    vectorizerCount = CountVectorizer(strip_accents='unicode', max_features=100, stop_words='english', max_df=0.5,
                                      min_df=10)
    Count = vectorizerCount.fit_transform(text)
    vectorizerTfidf = TfidfVectorizer(strip_accents='unicode', max_features=100, stop_words='english', max_df=0.5,
                                      min_df=10)
    Tfidf = vectorizerTfidf.fit_transform(df.article_content_cutted)
    # word=vectorizer.get_feature_names()#获取词袋模型中的所有词语
    # weight = tf.toarray()
    # for i in range(len(weight)):  # 打印每类文本的词频，第一个for遍历所有文本，第二个for便利某一类文本下的词频
    #     print(u"-------这里输出第", i, u"个文本的词语词频------")
    #     for j in range(len(word)):
    #         print(word[j], weight[i][j])
    if method == 'TFIDF':
        return Tfidf.toarray() # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的词频
    if method == 'COUNT':
        return Count.toarray() # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的词tfidf权重

def distance(vector1, vector2):
    '''
    计算欧式距离
    input:
        v1=(1,1)
        v2=(-1,-1)
    output:
        print(distance(v1,v2))
    '''
    d = 0
    for a, b in zip(vector1, vector2):
        d += (a - b) ** 2
    return d ** 0.5


def get_df_tf_info(df,tf):
    '''
    得到df_tf
    input:
        df,tf
    output:
        df_tf_list
    '''
    df_tf_list = []
    for i in range(len(tf)):
        df_tf_dict = {}
        df_tf_dict['article_id'] = df["article_id"]
        df_tf_dict["wechat_id"] = df["gzh_wechat_id"][i]
        df_tf_dict["tf"] = tf[i]
        df_tf_list.append(df_tf_dict)
        df_tf = DataFrame(df_tf_list)  # list类型转化为datafrme类型
    return df_tf

def cos(vector1, vector2):
    '''
    计算余弦相似度
    input:
        v1=(1,1)
        v2=(-1,-1)
    output:
        print(cos(v1,v2))
    '''
    dot_product = 0.0
    normA = 0.0
    normB = 0.0
    for a, b in zip(vector1, vector2):
        dot_product += a * b
        normA += a ** 2
        normB += b ** 2
    if normA == 0.0 or normB == 0.0:
        return 0.0
    else:
        return dot_product / ((normA * normB) ** 0.5)


def red(df_tf):
    '''
    计算内部战略相似度--冗余度
    每一篇公众号文章进行冗余度打分
    '''
    red_list=[]
    count = len(df_tf["tf"])
    for i in range(0, count):
        red=0.0
        c=1
        for j in range(i+1, count):
            if df_tf["wechat_id"][i] == df_tf["wechat_id"][j]:
                cos_res = cos(df_tf["tf"][i],df_tf["tf"][j])
        red = (red + cos_res)/c
        red_list.append(red)
        c = c + 1
    df_tf["red"]=red_list
        #print(df_tf["wechat_id"][i],red)
    return df_tf

def rep(df_tf):
    '''
    计算外部战略相似度--代表度
    每一篇公众号文章进行代表度打分
    '''
    rep_list=[]
    count = len(df_tf["tf"])
    for i in range(0, count):
        rep=0.0
        c=1
        for j in range(i+1, count):
            if df_tf["wechat_id"][i] != df_tf["wechat_id"][j]:
                cos_res = cos(df_tf["tf"][i],df_tf["tf"][j])
        rep = (rep + cos_res)/c
        rep_list.append(rep)
        c = c + 1
    df_tf["rep"]=rep_list
        #print(df_tf["wechat_id"][i],red)
    return df_tf

# def write_data(item_list):
#     with open('wechat_df_tf.csv', 'w', encoding='UTF-8', newline='') as f:
#         writer = csv.DictWriter(f, fieldnames=['article_id','wechat_id','tf'])
#         writer.writeheader()
#         for each in item_list:
#             writer.writerow(each)

if __name__ == '__main__':
    # 获取指定目录下的csv，并打开操作
    for file in glob.glob(r"C:/Users/anhan/programmingfiles/wechat/*.csv"):
        df = pd.read_csv(file, encoding='gb18030')  # 编码是中文GB18030，不是utf-8
    # 分词
    df["article_content_cutted"] = df.article_content.apply(chinese_word_cut)
    # 设置文章id
    df["article_id"] = range(len(df))
    # 行业文本向量化
    tf = vectorizer(df.article_content_cutted,'TFIDF')
    # 将向量化文章与相应的公众号以及相应的文章对应起来
    df_tf = get_df_tf_info(df,tf)
    # 计算Red()和Rep()
    df_tf = rep(red(df_tf))
    # 计算子模块函数H()
    df_tf["submode"]= df_tf["red"]-df_tf["rep"]
    # 按照公众号形成公众号子模块函数值--差异化战略打分
    df_tf_submode = df_tf.groupby('wechat_id').mean()
    # 将df_tf_submode写出到csv
    df_tf_submode.to_csv('df_tf_submode.csv')

        




