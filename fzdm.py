import urllib.request
from bs4 import BeautifulSoup
import re
import execjs 

import db

COMIC_URL = 'https://manhua.fzdm.com/%d/';
 
def update_comics(min_id = 1, max_id = 99999):
    # TODO test
    for id in range(min_id, min_id + 1):
        url = COMIC_URL%(id)
        soup = _get_soup(url)
        if (soup == None):
            return
        
        name = __get_soup(soup)
        author = _get_author(soup)
        img = _get_img(soup)
        latest_chapter_name = _get_latest_chapter_name(soup)
        latest_chapter_url = _get_latest_chapter_url(soup)
        print ('comic: ', name, author, img)
        print ('latest: ', latest_chapter_name, latest_chapter_url)
        print ('')

        db.insert_comic(id, name, url, author, img)
        db.insert_latest_chapter(id, latest_chapter_name, latest_chapter_url)
        
        chapters = get_chapters(soup, url)
        index = 0
        for chapter_name in chapters:
            index+=1
            if (index > 3): 
                break
            chapter_url = chapters[chapter_name]
            chapter_imgs = get_content(chapter_url)
            print ('chapter: ', chapter_name, chapter_url)
            
            index2 = 0
            for img in chapter_imgs:
                index2 += 1
                if (index > 3):
                    break
                print ('chapter img: ', img)
            print('')
            #db.insert_chapter(chapter_name, chapter_url)
        
def update_new_comics():
    latest_id = db.get_latest_comic_id()
    new_id = latest_id + 1
    update_comics(new_id)

def __get_soup(soup):
    name = soup.find(attrs={'property':'og:novel:book_name'})['content']
    return name

def _get_author(soup):
    author = soup.find(attrs={'property':'og:novel:author'})['content']
    return author

def _get_img(soup):
    div = soup.find('div', id='content')
    img = div.find('img').get('src')
    return img

def _get_latest_chapter_name(soup):
    name = soup.find(attrs={'property':'og:novel:latest_chapter_name'})['content']
    return name

def _get_latest_chapter_url(soup):
    url = soup.find(attrs={'property':'og:novel:latest_chapter_url'})['content']
    return url

def get_chapters(soup, url):
    map = {}
    lis = soup.find_all('li', 'pure-u-1-2 pure-u-lg-1-4')
    for li in lis:
        a = li.find('a')
        title = a.get('title')
        href = url + a.get('href')
        map[title] = href
    return map

def get_content(url):
    list = []
    for i in range(1, 3):
        index = url + "index_%d.html"%(i)
        soup = _get_soup(index)
        if (soup == None):
            return list
            
        reg = re.compile('var mhurl=')
        script = soup.find(text=reg)
        var = script.split('var mhurl=\"')[1]
        mhurl = var.split('\"')[0]
        imgUrl = 'http://p1.manhuapan.com/' + mhurl
        list.append(imgUrl)
    return list

def _get_soup(url):
    try:
        page = urllib.request.urlopen(url)
        html = page.read().decode('utf-8')
    except:
        return None
    return BeautifulSoup(html, 'html.parser')

#get_content('https://manhua.fzdm.com/27/515/')

update_comics(1)
#update_new_comics()
