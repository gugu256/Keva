import time


def log(msg):
    with open("log/logs.log", "a") as f:
        f.write(time.asctime() + " : " + msg + "\n")
