import sys
import multiprocessing as mp
import urllib.request
import textwrap
from datetime import datetime, timedelta, timezone

from dateutil.parser import parse as parsedate

POSTLIMIT = 5
POSTLIMIT = None

FOLLOWING = [
    'https://hecanjog.com/twtxt.txt', # sanity check
    'https://timmorgan.org/twtxt.txt',
    'https://txt.eli.li/twtxt/twtxt.txt',
    'https://feg-ffb.de/twtxt.txt',
    'https://www.frogorbits.com/twtxt.txt',
    'https://fundor333.com/twtxt.txt',
    'https://hjertnes.social/twtxt.txt',
    'https://john.colagioia.net/twtxt.txt',
    'http://ctrl-c.club/~jlj/tw.txt',
    'https://koehr.in/twtxt.txt',
    'http://lahvak.github.io/twtxt/twtxt.txt',
    'https://tilde.town/~lucidiot/twtxt.txt',
    'https://mdosch.de/twtxt.txt',
    'https://tilde.club/~melyanna/twtxt.txt',
    'https://pbat.ch/twtxt.txt',
    'https://xandkar.net/twtxt.txt',
]

OLD = 90
HIDE = 7

def convertdate(date):
    date = parsedate(date)
    if not date.tzinfo:
        date = date.replace(tzinfo=timezone.utc)
    return date

def getfeeds():
    return feeds

def parsefeed(url, feed):
    now = datetime.now(timezone.utc)
    old = now - timedelta(days=HIDE)

    posts = []
    for post in feed.splitlines():
        if len(post) == 0 or  post[0] == '#' or post[0] == '\n' or post.strip() == '':
            continue
        try:
            date, content = tuple(post.split('\t'))
            date = convertdate(date)
            if date > old:
                posts += [{'url': url, 'date': date, 'content': content}]
        except ValueError as e:
            pass
    return sorted(posts, key=lambda x: x['date'])

def _parsefeed(url):
    now = datetime.now(timezone.utc)
    old = now - timedelta(days=OLD)

    try:
        with urllib.request.urlopen(url) as conn:
            updated = convertdate(conn.headers['last-modified'])
            if updated > old:
                feed = conn.read().decode('utf-8')
                print(url)
                posts = parsefeed(url, feed)
                if POSTLIMIT is not None:
                    posts = posts[-POSTLIMIT:]
                return posts

            else:
                print('  NO UPDATES IN %s DAYS::' % OLD, url)
                return None

    except Exception as e:
        print('  ERR::', e, url)
        return None


def getlast():
    posts = []
    processes = mp.cpu_count()
    with mp.Pool(processes=processes) as process_pool:
        for result in [ process_pool.apply_async(_parsefeed, (FOLLOWING[i % len(FOLLOWING)],)) for i in range(len(FOLLOWING)) ]:
            r = result.get()
            if r is not None:
                posts += r

    return sorted(posts, key=lambda x: x['date'])

def printposts(posts):
    print()
    print(' ::::::::::::::::')
    print(':: LATEST POSTS ::')
    print(' ::::::::::::::::')
    print()
    for post in posts:
        content = '\n'.join(textwrap.wrap(post['content'], 80))
        content = textwrap.indent(content, '  | ')
        print(post['url'])
        print(post['date'])
        print(content)
        print()

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        exit()

    if sys.argv[1] == '--feed':
        posts = getlast()
        printposts(posts)

