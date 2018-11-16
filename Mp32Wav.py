from pydub import *
import time
import subprocess


def trans_mp3_to_wav(file_path):
    t = time.time()
    now_time = int(t * 1000000)
    print(now_time)
    output_file_name = str(now_time) + ".wav"
    audio = AudioSegment.from_mp3(file_path)
    audio.set_frame_rate(16000).set_channels(1)
    audio.export(out_f=output_file_name, format="wav")
    return output_file_name


def trans_mp3_to_pcm(file_path):
    t = time.time()
    now_time = int(t * 1000000)
    print(now_time)
    output_file_name = str(now_time) + ".pcm"
    audio = AudioSegment.from_mp3(file_path)
    # audio.set_frame_rate(16000).set_channels(1)
    audio.export(out_f=output_file_name, format="s16le", parameters=["-ar", "16000", "-ac", "1", "-acodec", "pcm_s16le"])
    return output_file_name
