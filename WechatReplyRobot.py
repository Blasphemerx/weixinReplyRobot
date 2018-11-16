from itchat.content import *
from WeatherForecast import *
from Mp32Wav import *
from SpeechRecognition import *
from ImageRecognition import *
import requests
import json
import itchat
import jieba
import os

itchat.auto_login()

VERSION = "\n【徐福v0.4自动回复】"

AUTO_REPLY_GROUPS = [{"group": u"WeChat测试", "switch": "off"}, {"group": u"505宿舍", "switch": "off"},
                     {"group": u"家庭", "switch": "off"}, {"group": u"小团体", "switch": "off"}]
OFF_KEY_WORDS = ["闭嘴", "shut up", "滚回去", "我会想你的", "解除", "解散"]
ON_KEY_WORDS = ["徐福", "出现", "出来", "召唤", "聊聊", "聊5毛的", "聊10块钱的", "许个愿"]
WEATHER_KEY_WORDS = ["天气", "天气如何", "weather"]

API_KEY = '1CgzeO4SmS4n2MVhq84ZIQ9z'
SECRET_KEY = 'IohPXSvEQxb1ocMmSfxiZbIG7AhSXOnh'

IMAGE_APP_ID = "14828961"
IMAGE_API_KEY = "SGUVZQfgmTOdbFMmNxWBf4SN"
IMAGE_SECRET_KEY = "LfKFht8TqhkAMN6TKnCDiikyWZbz6mq8"

auto_reply_flags = "on"


def tuling(info):
    """
    调用图灵机器人的api，采用爬虫的原理，根据聊天消息返回回复内容
    :param info: 对话内容
    :return: 回答内容
    """
    app_key = "e5ccc9c7c8834ec3b08940e290ff1559"
    url = "http://www.tuling123.com/openapi/api?key=%s&info=%s" % (app_key, info)
    req = requests.get(url)
    content = req.text
    data = json.loads(content)
    answer = data['text'] + VERSION
    return answer


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    """
    注册文本消息，绑定到text_reply处理函数
    text_reply msg_files可以处理好友之间的聊天回复
    :param msg: 对话内容
    :return: 微信回答图灵机器人答案
    """
    global auto_reply_flags
    if exist_in_key_word(msg['Text'], OFF_KEY_WORDS):
        auto_reply_flags = "off"
    elif exist_in_key_word(msg['Text'], ON_KEY_WORDS):
        auto_reply_flags = "on"
    if auto_reply_flags == "on":
        itchat.send('%s' % tuling(msg['Text']), msg['FromUserName'])


@itchat.msg_register([ATTACHMENT, VIDEO])
def download_files(msg):
    msg['Text'](msg['FileName'])
    return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])


@itchat.msg_register(RECORDING)
def speech_recognition(msg):
    msg['Text'](msg['FileName'])
    pcm_file = trans_mp3_to_pcm(msg['FileName'])
    asr = ASR(API_KEY, SECRET_KEY)
    message = asr.do_speech_recognition(pcm_file)
    answer = "您说的是：【" + message + "】吗？" + VERSION
    os.remove(msg['FileName'])
    os.remove(pcm_file)
    itchat.send('%s' % answer, msg['FromUserName'])


@itchat.msg_register(PICTURE)
def image_recognition(msg):
    msg['Text'](msg['FileName'])
    ir = IR(IMAGE_APP_ID, IMAGE_API_KEY, IMAGE_SECRET_KEY)
    context = ir.do_image_recognition(msg['FileName'])
    answer = context + VERSION
    os.remove(msg['FileName'])
    itchat.send('%s' % answer, msg['FromUserName'])


@itchat.msg_register(TEXT, isGroupChat=True)
def group_text_reply(msg):
    """
    现在微信加了好多群，并不想对所有的群都进行设置微信机器人，只针对想要设置的群进行微信机器人，可进行如下设置
    :param msg:
    :return:
    """
    item = get_group_user_name(msg)
    # print("item: " + item)
    if item != "":
        message = msg['Content']
        if exist_in_key_word(message, WEATHER_KEY_WORDS):
            wf = WeatherForecast(None)
            wf_info = wf.get_weather_info()
            itchat.send(u'%s' % wf_info, item)
        else:
            itchat.send(u'%s' % tuling(msg['Text']), item)


@itchat.msg_register(RECORDING, isGroupChat=True)
def group_reording_reply(msg):
    group_id = get_group_id(msg)
    if group_id != "":
        msg['Text'](msg['FileName'])
        pcm_file = trans_mp3_to_pcm(msg['FileName'])
        asr = ASR(API_KEY, SECRET_KEY)
        message = asr.do_speech_recognition(pcm_file)
        answer = "您说的是：" + message + "吗？" + VERSION
        os.remove(msg['FileName'])
        os.remove(pcm_file)
        itchat.send('%s' % answer, group_id)


@itchat.msg_register(PICTURE, isGroupChat=True)
def group_image_reply(msg):
    group_id = get_group_id(msg)
    if group_id != "":
        msg['Text'](msg['FileName'])
        ir = IR(IMAGE_APP_ID, IMAGE_API_KEY, IMAGE_SECRET_KEY)
        context = ir.do_image_recognition(msg['FileName'])
        answer = context + VERSION
        os.remove(msg['FileName'])
        itchat.send('%s' % answer, group_id)


def get_group_id(msg):
    """
    微信群中有文字信息时，针对设置的微信群，按照机器人是否开启的标志，进行应答或忽视
    :param msg: 微信群文字信息
    :return: 微信群id
    """
    from_user_name = msg['FromUserName']
    if msg['ActualUserName'] == msg['FromUserName']:
        from_user_name = msg['ToUserName']
    itchat.get_chatrooms(update=True)
    for group_name in AUTO_REPLY_GROUPS:
        my_rooms = itchat.search_chatrooms(name=group_name.get("group"))
        for room in my_rooms:
            print("UserName: " + room['UserName'])
            print("from_user_name: " + from_user_name)
            if room['NickName'] == group_name.get("group") and room['UserName'] == from_user_name:
                return room['UserName']
            else:
                print("No groups found！")
                continue
    return ""


def get_group_user_name(msg):
    """
    微信群中有文字信息时，针对设置的微信群，按照机器人是否开启的标志，进行应答或忽视
    :param msg: 微信群文字信息
    :return: 微信群id
    """
    context = msg['Content']
    from_user_name = msg['FromUserName']
    if msg['ActualUserName'] == msg['FromUserName']:
        from_user_name = msg['ToUserName']
    itchat.get_chatrooms(update=True)
    for group_name in AUTO_REPLY_GROUPS:
        my_rooms = itchat.search_chatrooms(name=group_name.get("group"))
        ori_switch = group_name.get("switch")
        for room in my_rooms:
            print("UserName: " + room['UserName'])
            print("from_user_name: " + from_user_name)
            if room['NickName'] == group_name.get("group") and room['UserName'] == from_user_name:
                if exist_in_key_word(context, OFF_KEY_WORDS):
                    group_name["switch"] = "off"
                elif exist_in_key_word(context, ON_KEY_WORDS):
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


def exist_in_key_word(context, key_words):
    """
    查找文字信息中是否含有设置好的关键词
    :param context: 微信文字信息
    :param key_words: 关键词
    :return: 含有返回True，不含有返回False
    """
    word_lists = jieba.lcut_for_search(context)
    for word in word_lists:
        if word in key_words:
            return True
    return False


itchat.run()
