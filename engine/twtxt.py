import sys
import urllib.request
import textwrap

FOLLOWING = [
    'https://hecanjog.com/twtxt.txt', # sanity check
    'https://wiki.xxiivv.com/twtxt.txt', 
    'https://timmorgan.org/twtxt.txt',
    'https://abliss.keybase.pub/twtxt.txt#7a778276dd852edc65217e759cba637a28b4426b',
    'https://akraut.keybase.pub/twtxt.txt',
    'https://dev.exherbo.org/~alip/twtxt.txt',
    'http://autoalk.tk/twtxt/autoalk.txt',
    'https://benaiah.me/twtxt.txt',
    'https://buckket.org/twtxt.txt',
    'http://pestilenz.org/~ckeen/twtxt.txt',
    'http://clementd-files.cellar.services.clever-cloud.com/twtxt.txt',
    'https://davebucklin.com/twtxt.txt',
    'https://yourtilde.com/~deepend/twtxt.txt',
    'http://edsu.github.io/twtxt/twtxt.txt',
    'https://txt.eli.li/twtxt/twtxt.txt',
    'http://escowles.github.io/tw.txt',
    'https://feg-ffb.de/twtxt.txt',
    'https://www.frogorbits.com/twtxt.txt',
    'https://fundor333.com/twtxt.txt',
    'https://gbmor.dev/twtxt.txt',
    'https://tilde.pt/~gil/twtxt.txt',
    'https://hjertnes.social/twtxt.txt',
    'https://jb55.com/twtxt.txt',
    'https://john.colagioia.net/twtxt.txt',
    'http://ctrl-c.club/~jlj/tw.txt',
    'https://johanbove.info/twtxt.txt',
    'https://enotty.dk/twtxt.txt',
    'https://enotty.dk/kasdk.txt',
    'https://kernel-pancake.nl/twtxt.txt',
    'https://koehr.in/twtxt.txt',
    'http://lahvak.github.io/twtxt/twtxt.txt',
    'https://www.gkbrk.com/twtxt.txt',
    'https://tilde.town/~lucidiot/twtxt.txt',
    'https://tilde.pt/~marado/twtxt.txt',
    'https://domgoergen.com/twtxt/mdom.txt',
    'https://mdosch.de/twtxt.txt',
    'https://tilde.club/~melyanna/twtxt.txt',
    'https://tilde.town/~mr_woggle/twtxt.txt',
    'http://nblade.sdf.org/twtxt/twtxt.txt',
    'https://karl.theharrisclan.net/twtxt.txt',
    'https://pbat.ch/twtxt.txt',
    'http://pelmel.org/twtxt.txt',
    'https://prologic.github.io/twtxt.txt',
    'https://lublin.se/twtxt.txt',
    'http://twtxt.xyz/user/8c2b4bbfa328944ba.txt',
    'http://ruebot.github.io/twtxt/twtxt.txt',
    'https://codevoid.de/tw.txt',
    'https://sixbitproxywax.com/twtxt.txt',
    'http://scott.vranesh-fallin.com/twtxt.txt',
    'https://twtxt.lpho.de/twtxt.txt',
    'https://grex.org/~tfurrows/twtxt.txt',
    'https://tilde.team/~tildebeast/twtxt/twtxt.txt',
    'https://twtxt.rosaelefanten.org/',
    'https://lublin.se/twet.txt',
    'https://buckket.org/twtxt_news.txt',
    'https://vinc.cc/twtxt.txt',
    'https://tilde.town/~von/twtxt.txt',
    'https://xandkar.net/twtxt.txt',
]

def getfeeds():
    feeds = []
    for url in FOLLOWING:
        try:
            with urllib.request.urlopen(url) as f:
                feeds += [(url, f.read().decode('utf-8'))]
        except Exception as e:
            print(e, url)
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

