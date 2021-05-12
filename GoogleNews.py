import threading
import time
from bs4 import BeautifulSoup
import requests
from urllib.parse import quote
import lxml
import random
from fake_useragent import UserAgent

#google news
class googleNews(threading.Thread):
    def __init__(self, base_url, url, path):
        threading.Thread.__init__(self)
        self.base_url = base_url
        self.url = url
        self.lock = threading.Lock()
        self.path = path


    def run(self):
        self.res = requests.get(self.url)
        self.soup = BeautifulSoup(self.res.text, 'lxml')
        self.title_html = self.soup.select('h3.zBAuLc  div')
        self.website_html = self.soup.select('div.ZINbbc.xpd.O9g5cc.uUPGi > div.kCrYT > a[href^="/url"]')
        self.website_urls = [self.website_html[i]['href'].strip('/url?q=') for i in range(len(self.website_html))]
        self.file = self.path + '/google_Link.txt'



        self.lock.acquire()
        with open(self.file, 'w') as file:
            for title, link in zip(self.title_html, self.website_urls):
                #print('Title: ', title.text)
                #print('Website: ', link)
                file.write('Title: '+title.text+'\nWebsite: '+link+'\n')
        self.lock.release()

        time.sleep(random.randint(1,5))




def google(path, keyW, pageN):
    start_time = time.time()
    user_agent = UserAgent()
    headers = {'User-Agent': user_agent.random}
    keyword = quote(keyW.encode('utf8'))
    pageNum = int(pageN)
    base_url = 'https://www.google.com.tw'
    search_url = base_url + f'/search?q={keyword}&gbv=2&tbm=nws'

    urls = []

    for _ in range(pageNum):
        urls.append(search_url)
        res = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(res.text, 'lxml')
        next_page_html = soup.select('div.nMymef.MUxGbd.lyLwlc > a[aria-label^="下一頁"]')
        next_url = base_url + next_page_html[0]['href']
        search_url = next_url

    threads = []
    #lock = threading.Lock()
    for i in range(len(urls)):
        threads.append(googleNews(base_url, urls[i], path))
        threads[i].start()

    for i in range(len(urls)):
        threads[i].join()

    end_time = time.time()
    print(f"{end_time - start_time} 秒爬取 {pageNum} 頁的文章")
    print('-------End-------')

