import requests
import ffmpy
import time

source = ""  # Insert stream url
file = ""  # Insert target media file
chunk_size = 1024  # bytes
resp_timeout = 5  # secs
delay = 0.5  # secs

headers = {
    'user-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/75.0.3770.100 Safari/537.36'
}


def extract(source, file):
    with open(file, "ab") as f:
        resp = requests.get(source, stream=True, headers=headers, timeout=resp_timeout)
        for chunk in resp.iter_content(chunk_size):
            f.write(chunk)
        f.close()


# extract(source, file)

playlist = ""  # Insert playlist file url
path = ""  # Insert streaming media root here


def filter(playlist, path):
    resp = requests.get(playlist, headers=headers, timeout=resp_timeout)
    content = resp.content.decode("utf-8").splitlines()
    for line in content:
        if line[0] != "#":
            source = path + line
            extract(source, file)
            time.sleep(delay)


#  filter(playlist, path)

video_file = ""  # Insert video file here
audio_file = ""  # Insert audio file here
output_file = ""  # Insert output media file name here


def mux(video_file, audio_file, output_file):
    Ff = ffmpy.FFmpeg(
        inputs={video_file: None, audio_file: None},
        outputs={output_file: "-b:v 1M"}
    )
    ff.run()


# mux(video_file, audio_file, output_file)

print("Process finished.")
