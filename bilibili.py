#!/usr/bin/env python3
# encoding: utf-8
# author: 0.382
# date:
# description: 抓取b站番剧数据
# environment:  win64 python3.7
# -----------------------------

from urllib import request,parse
import os
import json
import codecs
import re
from fuzzywuzzy import fuzz

Headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
anime_sort_URL = 'https://bangumi.bilibili.com/media/web_api/search/result'

urldata = {
    'season_version': '-1', #类型
    'area':           '-1', #地区
    'is_finish':      '-1', #是否完结
    'copyright':      '-1', #版权
    'season_status':  '-1', #付费
    'season_month':   '-1', #季度
    'pub_date':       '-1', #时间
    'style_id':       '-1', #风格
    'order':          '3',  #排序依据
    'st':             '1',  #未知
    'sort':           '0',  #正序或倒序
    'page':           '1',  #页码
    'season_type':    '1',  #未知，参见README
    'pagesize':       '20'  #一页大小
}

# 下载一个页面
def load_page(url, urldata):
    if urldata == None:
        this_url = url
    else:
        this_url = url + '?' + parse.urlencode(urldata)
    req = request.Request(this_url, headers = Headers)
    response = request.urlopen(req)
    return response.read().decode('utf-8')

# 这个anime是一个大字典，其形状你可以自己print看看，也可以看看anime.json
def get_anime(anime):
    anime_req = request.Request(anime['link'], headers=Headers)
    try:
        anime_html = request.urlopen(anime_req).read().decode('utf-8')
    except urllib.error.HTTPError:
        return {}
    anime_re = '"stat":{"coins":\d+,"danmakus":\d+,"favorites":\d+,"reply":\d+,"share":\d+,"views":\d+},"style":[\s\S]+?,"mediaRating":{[\s\S]+?}'
    anime_str = re.search(anime_re, anime_html)
    anime_data = json.loads('{"data":{'+anime_str.group()+'}')
    anime_dic = {}
    anime_dic['anime'] = anime['season_id']                          #番号
    anime_dic['title'] = anime['title']                              #标题
    anime_dic['cover'] = anime['cover']                              #封面
    anime_dic['is_finish'] = anime['is_finish']                      #是否完结
    anime_dic['views'] = anime_data['data']['stat']['views']         #播放量
    anime_dic['favorites'] = anime_data['data']['stat']['favorites'] #追番人数
    anime_dic['danmakus'] = anime_data['data']['stat']['danmakus']   #弹幕总量
    anime_dic['coins'] = anime_data['data']['stat']['coins']         #硬币总量
    anime_dic['reply'] = anime_data['data']['stat']['reply']         #可能是评论数，目前还一直是0
    anime_dic['share'] = anime_data['data']['stat']['share']         #可能是分享数，目前还一直是0
    anime_dic['style'] = anime_data['data']['style']                 #风格，即标签
    anime_dic['mediaRating'] = anime_data['mediaRating']             #评分，由于有的番没有评分，我就取这个参数了，后面也会比较方便
    return anime_dic

# 保存番剧数据
def save_anime(anime):
    anime_dic = get_anime(anime)
    if anime_dic != {}:
        fp = codecs.open('.\\anime\\{0}.json'.format(anime_dic['anime']),'w','utf-8')
        json.dump(anime_dic,fp,ensure_ascii=False)
        fp.close()

# 创建一个索引，便于从番名检索番剧数据，我还是觉得用番号作为文件名便于管理，只好出此下策
# sql是不会sql的，这辈子都不会sql的，只能够写写json,csv才能维持的了生活这样子
def make_index():
    anime_file_list = os.listdir('.\\anime')
    index = {}
    for file in anime_file_list:
        fp = codecs.open('.\\anime\\'+file, 'r', 'utf-8')
        anime = json.load(fp)
        index[anime['title']] = anime['anime']
        fp.close()
    index_file = codecs.open('index.json','w','utf-8')
    json.dump(index, index_file, ensure_ascii=False, sort_keys=True, indent=4)

# 想到实际存储的题目是固定格式的，未必都记得住，就用模糊匹配吧
# 下一步是不是该人工智能，自然语言搜索，把好大的鱼和游戏人生联系在一起呢，对我而言太难了
# 模糊匹配实测还是可以把《实教》这样的简称搜索出来的，毕竟有字符相同
def search_anime(Title):
    index = json.load(codecs.open('index.json','r','utf-8'))
    Possible_anime = []
    for key in index.keys():
        if fuzz.ratio(Title,key):
            Possible_anime.append(index[key])
    return Possible_anime

if __name__ == '__main__':
    for pagenumber in range(1,2):
        print(pagenumber)
        urldata['page'] = str(pagenumber)
        html = load_page(anime_sort_URL, urldata)
        data = json.loads(html)
        anime_list = data['result']['data']
        for anime in anime_list:
            print(anime['title'])
            save_anime(anime)
    make_index()
    print(search_anime('实教'))