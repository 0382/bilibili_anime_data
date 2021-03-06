#-*- encoding=utf-8 -*-
# author: 0.382
# environment: win64 python3.7
# ---------------------------
import json
import os
import codecs

anime_file_list = os.listdir('anime')
anime_list = []

for file in anime_file_list:
    fp = codecs.open('.\\anime\\'+file, 'r', 'utf-8')
    anime = json.load(fp)
    if anime['mediaRating'] != {}:
        score_anime = {}
        score_anime['title'] = anime['title']
        score_anime['score'] = anime['mediaRating']['score']
        score_anime['count'] = anime['mediaRating']['count']
        anime_list.append(score_anime)
    else:
        continue

anime_list.sort(key = lambda x:(float(x['score']),int(x['count'])), reverse = True)

fp = codecs.open('score.txt', 'w', 'utf-8')

for num,my_anime in enumerate(anime_list):
    fp.write('{0}.{1}\n总评分：{2}\n评分人数：{3}\n'.format(num+1, my_anime['title'], my_anime['score'], my_anime['count']))

fp.close()