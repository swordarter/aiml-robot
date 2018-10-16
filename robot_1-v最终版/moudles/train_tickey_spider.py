# coding utf-8
#该模块提供火车票信息查询服务，有两个接口可供外界调用，分别为方法get_train_info('出发地','到达地','出发日期'，'座位类型','几点之后','几点之前')和get_price('车次')
#方法get_train_info('出发地','到达地','出发日期'，'座位类型','几点之后','几点之前')，返回一个字符串。如果查询到符合条件的车次，返回最接近设置的出发时间的车次；
# 　　　　　如在查询时段没有该类型的座位，但在其它时段有该类型的票，则提示无票且返回存在查询的座位类型车票的其它时间；如果当日该类型的座位票已全部售完，则返回
#           返回提示无票及有票的座位类型和发车时间
#           该字符串包含所有满足条件的列车基本信息和有票的座位类型余票，传入的参数前两个可以写任意城市名，最后一个要求必须为yyyy-mm-dd格式
#方法get_price('车次')，返回一个字符串，如果传入车次号不存在则返回'车次不存在，请重新输入'，否则，返回该车次的各种座位类型和票价的字符串。
#			传入的参数'车次'，如果要查询的车次第一个是字母要保证是大写字母，否则不能正确匹配到。
import requests
import json

class TrainTicketSpider:
    def __init__(self):
        self.train_url="https://kyfw.12306.cn/otn/leftTicket/queryO?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT"
        self.price_url="https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice?train_no={}&from_station_no={}&to_station_no={}&seat_types={}&train_date={}"
        self.headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}
        self.station_list=self.set_station_list()
        self.trains_list=[]

    def parse_url(self,url):
        responses=requests.get(url,headers=self.headers)
        return responses.content.decode()

    def set_station_list(self):
        url="https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9069"
        html_str=self.parse_url(url)
        html_str=html_str.split("=")[1].split('|')
        list=[]
        index=0
        for str in html_str:
            iterm={}
            if str.isupper():
                iterm['sign']=str
                iterm['station']=html_str[index-1]
                list.append(iterm)
            index=index+1
        return list

    def get_station_sign(self,station):
        for item in self.station_list:
            if  item['station']==station:
                return  item['sign']

    def get_station_name(self,station_sign):
        for item in self.station_list:
            if item['sign'] == station_sign:
                return item['station']

    def set_train_info(self,f_station,t_station,date):
        from_station=self.get_station_sign(f_station)
        to_station=self.get_station_sign(t_station)
        url=self.train_url.format(date,from_station,to_station)
        html_str = self.parse_url(url)
        dic = json.loads(html_str)['data']
        trains_data= dic['result']
        for train in trains_data:
            info={}
            s=train.split('|')
            if s[0]!='':
                info['date']=date
                info['train_no'] = s[2]
                info['车次']=s[3]
                info['始发站']=self.get_station_name(s[4])
                info['终点站']=self.get_station_name(s[5])
                info['出发时刻']=s[8]
                info['到达时刻']=s[9]
                info['历时']=s[10]
                info['from_station_no'] = s[16]
                info['to_station_no'] = s[17]
                info['高级软卧']=s[21]
                info['软卧']=s[23]
                info['软座']=s[24]
                info['无座']=s[26]
                info['硬卧']=s[28]
                info['硬座']=s[29]
                info['二等座']=s[30]
                info['一等座']=s[31]
                info['商务特等座']=s[32]
                info['动卧']=s[33]
                info['seat_types']=s[35]
                self.trains_list.append(info)

    def time_trans(self,t):
        return int(t.split(':')[0]), int(t.split(':')[1])

    def time_comp(self,t, t_min, t_max):
        t_h, t_m = self.time_trans(t)
        min_h, min_m = self.time_trans(t_min)
        max_h, max_m = self.time_trans(t_max)
        if (min_h < t_h or (min_h == t_h and min_m <= t_m)) and (max_h > t_h or (max_h == t_h and max_m >= t_m)):
            return True
        return False

    def time_info_of_seat_type(self,seat_type):
        time_info=''
        for li in self.trains_list:
            if li[seat_type] not in ['', '无']:
                time_info+=li['出发时刻']+"/"
        return time_info

    def get_train_info(self,f_station,t_station,date,seat_type,time_s="00:00",time_e="24:00"):
        self.set_train_info(f_station,t_station,date)
        if len(self.trains_list)==0:
            return "{}到{}的列车似乎尚未开通".format(f_station,t_station)
        has_seat=False
        trains=[]
        for li in self.trains_list:
            if li[seat_type] not in ['','无']:
                has_seat=True
                if self.time_comp(li['出发时刻'],time_s,time_e):
                    trains.append(li)
        if len(trains)>0:
            str_format = ['车次', '始发站', '终点站', '出发时刻', '到达时刻', '历时', seat_type]
            info='符合条件的车次共{}班,具体信息为：\n'.format(len(trains))
            for li in trains:
                for item in str_format:
                    info+=item+':'+li[item]+' '
                info+='\n'
            return info
        if has_seat:
            s=self.time_info_of_seat_type(seat_type)
            return "该时段内的{}票已售完，{}时段还有{}票，可以考虑购买".format(seat_type,s,seat_type)
        else:
            seat_list=['硬座','软座','硬卧','无座','商务特等座','一等座','二等座','软卧','高级软卧','动卧']
            info=""
            for item in seat_list:
                s=self.time_info_of_seat_type(item)
                if s!='':
                    info+=item+'('+s+')'
            if info!='':
                return "当日该座位类型的火车票已售完，其它座位类型的火车信息为：{}".format(info)
            else:
                return "当日所有车次的所有火车票均已售完"

    def get_price(self,train_name):
        seat_type={'A1':'硬座','A2':'软座','A3':'硬卧','WZ':'无座','A9':'商务特等','M':'一等','O':'二等','A4':'软卧','A6':'高级软卧','F':'动卧'}
        pri=tuple()
        for item in self.trains_list:
            if item['车次']==train_name:
                pri=(item['train_no'],item['from_station_no'],item['to_station_no'],item['seat_types'],item['date'])
                break
        else:
            return '车次不存在，请重新输入'
        url=self.price_url.format(*pri)
        html_str=self.parse_url(url)
        price_date=json.loads(html_str)['data']
        # price_info={}
        s=''
        for key,value in price_date.items():
            if key in seat_type.keys():
                # price_info[seat_type[key]]=value
                s=s+seat_type[key]+":"+value+" "
        if s!='':
            return train_name+'的票价信息为:'+s
        return "无法查询到该列车的票价信息"


# train_ticket=TrainTicketSpider()
# print(train_ticket.get_train_info('北京','成都','2018-10-16','软卧','00:00','15:00',))
# print(train_ticket.get_price('K817'))



