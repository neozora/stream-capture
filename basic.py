import requests
import ffmpy
import time

headers = {
    'user-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/75.0.3770.100 Safari/537.36'
}


# extraction

source_url = "<Insert stream url here>"
file = "<Insert target media file here>"
chunk_size = 1024 # bytes
resp_timeout = 5 # secs


def extract(source_url, file):
    with open(file, "ab") as f:
        resp = requests.get(source_url, stream=True, timeout=resp_timeout)
        for chunk in resp.iter_content(chunk_size):
            f.write(chunk)


# filtration

delay = 0.5 # secs
playlist_url = "<Insert playlist url here>"


def filter(playlist_url):
    resp = requests.get(playlist_url, timeout=resp_timeout)
    content = resp.content.decode("utf-8").splitlines()
    for line in content:
        if line[0] != "#":
            extract(line, file)
            time.sleep(delay)


# conversion / multiplex

video_file = "<Insert video file here>"
audio_file = "<Insert audio file here>"
output_file = "<Insert output media file name here>"


def mux(video_file, audio_file, output_file):
    Ff = ffmpy.FFmpeg(
            inputs = {video_file: None, audio_file: None},
            outputs = {output_file: "-b:v 1M" }
    )
    ff.run()
