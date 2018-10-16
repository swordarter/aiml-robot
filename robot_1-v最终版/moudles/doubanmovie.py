#本模块提供电影数据，包括一周新片榜和上榜电影的短评，相关接口是get_movies()和get_info('待查询电影序号','影评数量')
#get_movies() 返回一个字符串，包含一周新片榜的电影相关信息（电影序号，电影名称，评分，评价人数）
#get_info('待查询电影序号','影评数量')返回一个字符串，包含查询的电影的详细基本信息（主演，上映时间、类型、国家等）以及指定数量(方法内部已控制最大50条，输入大于50只显示50条)的相关短评；传入的参数：待查询电影序号，为get_movies()输出结果中电影序号减1，
#   传入之前需保证为数字类型且数值范围在1~10；传入的第二个参数为用户希望看到的影评条数，传入之前需保证为>0的整数

import requests
from lxml import etree

class MovieSpider:
    def __init__(self):
        self.start_url="https://movie.douban.com/chart"
        self.headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}
        self.movies_url=[]
        self.comment_url="{}comments?start={}&limit=20&sort=new_score&status=P"

    def parse_url(self,url):
        response=requests.get(url,headers=self.headers)
        return response.content.decode()

    def get_movies_list(self,html_str):
        html=etree.HTML(html_str)
        content_list=html.xpath(".//div[@id='content']//table")
        movie_list=[]
        for div in content_list:
            movie={}
            self.movies_url.append(div.xpath(".//div[@class='pl2']/a/@href")[0])
            movie["title"]=div.xpath(".//div[@class='pl2']/a/text()")[0].strip().split("\n")[0]
            movie["rating"]=div.xpath(".//div[@class='star clearfix']/span[@class='rating_nums']/text()")[0]
            movie["hot"]=div.xpath(".//div[@class='star clearfix']/span[@class='pl']/text()")[0]
            movie_list.append(movie)
        return movie_list
    def get_movies(self):
        html_str=self.parse_url(self.start_url)
        movie_info=self.get_movies_list(html_str)
        index=1
        s=''
        for info in movie_info:
            s=s+str(index)+".\t"+"名称:"+info["title"]+'\t'+'评分:'+info["rating"]+info["hot"]+'\n'
            index+=1
        return s

    def get_base_info(self,index):
        url = self.comment_url.format(self.movies_url[index],'0')
        html_str = self.parse_url(url)
        html = etree.HTML(html_str)
        base_info = html.xpath(".//div[@class='movie-summary']//p//text()")
        info_picture=html.xpath(".//div[@class='movie-summary']//img/@src")[0]
        info_str=""
        for info in base_info:
            info_str+=info
        return info_str,info_picture

    def get_content(self,html_str):
        html=etree.HTML(html_str)
        item_div=html.xpath(".//div[@id='comments']//div[@class='comment-item']")
        item_list=[]
        for div in item_div:
            item={}
            item['vote']=div.xpath(".//span[@class='votes']/text()")[0]
            item['comment']=div.xpath(".//span[@class='short']/text()")[0]
            item_list.append(item)
        return item_list

    def get_comments(self,index,counts):
        number=counts if counts<=50 else 50
        comments_list=[]
        comment_str = ''
        comment_number = 0
        while comment_number<number:
            url = self.comment_url.format(self.movies_url[index],str(comment_number))
            html_str=self.parse_url(url)
            comments_list+=self.get_content(html_str)
            comment_number+=20
        for comment in comments_list[0:number]:
                comment_str+=comment['vote']+'人认为：'+comment['comment']+'\n'
        return comment_str

    def get_info(self,index,number):
        info='电影基本信息：\n'
        s,p=self.get_base_info(index)
        info+=s
        info+='\n相关影评：\n'
        comments=self.get_comments(index,number)
        info+=comments
        return info

# movie_spider=MovieSpider()
# print(movie_spider.get_movies())
# print(movie_spider.get_info(1,5))





