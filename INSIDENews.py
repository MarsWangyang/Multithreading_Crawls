import threading
import requests
from bs4 import BeautifulSoup
import time
import random


class Crawls(threading.Thread):
    def __init__(self, urls, path, pageNum):
        threading.Thread.__init__(self)
        self.urls = urls
        self.lock = threading.Lock()
        self.path = path
        self.pageNum = pageNum


    def run(self):
        self.file = self.path + '/INSIDE_News(AI)_Link.txt'

        for url in self.urls:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "lxml")

            titles = soup.find_all("h3", {"class": "post_title"})
            website = soup.select('div.post_list_item_content a[class^="js-auto_break_title"]')


            self.lock.acquire()
            with open(self.file, 'w') as file:
                for i in range(len(website)):
                    link = website[i]['href']
                    title = titles[i].getText().strip()
                    file.write('Title: ' + title + '\nWebsite: ' + link + '\n')
            self.lock.release()

            time.sleep(random.randint(1, 5))

def Inside(path, keyword, page):

    thread = []
    base_url = "https://www.inside.com.tw/tag/AI"
    urls = [f"{base_url}?page={page}" for page in range(1, int(page)+1)]


    threads = []
    for i in range(int(page)):
        threads.append(Crawls([urls[i]], path, int(page)))
        threads[i].start()

    for i in range(int(page)):
        threads[i].join()

