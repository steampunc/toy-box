import subprocess
import time

subprocess.call(["windscribe", "connect"])

while True:
    subprocess.call(["windscribe", "disconnect"])
    subprocess.call(["windscribe", "connect"])

    time.sleep(120)
