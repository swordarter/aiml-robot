from PyQt5 import QtCore,QtGui,QtWidgets

class robot_UI(object):
    def setupUI(self,Form):
        Form.setObjectName('Form')
        Form.resize(800,600)
        self.QtWidgets = QtWidgets
        self.sendButton = QtWidgets.QPushButton(Form)
        self.sendButton.setGeometry(QtCore.QRect(470,500,80,36))
        self.sendButton.setObjectName('sendButton')

        self.QTextEdit_input = QtWidgets.QTextEdit(Form)
        self.QTextEdit_input.setGeometry(QtCore.QRect(10,500,450,36))
        self.QTextEdit_input.setObjectName('QTextEdit_input')

        self.QTextBrowser_show = QtWidgets.QTextBrowser(Form)
        self.QTextBrowser_show.setGeometry(QtCore.QRect(10,50,450,430))
        self.QTextBrowser_show.setObjectName('QTextEdit_show')

        self.clearButton = QtWidgets.QPushButton(Form)
        self.clearButton.setGeometry(QtCore.QRect(560,500,80,36))
        self.clearButton.setObjectName('clearButton')

        self.startButton = QtWidgets.QPushButton(Form)
        self.startButton.setGeometry(QtCore.QRect(660,500,80,36))
        self.startButton.setObjectName('startButton')

        self.enterButton = QtWidgets.QPushButton(Form)
        self.enterButton.setGeometry(QtCore.QRect(680,181,80,36))
        self.enterButton.setObjectName('enterButton')   
    
        self.QTextEdit_TIME = QtWidgets.QTextEdit(Form)
        self.QTextEdit_TIME.setGeometry(QtCore.QRect(580,50,180,36))
        self.QTextEdit_TIME.setObjectName('QTextEdit_TIME')

        self.QTextEdit_THREAD = QtWidgets.QTextEdit(Form)
        self.QTextEdit_THREAD.setGeometry(QtCore.QRect(580,90,180,36))
        self.QTextEdit_THREAD.setObjectName('QTextEdit_THREAD')

        self.QTextEdit_LOCATION = QtWidgets.QTextEdit(Form)
        self.QTextEdit_LOCATION.setGeometry(QtCore.QRect(580,130,180,36))
        self.QTextEdit_LOCATION.setObjectName('QTextEdit_LOCATION')

        self.QLabel_TIME = QtWidgets.QLabel(Form)
        self.QLabel_TIME.setGeometry(QtCore.QRect(500,50,60,36))
        self.QLabel_TIME.setObjectName('QLabel_TIME')

        self.QLabel_THREAD = QtWidgets.QLabel(Form)
        self.QLabel_THREAD.setGeometry(QtCore.QRect(500,90,60,36))
        self.QLabel_THREAD.setObjectName('QLabel_THREAD')

        self.QLabel_LOCATION = QtWidgets.QLabel(Form)
        self.QLabel_LOCATION.setGeometry(QtCore.QRect(500,130,60,36))
        self.QLabel_LOCATION.setObjectName('QLabel_LOCATION')

        self.QTextBrowser_content = QtWidgets.QTextBrowser(Form)
        self.QTextBrowser_content.setGeometry(QtCore.QRect(470,227,320,253))
        self.QTextBrowser_content.setObjectName('QTextEdit_content')
        
        Form.window_pale = QtGui.QPalette()
        Form.window_pale.setBrush(Form.backgroundRole(),QtGui.QBrush(QtGui.QPixmap("./images/picture1.jpg")))
        Form.setPalette(Form.window_pale)
        
        Form.setWindowTitle('chat')
        Form.setWindowIcon(QtGui.QIcon("./images/form.png"))
        
        self.tray = QtWidgets.QSystemTrayIcon()
        self.icon = QtGui.QIcon('./images/form.png')  
        self.tray.setIcon(self.icon)  
         
        self.tray_menu = QtWidgets.QMenu(QtWidgets.QApplication.desktop())


    
        self.retranslateUI(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)


    def retranslateUI(self,Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate('Form','聊天窗口'))
        self.sendButton.setText(_translate('Form','发送消息'))
        self.clearButton.setText(_translate('Form','清除内容'))
        self.startButton.setText(_translate('Form','唤醒大白'))
        self.enterButton.setText(_translate('Form','确定录入'))
        self.QLabel_TIME.setText(_translate('Form','写入时间'))
        self.QLabel_THREAD.setText(_translate('Form','写入事件'))
        self.QLabel_LOCATION.setText(_translate('Form','写入地点'))
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    windget = QtWidgets.QWidget()
    ui = robot_UI()
    ui.setupUI(windget)
    windget.show()
    sys.exit(app.exec_())
