import sqlite3

DB = 'fzdm.db'
TABLE_COMICS = 'comics'
TABLE_LATEST_CHAPTERS = 'latest_chapters'
TABLE_CHAPTERS = 'chapters'
TABLE_CHAPTER_IMAGES = 'chapter_images'
TABLE_FAVOURITE_COMICS = "favourite_comics"
TABLE_USERS = "users"

def create_tables():
    conn = sqlite3.connect(DB)
    try:
        sql = '''
        CREATE TABLE IF NOT EXISTS %s
            (ID INTEGER PRIMARY KEY NOT NULL,
            NAME TEXT NOT NULL,
            URL TEXT NOT NULL,
            AUTHOR TEXT,
            IMG TEXT
            )
        ''' % (TABLE_COMICS)
        conn.execute(sql)
        sql = '''
        CREATE TABLE IF NOT EXISTS %s
            (ID INTEGER PRIMARY KEY NOT NULL,
            NAME TEXT NOT NULL,
            URL TEXT NOT NULL
            )
        ''' % (TABLE_LATEST_CHAPTERS)
        conn.execute(sql)
        
        sql = '''
        CREATE TABLE IF NOTE EXISTS %s
            (ID INTEGER PRIMARY KEY NOT NULL,
            COMIC_ID INTEGER NOT NULL,
            NAME TEXT NOT NULL,
            URL TEXT NOT NULL
            )
        ''' % (TABLE_CHAPTERS)
        conn.execute(sql)
        
        sql = '''
        CREATE TABE IF NOTE EXISTS %s
            (ID INTEGER PRIMARY KEY NOT NULL,
            COMIC_ID INTEGER NOT NULL,
            CHAPTER_ID INTEGER NOT NULL,
            IMAGE_URL TEXT NOT NULL
            )
        ''' % (TABLE_CHAPTER_IMAGES)
        conn.execute(sql)
        
        sql = '''
        CREATE TABLE IF NOT EXISTS %s
            (ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NAME TEXT NOT NULL,
            PASSWORD TEXT NOT NULL
            )
        ''' % (TABLE_USERS)
        conn.execute(sql)
        
        sql = '''
        CREATE TABLE IF NOT EXISTS %s
            (ID INTEGER PRIMARY KEY AUTOINCREMENT,
            USER_ID INTEGER NOT NULL,
            COMIC_ID INTEGER NOT NULL
            )
        ''' % (TABLE_FAVOURITE_COMICS)
        conn.execute(sql)
        
        conn.commit()
    except:
        print ('fail to create table')
    conn.close()
    
def insert_comic(id, name, url, author, img):
    conn = sqlite3.connect(DB)
    # INSERT OR REPLACE
    # INSERT OR IGNORE
    sql = '''
    INSERT OR REPLACE INTO %s
    (ID, NAME, URL, AUTHOR, IMG)
    VALUES (%d, "%s", "%s", "%s", "%s")
    ''' % (TABLE_COMICS, id, name, url, author, img)
    conn.execute(sql)
    conn.commit()
    conn.close()

def insert_latest_chapter(id, name, url):
    conn = sqlite3.connect(DB)
    sql = '''
    INSERT OR REPLACE INTO %s 
    (ID, NAME, URL) 
    VALUES (%d, "%s", "%s")
    ''' % (TABLE_LATEST_CHAPTERS, id, name, url)
    conn.execute(sql)
    conn.commit()
    conn.close()
    
def get_latest_comic_id():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    sql = '''
    SELECT max(ID) FROM %s
    ''' % (TABLE_COMICS)
    cursor = c.execute(sql)
    id = cursor.fetchone()[0]
    conn.close()
    return id

def select_all():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    sql = '''
    SELECT ID, NAME, URL from %s
    ''' % (TABLE_COMICS)
    cursor = c.execute(sql)
    for row in cursor:
        print('ID = ', row[0])
        print('NAME = ', row[1])
        print('URL = ', row[2])
    conn.close()

#create_tables()
