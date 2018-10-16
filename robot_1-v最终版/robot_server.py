from PyQt5 import QtCore,QtGui,QtWidgets
from socket import *
from threading import Thread
import aiml
import time
import sys
from settings import robotStart
from settings.viewUI import robot_UI
from moudles.tianqi import WeatherSpider





class robotServer(robot_UI):
    def __init__(self):
        self.port = 9200
        self.host = '176.136.12.80'
        self.sockfd = socket()
        self.sockfd.setblocking(False)
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.address = (self.host,self.port)
        self.client_socket_list = list()
        self.dabai = robotStart.myBot()
        self.dabai.robotborn()
    

    def serve_forever(self):
        self.sockfd.bind(self.address)
        self.sockfd.listen(50)
        print('启动成功')
        self.server_th = Thread(target=self.server_concurrency)
        self.server_th.setDaemon(True)
        self.server_th.start()

    def server_concurrency(self):
        while True:
            try:
                connfd,addr = self.sockfd.accept()
            except Exception as e:
                pass
            else:
                connfd.setblocking(False)
                print('连接成功')
                self.client_socket_list.append((connfd,addr))
            for client, Caddress in self.client_socket_list:
                try:
                    msg_recv = client.recv(4096)
                    print(self.client_socket_list)
                    print('服务器接收')
                except Exception as res:
                    pass
                else:
                    key_select = '关键字:'
                    key_select_1 = '今天'
                    key_select_2 = '明天'
                    key_select_3 = '后天'
                    key_select_4 = '查询车票 '
                    key_select_5 = '新闻话题 '
                    if msg_recv.decode().split('%')[0] == 'bye':
                        self.send_server('end')
                    elif key_select in msg_recv.decode().split('%')[0]:
                        moudle = __import__("talks.file_write")
                        print(moudle)
                        print(moudle.file_write)
                        print(moudle.file_write.baidubaike)
                        query_word = msg_recv.decode().split('%')[0].split(':')[1]
                        meaning = moudle.file_write.baidubaike(query_word)
                        moudle.file_write.baidubaike_modify(meaning)
                        self.dabai.mybot.learn('settings/std-startup.xml')
                        self.dabai.mybot.respond('LOAD AI')
                        self.send_server(msg_recv.decode())
                    elif key_select_1 in msg_recv.decode().split('%')[0]:
                        days = 1
                        weather_spider = WeatherSpider()
                        weather_res = weather_spider.get_complete_info(days)
                        moudle = __import__("talks.file_write")
                        moudle.weather_modify(weather_res)
                        self.dabai.mybot.learn('settings/std-startup.xml')
                        self.dabai.mybot.respond('LOAD AI')
                        self.send_server(msg_recv.decode())
                    elif key_select_2 in msg_recv.decode().split('%')[0]:
                        days = 2
                        weather_spider = WeatherSpider()
                        weather_res = weather_spider.get_complete_info(days)
                        moudle = __import__("talks.file_write")
                        moudle.weather_modify(weather_res)
                        self.dabai.mybot.learn('settings/std-startup.xml')
                        self.dabai.mybot.respond('LOAD AI')
                        self.send_server(msg_recv.decode())
                    elif key_select_3 in msg_recv.decode().split('%')[0]:
                        days = 3
                        weather_spider = WeatherSpider()
                        weather_res = weather_spider.get_complete_info(days)
                        moudle = __import__("talks.file_write")
                        moudle.weather_modify(weather_res)
                        self.dabai.mybot.learn('settings/std-startup.xml')
                        self.dabai.mybot.respond('LOAD AI')
                        self.send_server(msg_recv.decode())
                    # elif key_select_4 in msg_recv.decode().split('%')[0]:
                    #     msg_ticket_list = msg_recv.decode().split('%')[0].split(' ')
                    #     print(msg_ticket_list)
                    #     train_s = msg_ticket_list[1]
                    #     train_e = msg_ticket_list[2]
                    #     train_t = msg_ticket_list[3]
                    #     try:
                    #         from train_tickey_spider import TrainTicketSpider
                    #         train_ticket = TrainTicketSpider()
                    #         response_ticket = train_ticket.get_train_info(train_s,train_e,train_t)
                    #         moudle = __import__("file_write")
                    #         moudle.ticket_info_modify(response_ticket)
                    #         self.dabai.mybot.learn('std-startup.xml')
                    #         self.dabai.mybot.respond('LOAD AI')
                    #         self.send_server(msg_recv.decode())
                    #     except Exception:
                    #         msg_recv = '查无此车'+'%'+msg_recv.decode().split('%')[1]
                    #         self.send_server(msg_recv)                        
                    # elif key_select_5 in msg_recv.decode().split('%')[0]:
                    #     msg_price_list = msg_recv.decode().split('%')[0].split(' ')
                    #     msg_ticket_price = msg_price_list[1]
                    #     try:
                    #         from train_tickey_spider import TrainTicketSpider
                    #         train_ticket = TrainTicketSpider()
                    #         response_ticket_price = train_ticket.get_price(msg_ticket_price)
                    #         moudle = __import__("file_write")
                    #         moudle.ticket_price_modify(response_ticket_price)
                    #         self.dabai.mybot.learn('std-startup.xml')
                    #         self.dabai.mybot.respond('LOAD AI')
                    #         self.send_server(msg_recv.decode())
                    #     except Exception:
                    #         msg_recv = '车次不存在'+'%'+msg_recv.decode().split('%')[1]
                    #         self.send_server(msg_recv)                       
                    else:
                        key_words_zh = '请将中文'
                        key_words_en = '请将英文'
                        if key_words_zh or key_words_en in msg_recv.decode().split('%')[0]:
                            moudle = __import__("talks.file_write")
                            query_word = ''
                            for word in msg_recv.decode().split('%')[0]:
                                if word in ['请','将','中','文','翻','译','成','英','文']:
                                    continue
                                query_word += word
                            print(query_word)
                            if key_words_zh in msg_recv.decode().split('%')[0]:
                                meaning = moudle.file_write.query_word(query_word,"zh","en")
                                moudle.file_write.file_modify_en(meaning)
                            elif key_words_en in msg_recv.decode().split('%')[0]:
                                meaning = moudle.file_write.query_word(query_word,"en","zh")
                                moudle.file_write.file_modify_zh(meaning)
                            self.dabai.mybot.learn('settings/std-startup.xml')
                            self.dabai.mybot.respond('LOAD AI')

                        self.send_server(msg_recv.decode())    
            
    def send_server(self,msg):
        print('大白正在思考')
        msg_list = msg.strip().split('%')
        question = msg_list[0]
        print(question)
        #可能存在对话中出现百分号
        if len(msg_list) > 1:
            ADDR = tuple(eval(msg_list[1]))
            print(ADDR)
        else:
            ADDR=tuple()
        print(ADDR)
        for client,caddress in self.client_socket_list:
            if caddress == ADDR:
                question_make = list()
                for word in question:
                    question_make.append(word)
                question = ' '.join(question_make)
                response = self.dabai.robothandler(question)
                msg = '{}\n'.format(response).encode()
                client.send(msg)
                print('服务端已发送')
            if not ADDR:
                client.send(b'bye')         
                client.close()
                print('服务端已关闭')
                self.client_socket_list.remove((client,caddress))     

    
                


            




