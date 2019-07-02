import requests
import ffmpy
import time

source = ""  # Insert stream url
chunk_size = 1024  # bytes
resp_timeout = 5  # secs
delay = 0.5  # secs
path = ""

headers = {
    "user-agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/75.0.3770.100 Safari/537.36"
}


def interpret(link):
    resp = requests.get(link, stream=True, headers=headers, timeout=resp_timeout)

    resp_type = resp.headers["content-type"]

    if resp_type == "application/vnd.apple.mpegurl":
        return "Playlist"
    elif resp_type == "audio/mpeg":
        return "mp3"
    elif resp_type == "video/mp4":
        return "mp4"
    else:
        return "Null"


def extract_stream(source, file, ext):
    with open(file + "." + ext, "ab") as f:
        resp = requests.get(source, stream=True, headers=headers, timeout=resp_timeout)
        for chunk in resp.iter_content(chunk_size):
            f.write(chunk)
        f.close()


def extract_playlist(playlist, path, file):
    resp = requests.get(playlist, headers=headers, timeout=resp_timeout)
    content = resp.content.decode("utf-8").splitlines()
    for line in content:
        if line[0] != "#":
            source = path + line
            extract_stream(source, file, "ts")
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


def main():
    link = input("Insert streaming or playlist link: ")
    file = input("Insert output file name: ")
    ext = interpret(link)
    if ext == "Playlist":
        extract_playlist(link, path, file)
    else:
        extract_stream(link, file, ext)
    print("Process finished.")


if __name__ == "__main__":
    main()
