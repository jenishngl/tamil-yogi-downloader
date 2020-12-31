import sys
import requests
import queue
import re
import os
from subprocess import call
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import unquote_plus
from threading import Thread
from progress.bar import Bar

q = queue.Queue()
num_of_threads = 20
FFMPEG_DIR = ""
TEMP_DIR = "video1"
available_resolutions = []
# bar = Bar()

def initialize_threads():
    print(f"Setting up {num_of_threads} Threads for processing")
    for _ in range(num_of_threads):
        worker = Thread(target=doWork, args=(q,))
        worker.setDaemon(True)
        worker.start()

def downloadFile(arr):
    r = requests.get(arr[1])
    if not os.path.exists(TEMP_DIR):
        os.mkdir(TEMP_DIR)
    try:
        open(os.path.join(TEMP_DIR,str(arr[0])), "wb").write(r.content)
        bar.next()
    except Exception as e:
        error = e
        print(error)
        print(f"Error in saving : {str(arr[0])}")

def doWork(q):
    while True:
        downloadFile(q.get())
        q.task_done()

def get_choice():
    option = int(input()) - 1
    if (option > -1 and option <= len(available_resolutions)):
        print(f"You have selected {available_resolutions[option]['resolution']}")
        return {"status": False, "option": option}
    else:
        print("Please select a valid option")
        return {"status": True, "option": None}

def get_masterfile(URL):
    options = Options()
    options.headless = True
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options,executable_path=r"chromedriver.exe")
    print("Loading the URL...")
    try:
        global bar, title, uncleaned_title
        driver.get(URL)
        uncleaned_title = driver.execute_script('return window._wp_rp_post_title')
        title = unquote_plus(uncleaned_title)
        print("Searching video player...")
        vframe = [frame for frame in driver.find_elements_by_tag_name("iframe") if "vidorg.net" in frame.get_attribute('src')]
        if len(vframe) > 0:
            driver.switch_to.frame(vframe[0])
            master_URL = driver.execute_script('return jwplayer("vplayer").getConfig().playlistItem.file')
            r = requests.get(master_URL)
            masterfile_contents = r.content
            formats = re.findall(r'(#EXT-X-STREAM-INF):(PROGRAM-ID=\d+),(BANDWIDTH=\d+),(RESOLUTION=\d+x\d+),(FRAME-RATE=[.*\d]+),(CODECS=[.\"\w\d,]+)\n(http://[a-zA-z0-9-./]+)',masterfile_contents.decode("utf-8"))
            for f in formats:
                available_resolutions.append({"resolution": str(f[3]).split("=")[1], "master_url" : str(f[6])})
            print(f"Available Resolutions for {title} are:")
            for i, resol in enumerate(available_resolutions):
                print(f"{i+1}) {resol['resolution']}")
            option = {"status": True, "option": None}
            while(option["status"]):
                option = get_choice()
            option = option["option"]
            BASE_URL = str(available_resolutions[option]["master_url"])
            INDEX_BASE_URL = BASE_URL.rsplit('/',1)[0]
            INDEX_FILENAME = BASE_URL.rsplit('/',1)[1]
            r = requests.get(available_resolutions[option]["master_url"])
            indexfile_contents = r.content
            parts = re.findall(r'(#EXTINF:[0-9]+[.]*[0-9]+,\n)(seg-[0-9-.a-zA-Z]+)',indexfile_contents.decode("utf-8"))
            print("Initializing the Threads..")
            initialize_threads()
            q.put((INDEX_FILENAME, available_resolutions[option]["master_url"]))
            print("Queuing all tasks for download")
            for p in parts:
                q.put((str(p[1]), INDEX_BASE_URL + "/" + str(p[1])))
            pending_tasks = q.unfinished_tasks
            print(f"Waiting for all {pending_tasks} files to be downloaded...")
            bar = Bar('Downloading', max=pending_tasks)
            q.join()
            bar.finish()
            print("All files are downloaded")
            INDEX_FILE_PATH = TEMP_DIR + "/" + INDEX_FILENAME
            call(f"ffmpeg.exe -i {INDEX_FILE_PATH} -c copy -bsf:a aac_adtstoasc {uncleaned_title}.mp4", shell=True)
            call(f"rd /s /q {TEMP_DIR}", shell=True)
        else:
            print("Unable to fetch the data")
    except Exception as e:
        error = e
        print(error)

def main():
    if len(sys.argv) == 2:
        URL = sys.argv[1]
        get_masterfile(URL)
    else:
        print("missing arguments in script. FORMAT: python main.py <ticker> eg. python main.py AAPL")

if __name__=="__main__":
    main()