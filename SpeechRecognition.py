# coding=utf-8

import json
import base64
import time

from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode

timer = time.perf_counter

# 根据文档填写PID，选择语言及识别模型
DEV_PID = 1536  # 1537 表示识别普通话，使用输入法模型。1536表示识别普通话，使用搜索模型

CUID = '123456PYTHON'
# 采样率
RATE = 16000  # 固定值

ASR_URL = 'http://vop.baidu.com/server_api'


class DemoError(Exception):
    pass


"""  TOKEN start """

TOKEN_URL = 'http://openapi.baidu.com/oauth/2.0/token'
SCOPE = 'audio_voice_assistant_get'  # 有此scope表示有asr能力，没有请在网页里勾选


class ASR:
    def __init__(self, api_key, secret_key):
        self.key = api_key
        self.secret = secret_key
        self.token = self.fetch_token()

    def fetch_token(self):
        params = {'grant_type': 'client_credentials',
                  'client_id': self.key,
                  'client_secret': self.secret}
        post_data = urlencode(params).encode('utf-8')
        req = Request(TOKEN_URL, post_data)
        try:
            f = urlopen(req)
            result_str = f.read()
        except URLError as err:
            print('token http response http code : ' + str(err))
            result_str = str(err)

        print(result_str)
        result = json.loads(result_str)
        print(result)
        if 'access_token' in result.keys() and 'scope' in result.keys():
            if SCOPE not in result['scope'].split(' '):
                raise DemoError('scope is not correct')
            print('SUCCESS WITH TOKEN: %s ; EXPIRES IN SECONDS: %s' % (result['access_token'], result['expires_in']))
            return result['access_token']
        else:
            raise DemoError(
                'MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')

    """  TOKEN end """

    def do_speech_recognition(self, audio_file):
        with open(audio_file, 'rb') as speech_file:
            speech_data = speech_file.read()
        length = len(speech_data)
        if length == 0:
            raise DemoError('file %s length read 0 bytes' % audio_file)
        speech = base64.b64encode(speech_data)
        speech = str(speech, 'utf-8')
        params = {'dev_pid': DEV_PID,
                  'format': audio_file[-3:],
                  'rate': RATE,
                  'token': self.token,
                  'cuid': CUID,
                  'channel': 1,
                  'speech': speech,
                  'len': length
                  }
        post_data = json.dumps(params, sort_keys=False)
        # print post_data
        req = Request(ASR_URL, post_data.encode('utf-8'))
        req.add_header('Content-Type', 'application/json')
        try:
            begin = timer()
            f = urlopen(req)
            result_str = f.read()
            print("Request time cost %f" % (timer() - begin))
        except URLError as err:
            print('asr http response http code : ' + str(err))
            result_str = str(err)

        print(result_str)
        result_str = str(result_str, 'utf-8').split(',')[3].replace("\"result\":", "")
        return result_str
