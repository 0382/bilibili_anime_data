#------------------------------
#-*- encoding=utf-8 -*-
# author:       0.382
# date:         2018-5-5
# description:  抓取b站番剧的数据
# enviroment:   win10_32bit python3.5
#------------------------------

from urllib import request
import codecs
import json
import re

Headers = {'User-Agent':'Mozilla/5.0'}

#番剧索引的URL，参数直接写齐好了，相关参数解释请看URL.txt
index_URL = 'https://bangumi.bilibili.com/web_api/season/index_global?page={0}&page_size=20&version=1&is_finish=0&start_year=0&tag_id=135&index_type=1&index_sort=0&quarter=0&area=2'

#国创的URL，国创是专门分开的
index_cn_URL = 'https://bangumi.bilibili.com/web_api/season/index_cn?page={0}&page_size=20&version=1&is_finish=0&start_year=0&tag_id=&index_type=1&index_sort=0'

#番剧专题，指向唯一一个番剧，要填入的参数就是番号，但是程序没有用到，这个URL现在request还有回应，但是在浏览器会自动跳转到另外一个URL，那个我也没有研究
anime_URL = 'https://bangumi.bilibili.com/anime/{0}'

#这个url是某次无意间发现的，目前还没有研究相关参数，这个URL是代替上一个URL使用的
anime_json_URL = 'https://bangumi.bilibili.com/jsonp/seasoninfo/{0}.ver?callback=seasonListCallback&jsonp=jsonp'

#番剧播放URL，指向番剧某一集的播放页，只有在播放页面才有我需要的数据
play_URL = 'https://www.bilibili.com/bangumi/play/ep{0}'

#下载某URL页面
def load_page(url):
    req = request.Request(url, headers = Headers)
    response = request.urlopen(req)
    return response.read().decode('utf-8')

#分析index_URL页面，每页有20个番剧番号和番名信息
def get_anime(index_page):
    anime_id_list = re.findall(r'"season_id":"([0-9]+)"', index_page)
    anime_title_list = re.findall(r'"title":"([\s\S]*?)",', index_page)
    anime_list = zip(anime_id_list, anime_title_list)
    return anime_list

#保存一个番剧的信息
def save_anime(anime_play):
    play_page = load_page(play_URL.format(anime_play[2]))
    #anime_data这一点需要特别注意，在18年5月3号上面一行是有用的，但是5月4号就没有用了，网页页面变成了下面的结构，新的两个参数似乎还没有开始起作用
    #anime_data = re.search(r'"stat":{"coins":([0-9]+),"danmakus":([0-9]+),"favorites":([0-9]+),"views":([0-9]+)}', play_page)
    anime_data = re.search(r'"stat":{"coins":([0-9]+),"danmakus":([0-9]+),"favorites":([0-9]+),"reply":([0-9]+),"share":([0-9]+),"views":([0-9]+)}', play_page)
    anime_score = re.search(r'"mediaRating":{"count":([0-9]+),"score":([0-9]+\.?[0-9]?)}', play_page)
    anime_dic = {}
    anime_dic['anime'] = anime_play[0]
    anime_dic['title'] = anime_play[1]
    #anime_dic['ep_play'] = anime_play[2]
    anime_dic['coins'] = anime_data.group(1)
    anime_dic['danmakus'] = anime_data.group(2)
    anime_dic['favorites'] = anime_data.group(3)
    anime_dic['reply'] = anime_data.group(4)
    anime_dic['share'] = anime_data.group(5)
    anime_dic['views'] = anime_data.group(6)
    #并不是所有番剧都有评分
    if anime_score == None:
        anime_dic['count'] = ''
        anime_dic['score'] = ''
    else:
        anime_dic['count'] = anime_score.group(1)
        anime_dic['score'] = anime_score.group(2)
    fp = codecs.open('anime\\anime{0}.json'.format(anime_play[0]), 'w', 'utf-8')
    json.dump(anime_dic, fp, ensure_ascii = False)
    fp.close()

#遍历一页index_URL的所有番，找到信息并保存
def search_list(anime_list):
    for anime in anime_list:
        anime_page = load_page(anime_json_URL.format(anime[0]))
        anime_play_id = re.search(r'episode_id":"([0-9]+)"'.format(anime[0]), anime_page)
        if anime_play_id == None:
            continue
        else:
            anime_play_id = anime_play_id.group(1)
        anime_play = anime + (anime_play_id,)
        print(anime_play[0])
        save_anime(anime_play)

if __name__ == '__main__':
    #自己看看自己设定的参数有几页。超出的页面没有关系，但是会花程序运行时间
    for i in range(1,20):
        index_page = load_page(index_URL.format(i))
        anime_list = get_anime(index_page)
        search_list(anime_list)