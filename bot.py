#崽崽BOT 重制版
#利用itchat模块 制作崽崽BOT
#天气API：https://www.tianqiapi.com/api/?version=v1&cityid=101110101&appid=[appid]&appsecret=[appsecret] 城市ID 罗源101230104
import requests
import threading
import itchat
import time
import datetime
import json

#天气获取
def get_weather():
    url = 'https://www.tianqiapi.com/api/?version=v1&cityid=101230104&appid=[appid]&appsecret=[appsecret]'
    html = requests.get(url)
    content = html.text
    text = content.encode('utf-8').decode('unicode_escape')
    jtext = json.loads(text)
    city = jtext['city']
    datas = jtext['data'][0]
    date = datas['date']
    week = datas['week']
    wea = datas['wea']
    air_level = datas['air_level']
    air_tips = datas['air_tips']
    result = "{}\n呼呼~今天已经{}啦~\n今天{}的天气是{},空气质量{}\n{}".format(date,week,city,wea,air_level,air_tips)
    return result

#自动回复 (这里使用了免费机器人接口)
def bot_reply(content):
    url='http://i.itpk.cn/api.php?question='+content
    html = requests.get(url)
    result = html.text
    return result

#启动机器人
def bot_run():
    itchat.auto_login(hotReload=True)
    itchat.run()

#定时推送消息
def bot_push():
    friend = ['@5bf1ad9889d7a642dcdd7b54472629f95edd1d9d5b43815cda50488cc61be76d','@2a020a846b287bf7d19bd2664537c0527c947e80a94d7c13c893c0cdb066a301']
    while(True):
        time = datetime.datetime.now()
        hour = time.hour
        minute = time.minute
        times = "{0}{1}".format(hour,minute)
        if(times == '1830' or times == '0700' or times == '700'):
            if(Num == 0):
                for i in friend:
                    string = get_weather()
                    itchat.send(string,toUserName=i)
                Num = 1
        else:
            Num = 0
            
#多线程启动
def thr():
    thr_bot = threading.Thread(target=bot_run)
    thr_tips = threading.Thread(target=bot_push)
    thr_bot.start()
    thr_tips.start()

#消息注册
@itchat.msg_register(itchat.content.TEXT)
def auto_reply(msg):
    FromUser = msg['FromUserName']
    ToUser = msg['ToUserName']
    Text = msg['Text']
    reply = bot_reply(Text)
    print(reply)
    itchat.send(reply,toUserName=FromUser)

#Main
def main():
    thr()

#Main
if __name__ == '__main__':
    main()
