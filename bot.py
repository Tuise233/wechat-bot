import itchat
import re
import requests
import datetime
import time
import json

def get_sentence(api): #每日一句
        sentence = requests.get(api)
        return sentence.json()

def get_weather(api): #天气预报
        response = requests.get(api)
        return response.json()

def get_trans(content): #翻译
        url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
        post_form = {
                'i':content,
                'from':'AUTO',
                'to':'AUTO',
                'smartresult':'dict',
                'client':'fanyideskweb',
                'salt':'15611977983364',
                'sign':'8d7e3648b57bb328b326a08eb9928c2b',
                'ts':'1561197798336',
                'bv':'e2a78ed30c66e16a857c5b6486a1d326',
                'doctype':'json',
                'version':'2.1',
                'keyfrom':'fanyi.web',
                'action':'FY_BY_REALTlME'
        }
        response = requests.post(url,data=post_form)
        translate_json = response.text
        translate_dict = json.loads(translate_json)
        result = translate_dict['translateResult'][0][0]['tgt']
        return result

def auto_chat(text):
        url = 'http://api.qingyunke.com/api.php?key=free&appid=0&msg={}'.format(text)
        datas={
                "key":"free",
                "appid":"0",
                "msg":text
        }
        response = requests.post(url,data=datas)
        html = json.loads(response.text)
        return html['content']

def get_daytips():
        while True:
                jsAPI = 'http://open.iciba.com/dsapi/'
                tqAPI = 'https://www.tianqiapi.com/api/'
                sentence = get_sentence(jsAPI)
                content = sentence['content'] #英文句子
                note = sentence['note']
                weather = get_weather(tqAPI)
                info = weather['data'][0]
                tips = '城市:{}\n日期:{}\n空气指数:{} - {}\n天气情况:{}\n小提示:{}\n'.format(weather['city'],info['date'],info['air'],info['air_level'],info['wea'],info['air_tips'])
                users = itchat.search_friends('as') #搜索发送UserName (崽崽 = 用户备注)
                UserName = users[0]['UserName']
                while True:
                        time = datetime.datetime.now()
                        year = time.year
                        month = time.month
                        day = time.day
                        hour = time.hour
                        minute = time.minute
                        now = '现在是北京时间{}.{}.{} {}:{}'.format(year,month,day,hour,minute)
                        if hour == 10 and minute == 41:
                                string = '[崽崽BOT]\n{}\n\n每日一句:{}\n{}\n\n天气信息:\n{}'.format(now,content,note,tips)
                                itchat.send_msg(string,UserName)
                                break

#返回用户输入的参数
@itchat.msg_register(itchat.content.TEXT)
def print_content(msg):
        FromUserName = msg['FromUserName']
        ToUserName = msg['ToUserName']
        text = msg['Text']
        if text.find('_') != -1:
                CutText = text.split('_')
                if CutText[0] == '翻译':
                        trans = get_trans(CutText[1])
                        itchat.send_msg('[崽崽BOT]\n翻译结果:{}'.format(trans),toUserName = FromUserName)
        else:
                result = auto_chat(text)
                if result.find('菲菲') != -1:
                        replaced = result.replace('菲菲','崽崽')
                        itchat.send_msg('[崽崽BOT]\n{}'.format(replaced),toUserName = FromUserName)
                        return
                itchat.send_msg('[崽崽BOT]\n{}'.format(result),toUserName = FromUserName)
        
if __name__ == '__main__':
        itchat.auto_login(hotReload=True)
        itchat.run()
        
