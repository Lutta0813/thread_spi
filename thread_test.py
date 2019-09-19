import requests
from bs4 import BeautifulSoup
import threading


def url_setting():
    url = 'https://www.ptt.cc/bbs/Gossiping/index.html'
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        'refer': 'https://www.ptt.cc/bbs/Gossiping/index.html'
    }
    result = requests.Session()
    r = result.get(url, headers=headers, allow_redirects=False)


def get_data_threading_1():



def multitreading():
    thread_1 = threading.Thread(target=get_data_threading_1, name='T1')
    thread_1.start()



def main():
    multitreading()


if __name__ = '__main__':
    main()