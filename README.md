# bilibili_anime_data
抓取b站番剧信息（按照番剧索引页面的参数）

#### 获取数据

- bilibili.py是获取数据的程序，会在anime文件夹下生成一系列按照番号命名的番剧信息json文件。
- bilibili.py里面有一个参数表：
```python
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
```
- urldata用于控制搜索方式，其中的参数说明请看keywords.json，除了未知的两个参数之外，keywords.json已经给出很详细的说明。
  至于这些参数说明是那里来的，其实就在番剧索引页面的第一页源代码里面。
- 国创区。删除aera和season_month或设为-1，把st和season_type都改成4，就变成了国创区的索引。
- 更多发现。参数全部设为默认，把season_type改成2，似乎变成了电影区的索引，改成3似乎变成了纪录片的索引。
  我对这些区不是很熟，但是这个web api是非常有用的，值得进一步研究。此外st参数依然不知道有什么意义。

### 更多应用

- 开发中
