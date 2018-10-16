# -*- coding: utf-8 -*-
#��ģ���ṩ������Ϣ��ֻ��get_brif_info()��get_complete_info()�����ӿڿɹ��ⲿ����
#get_brif_info()����Ҫ�������������7��ļ�������Ϣ
#get_complete_info()��Ҫ����һ��1~7���������Ͳ������ò���ָ����Ҫ������һ���������Ϣ������ָ��ĳһ��ľ���������Ϣ
#���ͣ�����������Ҫʵʱ���ݣ���ˣ�ÿ�ε��ýӿڻ��Զ���������ȡ��Ϣ����self.weather_info��

import requests
from lxml import etree

class WeatherSpider:
 def __init__(self):
    self.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"}
    self.url = "http://www.nmc.cn/publish/forecast/AHB/huangshi.html"
    self.weather_info = []

 def parse_url(self):
    response = requests.get(self.url, headers=self.headers)
    return response.content.decode()

 def set_weather_info_list(self):
    html_str = self.parse_url()
    html = etree.HTML(html_str)
    div_list = html.xpath(".//div[@class='forecast']/div[@class='detail']/div[@class='day']")
    for div in div_list:
        dic = {}
        dic['date'] = "".join(div.xpath(".//div[@class='date']/text()")[0].strip().split(" "))
        dic['week'] = div.xpath(".//div[@class='week']/text()")[0].strip()
        dic['wdesc'] = div.xpath(".//div[@class='wdesc']/text()")[0].strip()
        dic['temp'] = div.xpath(".//div[@class='temp']/text()")[0].strip()
        dic['direct'] = div.xpath(".//div[@class='direct']/text()")[0].strip()
        dic['wind'] = div.xpath(".//div[@class='wind']/text()")[0].strip()
        self.weather_info.append(dic)

 def get_brif_info(self):
     self.set_weather_info_list()
     s=''
     index=1
     for item in self.weather_info:
        s=s+str(index)+"."+item['date']+':'+item['wdesc']+'\n'
        index=index+1
     return s

 def get_complete_info(self,index):
     self.set_weather_info_list()
     s=''
     dic=self.weather_info[index-1]
     s= dic['wdesc']+' '+dic['temp']+' '+dic['direct']+' '+dic['wind']
     return s

# ���ԣ�
# weather_spider=WeatherSpider()
# print(weather_spider.get_brif_info())
# print(weather_spider.get_complete_info(2))