#!/usr/bin/env python3
# coding: utf-8
# auther: 0.382
# data:   2018-06-24
# description: 抓取b站番剧数据
# enviroment:  Ubuntu16.04LTS 32bit python3.5
# ------------------------------------------

import urllib
from urllib import request,parse
import json
import codecs
import re

Headers = {'User-Agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/66.0.3359.181 Chrome/66.0.3359.181 Safari/537.36'}
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

def load_page(url, urldata):
    this_url = url + '?' + parse.urlencode(urldata)
    req = request.Request(this_url, headers = Headers)
    response = request.urlopen(req)
    return response.read().decode('utf-8')

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

def save_anime(anime):
    anime_dic = get_anime(anime)
    if anime_dic != {}:
        fp = codecs.open('./anime/{0}.json'.format(anime_dic['anime']),'w','utf-8')
        json.dump(anime_dic,fp,ensure_ascii=False)
        fp.close()
if __name__ == '__main__':
    for pagenumber in range(1,3):
        print(pagenumber)
        urldata['page'] = str(pagenumber)
        html = load_page(anime_sort_URL, urldata)
        data = json.loads(html)
        anime_list = data['result']['data']
        for anime in anime_list:
            #print(anime['title'])
            save_anime(anime)