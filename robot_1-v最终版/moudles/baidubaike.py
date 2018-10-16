import requests
import re

class BaikeSpider:
    def __init__(self):
        self.headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"}
        self.post_url="https://baike.baidu.com/item/"

    def run(self,keyword):
        url=self.post_url+keyword
        response=requests.post(url,headers=self.headers)
        html_str=response.content.decode()
        content=re.findall(r"<meta name=\"description\" content=\"(.*?)\">",html_str,re.S)[0]
        try:
           index=-1
           while True:
              index=index-1
              if content[index]=='。':
                  break
           return content[:index+1]
        except:
           return content

# baike=BaikeSpider()
# print(baike.run('黄蓉'))