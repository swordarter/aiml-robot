from PyQt5 import QtCore,QtGui,QtWidgets
from settings.viewUI import robot_UI
from robot_server import robotServer
import aiml
from socket import *
from threading import Thread
import datetime
import time
import winsound

#设置全局变量，绑定服务器端口
Saddress = ('176.136.12.80',9200)
#继承UI界面父类，创建窗口子类
class mainWindow(QtWidgets.QWidget,robot_UI):
    #设置信号槽，用于监测窗口控件的行为事件
    _signal = QtCore.pyqtSignal(str)
    _signal2 = QtCore.pyqtSignal(str)
    QtWidgets.QSystemTrayIcon
       
    def __init__(self,Saddress):
        super(mainWindow,self).__init__()
        self.setupUI(self)
        self.QTextEdit_TIME.setText('时间输入示例:1990-02-21-08-29')
        self.sendButton.clicked.connect(self.client_send)
        self.clearButton.clicked.connect(self.message_clear)
        self.startButton.clicked.connect(self.robot_born)
        self.enterButton.clicked.connect(self.clock)
        self.sendButton.setEnabled(False)
        self.enterButton.setEnabled(False)
        self.startButton.setEnabled(True)
        self.clearButton.setEnabled(True)
        self.QTextBrowser_show.setFont(QtGui.QFont('楷体',14))
        self.QTextBrowser_show.setStyleSheet("color:black")
        self.QTextBrowser_content.setFont(QtGui.QFont('楷体',12))
        self.QTextBrowser_content.setStyleSheet("color:black")
        self._signal.connect(self.messageSingal)
        self._signal2.connect(self.messageSingal2)
        self.Saddress = Saddress
        self.setFixedSize(self.width(), self.height())

    def robot_born(self):
        dabai = robotServer()
        print('start')
        dabai.serve_forever()
        self._signal.emit('大白已经苏醒，快去打招呼吧\n')
        self.client_serve_forever()
        self.sendButton.setEnabled(True)
        self.startButton.setEnabled(False)
    
    
    def client_serve_forever(self):
        self.sockfd = socket()       
        try :
            self.sockfd.connect(self.Saddress)
            print('starting')
        except Exception as e:
            print('客户端无法正常启动')
        self.client_th =Thread(target=self.client_concurrency)
        self.client_th.start()
    
    def client_concurrency(self):
        # weather_dict ={'晴':".images/sun.jpg",'阴':1,'多云':2,'小雨':3}
        while True:
            msg_recv = self.sockfd.recv(4096)
            if msg_recv:
                if msg_recv == b'bye':
                    self.sockfd.close()
                    print('客户端已关闭')
                    self._signal.emit('大白已冬眠，请勿打扰'+'\n')
                    self.sendButton.setEnabled(False)
                    self.startButton.setEnabled(True)
                    break
                else:
                    msg = msg_recv.decode('utf-8')
                    print(msg)
                    if msg == '主人是想了解最近好看的电影吗，大白精心准备了最近十大热门电影，请主人注意右下角的信息栏，想了解更多信息的话，请以(电影序号 "序号")格式输入，大白会给你找寻答案哦！'+'\n':
                        moudle = __import__('moudles.doubanmovie')
                        movie_spider= moudle.doubanmovie.MovieSpider()
                        show_movie = movie_spider.get_movies()
                        self._signal2.emit(show_movie)
                    elif msg == '主人，大白已为你搜罗了最新的热点新闻，请瞧瞧右下角哦，如果想了解详细内容，请输入"新闻话题 新闻序号"'+'\n':
                        moudle = __import__('moudles.news')
                        print(moudle)
                        news_spider = moudle.news.NewsSpider()
                        print(news_spider)
                        print(moudle.news.NewsSpider)
                        print("开始")
                        news_show = news_spider.get_news()
                        print("结束")
                        self._signal2.emit(news_show)
                    # elif len(msg.split(':')) > 1:
                    #     if msg.split(':')[1].split(' ')[0] in weather_dict:
                    #         print('天气图片')
                    #         key = msg.split(':')[1].split(' ')[0]
                    #         self._signal2.emit(weather_dict[key])                             
                    print('客户端已接收')
                    msg = "大白说：" + msg
                    self._signal.emit(msg)
            
    def get_addr(self):
        addr = self.sockfd.getsockname()
        return addr         
    
    def client_send(self):        
        msg = self.QTextEdit_input.toPlainText()
        kegwords = '备忘录'
        kegwords_1 = '百度百科'
        kegwords_2 = '天气'
        kegwords_3 = '电影序号 '
        kegwords_4 = '查询车票 '
        kegwords_5 = '新闻话题 '
        if msg[-1] == '\n':
            self.sendButton.setEnabled(False)
            self.sendButton.setEnabled(True)
        else:
            self.sendButton.setEnabled(True)
            if self.sockfd:
                addr = self.get_addr()
                if msg == 'bye':
                    msg_s = '{}%{}'.format(msg,repr(addr)).encode()
                    self.sockfd.send(msg_s)
                    msg_show = '我说:{}\n'.format(msg)
                    self._signal.emit(msg_show)
                    self.QTextEdit_input.clear()
                elif kegwords in msg:
                    msg_s = '{}%{}'.format(msg,repr(addr)).encode()
                    self.sockfd.send(msg_s)
                    msg_show = '我说:{}\n'.format(msg)
                    self._signal.emit(msg_show)
                    self.QTextEdit_input.clear()
                    self.enterButton.setEnabled(True)
                    # self.clock_th = Thread(target=self.clock)
                    # self.clock_th.setDaemon(True)
                    # self.clock_th.start()
                elif kegwords_1 in msg:
                    msg_s = '{}%{}'.format(msg,repr(addr)).encode()
                    self.sockfd.send(msg_s)
                    msg_show = '我说:{}\n'.format(msg)
                    self._signal.emit(msg_show)
                    self.QTextEdit_input.clear()
                elif kegwords_2 in msg:
                    msg_s = '{}%{}'.format(msg,repr(addr)).encode()
                    self.sockfd.send(msg_s)
                    msg_show = '我说:{}\n'.format(msg)
                    self._signal.emit(msg_show)
                    self.QTextEdit_input.clear()
                elif kegwords_3 in msg:
                    msg_s = '{}%{}'.format(msg,repr(addr)).encode()
                    self.sockfd.send(msg_s)
                    msg_show = '我说:{}\n'.format(msg)
                    self._signal.emit(msg_show)
                    self.QTextEdit_input.clear()
                    query_msg_list = msg.split(' ')
                    id_movie = int(query_msg_list[1])-1
                    moudle = __import__('moudles.doubanmovie')
                    moviespider = moudle.doubanmovie.MovieSpider()
                    moviespider.get_movies()
                    info_movie = moviespider.get_info(id_movie,5)
                    self._signal2.emit(info_movie)
                elif kegwords_4 in msg:
                    msg_s = '{}%{}'.format(msg,repr(addr)).encode()
                    self.sockfd.send(msg_s)
                    msg_show = '我说:{}\n'.format(msg)
                    self._signal.emit(msg_show)
                    self.QTextEdit_input.clear()
                    query_msg_list = msg.split(' ')
                    place_start = query_msg_list[1]
                    place_end = query_msg_list[2]
                    date = query_msg_list[3]
                    sit = query_msg_list[4]
                    time_start = query_msg_list[5]
                    time_end = query_msg_list[6]
                    moudle = __import__('moudles.train_tickey_spider')
                    train_spider = moudle.train_tickey_spider.TrainTicketSpider()
                    train_info = train_spider.get_train_info(place_start,place_end,date,sit,time_start,time_end)
                    self._signal2.emit(train_info)
                elif kegwords_5 in msg:
                    msg_s = '{}%{}'.format(msg,repr(addr)).encode()
                    self.sockfd.send(msg_s)
                    msg_show = '我说:{}\n'.format(msg)
                    self._signal.emit(msg_show)
                    self.QTextEdit_input.clear()
                    query_msg_list = msg.split(' ')
                    news_id = int(query_msg_list[1])-1
                    moudle = __import__('moudles.news')
                    news_spider = moudle.news.NewsSpider()
                    news_spider.get_news()
                    news_info = news_spider.get_news_content(news_id)
                    self._signal2.emit(news_info)
                else:
                    msg_s = '{}%{}'.format(msg,repr(addr)).encode()
                    self.sockfd.send(msg_s)
                    print('客户端发送')
                    msg_show = '我说:{}\n'.format(msg)
                    self._signal.emit(msg_show)
                    self.QTextEdit_input.clear()               
   
    def message_clear(self):
        self.QTextBrowser_show.clear()
        
    def messageSingal(self,msg):
        msg = msg + '\n'
        self.QTextBrowser_show.insertPlainText(msg)
        self.QTextBrowser_show.moveCursor(QtGui.QTextCursor.End)

    def messageSingal2(self,msg):
        msg = msg + '\n'
        self.QTextBrowser_content.clear()
        if '.images/' in msg:
            #  w = QtWidgets.QWidget()
            #  w.setGeometry(5,5,5,5)
            #  l1 = QtWidgets.QLabel(w)
            #  png = QtGui.QPixmap(msg)
            #  l1.setPixmap(png)
            msg = "<img src={}>".format(msg)
            self.QTextBrowser_content.insertHtml(msg)       
        else:
            self.QTextBrowser_content.insertPlainText(msg)
        self.QTextBrowser_content.moveCursor(QtGui.QTextCursor.End)

    def time_enter(self):
        times = self.QTextEdit_TIME.toPlainText().strip()
        self.QTextEdit_TIME.clear()
        return times

    def thread_enter(self):
        threads = self.QTextEdit_THREAD.toPlainText().strip()
        self.QTextEdit_THREAD.clear()
        return threads

    def location_enter(self):
        location = self.QTextEdit_LOCATION.toPlainText().strip()
        self.QTextEdit_LOCATION.clear()
        return location

    def clock(self):
        times = self.time_enter()
        print(times)
        thread = self.thread_enter()
        location = self.location_enter()
        if times and thread and location:
            try:
                time_list = times.split('-')
                print(time_list)
                hours = int(time_list[-2])
                minutes = int(time_list[-1])

                time_now = datetime.datetime.now()
                time_now = datetime.datetime.strftime(time_now,r'%Y-%m-%d-%H-%M')
                time_now_list = time_now.split('-')
                time_now_hours = int(time_now_list[-2])
                time_now_minutes = int(time_now_list[-1])
                
                values = (hours*60+minutes)-(time_now_hours*60+time_now_minutes)
                if values <= 0:
                    msg_show = '大白说:您输入的时间不正确，请重新输入'
                    self._signal.emit(msg_show)
                    return
                elif values < 45:
                    if 0 <= minutes <= values:
                        hours = hours
                        minutes = minutes
                    values = 0
                else:
                    if 0 <= minutes <= 45:
                        hours = hours-1
                        minutes = minutes+15 
                    elif 45 < minutes < 60:
                        minutes = minutes-45
                    values = 45
                time_list[-1] = self.judge_num(minutes)
                time_list[-2] = self.judge_num(hours)
                times = '-'.join(time_list)
                print('计时开始')
                print(times)
                msg_show = "大白说:定时期间请勿关闭我哦！！！"
                self._signal.emit(msg_show)
                self.clock_th = Thread(target=self.clock_start,args=(times,thread,location,values))
                self.clock_th.setDaemon(True)
                self.clock_th.start()
            except Exception:
                msg_show = "大白说:您输入的时间格式有误，请重新输入"+"\n"
                self._signal.emit(msg_show)
        else:
            msg_show = "大白说:输入有误，请重新输入"+"\n"
            self._signal.emit(msg_show)

    def clock_start(self,tims,thread,location,values):
        while True:
            time_now = datetime.datetime.now()
            time_now = datetime.datetime.strftime(time_now,r'%Y-%m-%d-%H-%M')
            if time_now == tims:
                msg = '大白说:主人距离{}还有{}分钟,地点:{},请尽快准备！\n'.format(thread,values,location)
                self._signal.emit(msg)
                for t in range(5):
                    winsound.Beep(600,1000)
                    time.sleep(1)
                self.enterButton.setEnabled(False)
                break
            time.sleep(1)

    def judge_num(self,num):
        if num < 10:
            num = '0%d'%(num)
        else:
            num = str(num)
        return num

if __name__ == '__main__':
    import sys,os     
    app = QtWidgets.QApplication(sys.argv)
    robot_mainwindow = mainWindow(Saddress)
    robot_mainwindow.show()
    sys.exit(app.exec_())