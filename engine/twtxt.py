import sys
import urllib.request
import textwrap
from datetime import datetime, timedelta, timezone

from dateutil.parser import parse as parsedate

FOLLOWING = [
    'https://hecanjog.com/twtxt.txt', # sanity check
    'https://wiki.xxiivv.com/twtxt.txt', 
    'https://timmorgan.org/twtxt.txt',
    'https://txt.eli.li/twtxt/twtxt.txt',
    'https://feg-ffb.de/twtxt.txt',
    'https://www.frogorbits.com/twtxt.txt',
    'https://fundor333.com/twtxt.txt',
    'https://hjertnes.social/twtxt.txt',
    'https://john.colagioia.net/twtxt.txt',
    'http://ctrl-c.club/~jlj/tw.txt',
    'https://enotty.dk/twtxt.txt',
    'https://enotty.dk/kasdk.txt',
    'https://koehr.in/twtxt.txt',
    'http://lahvak.github.io/twtxt/twtxt.txt',
    'https://tilde.town/~lucidiot/twtxt.txt',
    'https://mdosch.de/twtxt.txt',
    'https://tilde.club/~melyanna/twtxt.txt',
    'https://pbat.ch/twtxt.txt',
]

OLD = 30
HIDE = 7

def convertdate(date):
    date = parsedate(date)
    if not date.tzinfo:
        date = date.replace(tzinfo=timezone.utc)
    return date

def getfeeds():
    now = datetime.now(timezone.utc)
    old = now - timedelta(days=OLD)

    feeds = []
    for url in FOLLOWING:
        try:
            with urllib.request.urlopen(url) as conn:
                updated = convertdate(conn.headers['last-modified'])
                if updated > old:
                    feeds += [(url, conn.read().decode('utf-8'))]
                    print(url)
                else:
                    print('  OLD::', url)
        except Exception as e:
            print('  ERR::', e, url)
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
            #print(post, e)
    return sorted(posts, key=lambda x: x['date'])

def getlast(feeds, limit=5):
    posts = []
    for url, feed in feeds:
        feedposts = parsefeed(url, feed)
        posts += feedposts[-limit:]
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
        feeds = getfeeds()
        posts = getlast(feeds, 5)
        printposts(posts)

