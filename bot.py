#崽崽BOT 重制版
#利用itchat模块 制作崽崽BOT
#天气API：https://www.tianqiapi.com/api/?version=v1&cityid=101110101&appid=[appid]&appsecret=[appsecret] 城市ID 罗源101230104
import requests
import threading
import itchat
import time
import datetime
import json


friend = []
#天气获取
def get_weather():
    url = 'http://t.weather.sojson.com/api/weather/city/101230104'
    html = requests.get(url)
    content = html.text
    text = json.loads(content)
    city = text['cityInfo']['city']
    data = text['data']
    week = data['forecast'][0]['week']
    wendu = data['wendu']
    shidu = data['shidu']
    wea = data['forecast'][0]['type']
    air_tips = data['forecast'][0]['notice'] +"~"+ data['ganmao']
    result = "呼呼~今天已经{}啦~\n今天{}的天气是{}\n气温{} 湿度{}\n{}".format(week,city,wea,wendu,shidu,air_tips)
    return result

#自动回复 (这里使用了免费机器人接口)
def bot_reply(content):

#    url='http://i.itpk.cn/api.php?question='+content
#    html = requests.get(url)
#    result = html.text
#    return result
    url = 'http://i.itpk.cn/api.php'
    datas={
        'question':content,
        'limit':'5',
        'api_key':'f29db2b9138e16680489b04b14e31a12',
        'api_secret':'vs1wo26fh1ju',
        'type':'普通文本'
    }

    html = requests.post(url,data=datas)
    result = html.text
    return result

#启动机器人
def bot_run():
    itchat.auto_login(hotReload=True)
    itchat.run()

#定时推送消息
def bot_push():
    while(True):
        time = datetime.datetime.now()
        hour = time.hour
        minute = time.minute
        times = "{0}{1}".format(hour,minute)
        if(times == '1830' or times == '952' or times == '70'):
            if(Num == 0):
                for i in friend:
                    print(times)
                    string = get_weather()
                    itchat.send(string,toUserName=i)
                    stime = datetime.datetime.now()
                    pstring = '[{}:{}]推送消息:\n{}\n给用户{}'.format(stime.hour,stime.minute,string,i)
                    print(pstring)
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
    if(Text == 'system_get'):
        a = itchat.search_friends('as')[0]['UserName']
        friend.append(a)
        print(friend)
    reply = bot_reply(Text)
    time = datetime.datetime.now()
    string = '[{}:{}]回复消息:{}'.format(time.hour,time.minute,reply)
    print(string)
    itchat.send(reply,toUserName=FromUser)

#Main
def main():
    thr()

#Main
if __name__ == '__main__':
    main()
