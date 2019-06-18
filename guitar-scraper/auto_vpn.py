import subprocess
import time

while True:
    subprocess.call(["windscribe", "disconnect"])
    subprocess.call(["windscribe", "connect"])
    subprocess.call(["killall", "python3"])
    subprocess.call(["find", "./song_urls/", "-empty", "|", "xargs", "rm"]) 

    time.sleep(200)
