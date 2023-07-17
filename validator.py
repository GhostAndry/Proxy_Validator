import subprocess
from threading import Thread, Lock
import time
import logger
import os

subprocess.call('cls', shell=True)

lock = Lock()

threads = []
proxy_list = []
proxy_types = ["http", "https", "socks5", "socks4"]

logger.__init__()

proxies_file = input("Proxy file (Default: proxies.txt): ")
if len(proxies_file) == 0:
    proxies_file = "proxies.txt"

while True:
    try:
        num_threads = int(input("Number of threads: "))
        break
    except ValueError:
        print("Please enter a valid number of threads")

while True:
    try:
        loop = int(input("Repetitions: "))
        break
    except ValueError:
        print("Please enter a valid Loops")

def clear_file(filename):
    try:
        os.remove(filename)
    except:
        pass

def load_proxies_from_file(filename):
    with open(filename, "r") as file:
        proxies = file.read().splitlines()
    return proxies

def check_proxy(ip, port, proxy_type):
    command = f"curl --proxy {proxy_type}://{ip}:{port} --max-time 20 https://www.google.com"
    try:
        subprocess.check_call(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

def write_to_file(ip, port, ptype):
    with open("proxy_list.txt", "a") as file:
        file.write(f"{ip}:{port}:{ptype}\n")

def remove_duplicates(filename):
    lines_seen = set()  # Insieme per tenere traccia delle righe uniche
    output_lines = []

    with open(filename, "r") as file:
        for line in file:
            if line not in lines_seen:
                output_lines.append(line)
                lines_seen.add(line)

    with open(filename, "w") as file:
        file.writelines(output_lines)

def format_thread_num(thread_num, num_threads):
    if len(str(num_threads)) > 1:
        return str(thread_num).zfill(len(str(num_threads)))
    else:
        return str(thread_num)

def run_check_proxy(thread_num, lock, proxies):
    for proxy in proxies:
        for ptype in proxy_types:
            if check_proxy(proxy.split(':')[0], proxy.split(':')[1], ptype):
                with lock:
                    formatted_thread_num = format_thread_num(thread_num, num_threads)
                    logger.log(f"Thread {formatted_thread_num}: ✅ ({ptype}) {proxy}")
                    write_to_file(proxy.split(':')[0], proxy.split(':')[1], ptype)
            else:
                with lock:
                    formatted_thread_num = format_thread_num(thread_num, num_threads)
                    logger.log(f"Thread {formatted_thread_num}: ❌ ({ptype}) {proxy}")

subprocess.call('cls', shell=True)

clear_file("proxy_list.txt")

subprocess.call('cls', shell=True)

logger.log(f"Starting proxy checker with {num_threads} threads and {loop} repetitions.")

logger.log(f"Loading proxies...", True)
time.sleep(0.5)
proxies = load_proxies_from_file(proxies_file)
logger.log(f"Loaded {len(proxies)} proxies", True)
time.sleep(0.5)
logger.log(f"Starting proxy checker...", True)
time.sleep(1)

for _ in range(loop):
    for i in range(num_threads):
        thread_proxies = [proxy for index, proxy in enumerate(proxies) if index % num_threads == i]
        thread = Thread(target=run_check_proxy, args=(i + 1, lock, thread_proxies))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

subprocess.call('cls', shell=True)

remove_duplicates("proxy_list.txt")

try:
    with open("proxy_list.txt", 'r') as f:
        working_proxies = f.read().splitlines()
    logger.log(f"Proxy checking completed. Checked: {len(proxies)}  Working: {len(working_proxies)}.")
except:
    logger.log(f"Proxy checking completed. Checked: 0.")

logger.close()
