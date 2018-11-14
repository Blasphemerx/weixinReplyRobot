from itchat.content import *
from WeatherForecast import *
import requests
import json
import itchat

itchat.auto_login()

AUTO_REPLY_GROUPS = [{"group": u"WeChat测试", "switch": "off"}, {"group": u"505宿舍", "switch": "off"}, {"group": u"家庭", "switch": "off"}, {"group": u"小团体", "switch": "off"}]


def tuling(info):
    """
    调用图灵机器人的api，采用爬虫的原理，根据聊天消息返回回复内容
    :param info:
    :return:
    """
    app_key = "e5ccc9c7c8834ec3b08940e290ff1559"
    url = "http://www.tuling123.com/openapi/api?key=%s&info=%s" % (app_key, info)
    req = requests.get(url)
    content = req.text
    data = json.loads(content)
    answer = data['text'] + "\n【徐福v0.2自动回复】"
    return answer


def group_id(name):
    """
    对于群聊信息，定义获取想要针对某个群进行机器人回复的群ID函数
    :param name:
    :return:
    """
    df = itchat.get_chatrooms(update=True)
    df = itchat.search_chatrooms(name=name)
    print(df[0]['UserName'])
    return df[0]['UserName']


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    """
    注册文本消息，绑定到text_reply处理函数
    text_reply msg_files可以处理好友之间的聊天回复
    :param msg:
    :return:
    """
    itchat.send('%s' % tuling(msg['Text']), msg['FromUserName'])


@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    msg['Text'](msg['FileName'])
    return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])


@itchat.msg_register(TEXT, isGroupChat=True)
def group_text_reply(msg):
    """
    现在微信加了好多群，并不想对所有的群都进行设置微信机器人，只针对想要设置的群进行微信机器人，可进行如下设置
    :param msg:
    :return:
    """
    # 当然如果只想针对@你的人才回复，可以设置if msg['isAt']:
    # 根据自己的需求设置
    # item = group_id(u'WeChattesting')
    # print(msg['ToUserName'])
    # if msg['ToUserName'] == item:

    item = get_group_user_name(msg)
    # print("item: " + item)
    if item != "":
        if "天气如何" in msg['Content'] or "weather" in msg['Content'] or "天气" in msg['Content']:
            wf = WeatherForecast(None)
            wf_info = wf.get_weather_info()
            itchat.send(u'%s' % wf_info, item)
        else:
            itchat.send(u'%s' % tuling(msg['Text']), item)


def get_group_user_name(msg):
    context = msg['Content']
    from_user_name = msg['FromUserName']
    if msg['ActualUserName'] == msg['FromUserName']:
        from_user_name = msg['ToUserName']
    my_rooms = itchat.get_chatrooms(update=True)
    for group_name in AUTO_REPLY_GROUPS:
        my_rooms = itchat.search_chatrooms(name=group_name.get("group"))
        ori_switch = group_name.get("switch")
        for room in my_rooms:
            print("UserName: " + room['UserName'])
            print("from_user_name: " + from_user_name)
            if room['NickName'] == group_name.get("group") and room['UserName'] == from_user_name:
                if "闭嘴" in context or "shut up" in context or "滚回去" in context or "我会想你的" in context or "解散" in context:
                    group_name["switch"] = "off"
                elif "徐福" in context or "出现" in context or "出来" in context or "召唤" in context or "聊聊" in context or "聊5毛的" in context:
                    group_name["switch"] = "on"

                if msg['ActualUserName'] == msg['FromUserName']:
                    if group_name.get("switch") == "on" and ori_switch == "off":
                        print("myself first time turn on")
                        return room['UserName']
                    elif group_name.get("switch") == "off" and ori_switch == "on":
                        print("myself first time turn off")
                        return room['UserName']
                    else:
                        print("switch is off")
                        continue
                else:
                    if group_name.get("switch") == "on":
                        print("first time turn on")
                        return room['UserName']
                    elif group_name.get("switch") == "off" and ori_switch == "on":
                        print("first time turn off")
                        return room['UserName']
                    else:
                        print("turn off")
                        continue
            else:
                print("No groups found！")
                continue
    return ""


itchat.run()
