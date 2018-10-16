# _*_ coding: utf-8 _*_
import aiml
import os

mybot_path = '.'

class myBot(object):
    def __init__(self):
        self.path = mybot_path
        self.name = '大白'
        self.gender = "unknown"

    def robotborn(self):
        os.chdir(self.path)
        self.mybot = aiml.Kernel()
        self.mybot.learn('settings/std-startup.xml')
        self.mybot.respond('LOAD AI')
    
    def robothandler(self,inputs):
        msg = inputs
        response = self.mybot.respond(msg)
        return response

