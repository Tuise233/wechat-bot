import itchat
from itchat.content import *
import re
import requests
import datetime
import time

def get_sentence(api):
        sentence = requests.get(api)
        return sentence.json()

def get_weather(api):
        response = requests.get(api)
        return response.json()

if __name__ == '__main__':
        jsAPI = 'http://open.iciba.com/dsapi/'
        tqAPI = 'https://www.tianqiapi.com/api/'
        itchat.auto_login(hotReload=True)
        sentence = get_sentence(jsAPI)
        content = sentence['content'] #英文句子
        note = sentence['note']
        weather = get_weather(tqAPI)
        info = weather['data'][0]
        tips = '城市:{}\n日期:{}\n空气指数:{} - {}\n天气情况:{}\n小提示:{}\n'.format(weather['city'],info['date'],info['air'],info['air_level'],info['wea'],info['air_tips'])
        users = itchat.search_friends('崽崽') #搜索发送UserName (崽崽 = 用户备注)
        UserName = users[0]['UserName']
        while True:
                time = datetime.datetime.now()
                year = time.year
                month = time.month
                day = time.day
                hour = time.hour
                minute = time.minute
                now = '现在是北京时间{}.{}.{} {}:{}'.format(year,month,day,hour,minute)
                if hour == 11 and minute == 37:
                        string = '[崽崽BOT]\n{}\n\n每日一句:{}\n{}\n\n天气信息:\n{}'.format(now,content,note,tips)
                        itchat.send_msg(string,UserName)
                        break
        itchat.run()
