import requests
import ffmpy
import time
import os

source = ""  # Insert stream url
chunk_size = 1024  # bytes
resp_timeout = 5  # secs
delay = 0.5  # secs
temp_file = "temp.ts"

headers = {
    "user-agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/75.0.3770.100 Safari/537.36"
}


def extract(source, temp_file):
    print("Extracting")
    
    with open(temp_file, "ab") as f:
        resp = requests.get(source, stream=True, headers=headers, timeout=resp_timeout)
        for chunk in resp.iter_content(chunk_size):
            f.write(chunk)


def interpret(playlist_url, temp_file):
    print("Interpreting playlist") 
    prefix = playlist_url.split("/sec")[0]
    
    resp = requests.get(playlist_url, headers=headers, timeout=resp_timeout)
    content = resp.content.decode("utf-8").splitlines()
    for line in content:
        if line[0] != "#":
            source = prefix + line
            extract(source, temp_file)
            time.sleep(delay)


def convert(temp_file, output_file):
    ff = ffmpy.FFmpeg(
        inputs={temp_file: None},
        outputs={output_file: None}
    )
    ff.run()


def main():
    playlist_url = input("Insert playlist url: ")
    output_file = input("Output file name: ") + ".mp4"
    interpret(playlist_url, temp_file)
    convert(temp_file, output_file)
    os.remove(temp_file)
    input("Process finished.")


if __name__ == "__main__":
    main()
