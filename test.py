from WeatherForecast import *
from Mp32Wav import *
from SpeechRecognition import *
from ImageRecognition import *


API_KEY = '1CgzeO4SmS4n2MVhq84ZIQ9z'
SECRET_KEY = 'IohPXSvEQxb1ocMmSfxiZbIG7AhSXOnh'

IMAGE_APP_ID = "14828961"
IMAGE_API_KEY = "SGUVZQfgmTOdbFMmNxWBf4SN"
IMAGE_SECRET_KEY = "LfKFht8TqhkAMN6TKnCDiikyWZbz6mq8"

# wf = WeatherForecast(None)
# weather_info = wf.get_weather_info()
# print(weather_info)

# wav_file_name = trans_mp3_to_wav("181115-153957.mp3")
# pcm_file = trans_mp3_to_pcm("181115-162703.mp3")
#
# asr = ASR(API_KEY, SECRET_KEY)
# message = asr.do_speech_recognition(pcm_file)
# print(message)

ir = IR(IMAGE_APP_ID, IMAGE_API_KEY, IMAGE_SECRET_KEY)
context = ir.do_image_recognition("181116-152230.png")
print(context)

