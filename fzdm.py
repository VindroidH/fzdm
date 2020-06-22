import urllib.request
from bs4 import BeautifulSoup
import re
import execjs 

COMIC_URL = 'https://manhua.fzdm.com/%d/';
 
def getComics():
    map = {}
    for i in range(1, 2):
        url = COMIC_URL%(i)
        soup = getSoup(url)
        if (soup == None):
            print("soup is None")
            return
        
        name = getName(soup)
        latestChapterName = getLatestChapterName(soup)
        latestChapterUrl = getLatestChapterUrl(soup)
        print (name, latestChapterName, latestChapterUrl)
        
        getChapters(soup, url)
        
        map[name] = url
    #print (map)
    return map
    
def getName(soup):
    return soup.find(attrs={'property':'og:novel:book_name'})['content']

def getLatestChapterName(soup):
    return soup.find(attrs={'property':'og:novel:latest_chapter_name'})['content']

def getLatestChapterUrl(soup):
    return soup.find(attrs={'property':'og:novel:latest_chapter_url'})['content']

def getChapters(soup, url):
    map = {}
    lis = soup.find_all('li', 'pure-u-1-2 pure-u-lg-1-4')
    for li in lis:
        a = li.find('a')
        title = a.get('title')
        href = url + a.get('href')
        map[title] = href
    return map

def getContent(url):
    list = []
    for i in range(1, 999):
        index = url + "index_%d.html"%(i)
        soup = getSoup(index)
        if (soup == None):
            return list
            
        reg = re.compile('var mhurl=')
        script = soup.find(text=reg)
        var = script.split('var mhurl=\"')[1]
        mhurl = var.split('\"')[0]
        imgUrl = 'http://p1.manhuapan.com/' + mhurl
        list.append(imgUrl)
        print(imgUrl)
        
    return 0

def getSoup(url):
    try:
        page = urllib.request.urlopen(url)
        html = page.read().decode('utf-8')
    except:
        return None
    return BeautifulSoup(html, 'html.parser')

#comics = getComics()
getContent('https://manhua.fzdm.com/27/515/')