import urllib.request
from bs4 import BeautifulSoup as Soup
import re
from wxpy import *
from threading import Timer

def get_info(uri, page_range):
    send_text = ''
    for page in range(1, page_range):
        html = urllib.request.urlopen(uri + str(page)).read()
        soup = Soup(html, 'lxml')
        table = soup.findAll('tbody', id=re.compile('[a-z]+thread_[0-9]+'))
        for ele in table:
            link = ele.find('a', attrs={'class': 's xst'})
            href = 'http://bay123.com/' + link['href']
            text = link.get_text()
            send_text += text + '\n' + href + '\n' + '\n'
        send_text += '-----------------------------------------\n'
    return send_text

def send(friend, uri, page_range):
    try:
        text = get_info(uri, page_range)
        friend.send(text)
        t = Timer(86400, send, args=(friend, uri, page_range))
        t.start()
    except:
        print('send fail')

if __name__ == "__main__":
    bot = Bot()
    friend = bot.friends().search('mumu')[0]

    uri = 'http://bay123.com/forum.php?mod=forumdisplay&fid=40&filter=typeid&typeid=38&page='
    page_range = 3

    send(friend, uri, page_range)


