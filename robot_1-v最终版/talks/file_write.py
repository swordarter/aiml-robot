import os
import requests
import json
import re


line_find = "英文是:"
line_find_zh = "中文是:"
line_find_baidu = "查询如下:"
line_find_weather = "查询的天气状况为:"
line_find_ticket = "        具体车次情况如下,如想了解票价可继续输入'车次 (您想了解的车次)'，否则输入'否':"
line_find_price = "        该车次票价如下:"

def file_modify_en(mean):
    global line_find
    content = ''    
    line_change = "        英文是:%s"%(mean)
    f = open('talks/fanyi.aiml','r',encoding='utf-8')
    for line in f:
        if line_find in line:
            line = line.replace(line,line_change)+'\n'
        content += line
    print(content)  
    f.close()
    f = open('talks/fanyi.aiml','w',encoding='utf-8')
    f.write(content)
    f.close()
    line_find = line_change

def file_modify_zh(mean):
    global line_find_zh
    content = ''    
    line_change = "        中文是:%s"%(mean)
    f = open('talks/fanyi.aiml','r',encoding='utf-8')
    for line in f:
        if line_find_zh in line:
            line = line.replace(line,line_change)+'\n'
        content += line
    print(content)  
    f.close()
    f = open('talks/fanyi.aiml','w',encoding='utf-8')
    f.write(content)
    f.close()
    line_find_zh = line_change

def baidubaike_modify(knows):
    global line_find_baidu
    content = ''
    line_change = "        查询如下:%s"%(knows)
    f = open('talks/baidubaike.aiml','r',encoding='utf-8')
    for line in f:
        if line_find_baidu in line:
            line = line.replace(line,line_change)+'\n'
        content += line
    print(content)
    f.close()
    f = open('talks/baidubaike.aiml','w',encoding='utf-8')
    f.write(content)
    f.close()
    line_find_baidu = line_change

def weather_modify(weath):
    global line_find_weather
    content = ''
    line_change = "        查询的天气状况为:%s"%(weath)
    f = open('talks/tianqi.aiml','r',encoding='utf-8')
    for line in f:
        if line_find_weather in line:
            line = line.replace(line,line_change)+'\n'
        content += line
    print(content)
    f.close()
    f = open('talks/tianqi.aiml','w',encoding='utf-8')
    f.write(content)
    f.close()
    line_find_weather = line_change

# def ticket_info_modify(infos):
#     global line_find_ticket
#     content = ''
#     line_change = "        具体车次情况如下,如想了解票价可继续输入'车次 (您想了解的车次)'，否则输入'否':%s"%(infos)
#     f = open('huochepiao.aiml','r',encoding='utf-8')
#     for line in f:
#         if line_find_ticket in line:
#             line = line.replace(line,line_change)+'\n'
#         content += line
#     print(content)
#     f.close()
#     f = open('huochepiao.aiml','w',encoding='utf-8')
#     f.write(content)
#     f.close()
#     line_find_ticket = line_change

# def ticket_price_modify(price):
#     global line_find_price
#     content = ''
#     line_change = "        该车次票价如下:%s"%(price)
#     f = open('huochepiao.aiml','r',encoding='utf-8')
#     for line in f:
#         if line_find_price in line:
#             line = line.replace(line,line_change)+'\n'
#         content += line
#     print(content)
#     f.close()
#     f = open('huochepiao.aiml','w',encoding='utf-8')
#     f.write(content)
#     f.close()
#     line_find_price = line_change    


def query_word(word,w_from,w_to):
    headers={"User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Mobile Safari/537.36"}

    post_data = dict()
    post_data["query"] = word
    post_data["from"] = w_from
    post_data["to"] = w_to
    post_url="https://fanyi.baidu.com/basetrans"

    r=requests.post(post_url,data=post_data,headers=headers)
    dict_ret=json.loads(r.content.decode())
    ret=dict_ret['trans'][0]['dst']
    return ret

def baidubaike(keyword):
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"}
    post_url="https://baike.baidu.com/item/"

    url= post_url + keyword
    response=requests.post(url,headers=headers)
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