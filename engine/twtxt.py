import sys
import urllib.request
import textwrap

FOLLOWING = [
    'https://hecanjog.com/twtxt.txt', # sanity check
    'https://pbat.ch/twtxt.txt', 
    'https://wiki.xxiivv.com/twtxt.txt', 
    'https://tilde.town/~lucidiot/twtxt.txt',
]

def getfeeds():
    feeds = []
    for url in FOLLOWING:
        with urllib.request.urlopen(url) as f:
            feeds += [(url, f.read().decode('utf-8'))]
    return feeds

def parsefeed(url, feed):
    posts = []
    for post in feed.splitlines():
        if len(post) == 0 or  post[0] == '#' or post[0] == '\n' or post.strip() == '':
            continue
        try:
            date, content = tuple(post.split('\t'))
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

