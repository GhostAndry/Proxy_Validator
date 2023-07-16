import os
import datetime

f = None

def __init__():
    x = datetime.datetime.now()
    datetime_str = x.strftime("%d%m%Y%H%M%S")
    global f
    try:
        f = open(f"logs/{datetime_str}.log", "a", encoding="utf-8")
    except:
        os.makedirs("logs", exist_ok=True)
        f = open(f"logs/{datetime_str}.log", "a", encoding="utf-8")

def log(message, console=True):
    x = datetime.datetime.now()
    datetime_str = x.strftime("%d-%m-%Y %H:%M:%S")
    if console:
        print(f"[{datetime_str}] {message}")
        f.write(f"[{datetime_str}] {message}\n")
    else:
        f.write(f"[{datetime_str}] {message}\n")
    f.flush()

def close():
    f.close()
