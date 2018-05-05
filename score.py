#-*- encoding=utf-8 -*-

import json
import os
import codecs

#后宫番评分排行
anime_file_list = os.listdir('anime')

anime_list = []

for file in anime_file_list:
    fp = codecs.open('anime\\'+file, 'r', 'utf-8')
    anime = json.load(fp)
    if anime['score'] != '':
        score_anime = {}
        score_anime['title'] = anime['title']
        score_anime['score'] = anime['score']
        score_anime['count'] = anime['count']
        anime_list.append(score_anime)
    else:
        continue

anime_list.sort(key = lambda x:(float(x['score']),int(x['count'])), reverse = True)

fp = codecs.open('score.txt', 'w', 'utf-8')

for num,my_anime in enumerate(anime_list):
    fp.write('{0}.{1}\r\n总评分：{2}\r\n评分人数：{3}\r\n'.format(num+1, my_anime['title'], my_anime['score'], my_anime['count']))

fp.close()