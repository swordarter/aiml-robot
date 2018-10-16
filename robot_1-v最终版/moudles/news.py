#该模块提供百度热搜的数据，有两个接口可供外界调用，分别为get_news()和get_news_content(数字)
#get_news()，返回一个字符串，包含百度热搜的前20条信息
#get_news_content(数字)，返回一个字符串，包含对指定序号的热搜的相关10条新闻标题，传入的参数会直接作为下标，
#			所以在调用该函数时需要保证参数：1.是数字类型	2.数值在1~20之间	3.需要将用户输入减1，因为index=0时对应用户输入1时的新闻
#注意：在调用get_news_content(数字)时需要保证已经调用过同一个对象的get_news()方法；一次查询必须调用同一个对象的两个方法。

import requests
from lxml import etree

class NewsSpider:
    def __init__(self):
        self.start_url="http://top.baidu.com/buzz?b=1&fr=tph_right"
        self.headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}
        self.news_title=[]
        self.news_url=[]

    def parse_url(self,url,coding):
        responses=requests.get(url,headers=self.headers)
        return responses.content.decode(coding)

    def set_news_info(self,html_str):
        html=etree.HTML(html_str)
        self.news_title=html.xpath(".//table[@class='list-table']//a[@class='list-title']/text()")[0:20]
        self.news_url=html.xpath(".//table[@class='list-table']//td[@class='tc']/a[text()='新闻']/@href")[0:20]

    def set_news_title(self):
        html_str=self.parse_url(self.start_url,"gb2312")
        self.set_news_info(html_str)

    def get_news(self):
        self.set_news_title()
        result=''
        index=1
        for item in self.news_title:
            result=result+str(index)+'\t'+item+'\n'
            index=index+1
        return result

    def set_news_content(self,html_str):
        html=etree.HTML(html_str)
        div_list=html.xpath(".//div[@id='content_left']//h3")[0:10]
        news_content=[]
        for div in div_list:
            content_list=div.xpath(".//text()")
            str="".join(x.strip() for x in content_list)
            news_content.append(str)
        return news_content

    def get_news_content(self,index):
        url=self.news_url[index]
        html_str=self.parse_url(url,"utf-8")
        content=self.set_news_content(html_str)
        result=''
        for item in content:
            result=result+item+"\n"
        return  result

# news_spider=NewsSpider()
# print(news_spider.get_news())
# print(news_spider.get_news_content(1))