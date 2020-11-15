from datetime import datetime
from pathlib import Path
import sys
import re
import unicodedata

import pypandoc

class Post:
    def __init__(self, path):
        self.path = Path(path)
        self.headers = {}
        self.markdown = ''

        br = 0
        with open(self.path, 'r', encoding='utf-8') as f:
            for line in f:
                if line == '\n':
                    br += 1

                if br < 1:
                    # Metadata
                    k, v = tuple(line.split(': '))
                    if k == 'Tags':
                        self.headers[k] = v.strip().split(' ')
                    elif k == 'Date':
                        self.headers[k] = datetime.strptime(v.strip(), '%Y-%m-%d %H:%M')
                        self.datestring = v.strip()
                        self.year = self.headers[k].year
                        self.month = self.headers[k].month
                        self.day = self.headers[k].day
                    else:
                        self.headers[k] = v.strip()
                else:
                    # Markdown body
                    self.markdown += line

        self.html = pypandoc.convert_text(self.markdown, 'html5', format='md')

        if 'Status' not in self.headers:
            self.headers['Status'] = 'public'

        for k in self.headers.keys():
            setattr(self, k.lower(), self.headers[k])

        slug = unicodedata.normalize('NFKD', self.title).encode('ascii', 'ignore').decode('ascii')
        slug = re.sub('[-\s]+', '-', re.sub('[^\w\s-]', '', slug).strip().lower())
        self.slug = '%04d%02d%02d-%s' % (self.year, self.month, self.day, slug)


def load_template():
    now = datetime.now()
    today = '%s-%s-%s' % (now.year, now.month, now.day)

    with open('templates/header.html', 'r', encoding='utf-8') as f:
        header = f.read()
        header = header % today

    with open('templates/footer.html', 'r', encoding='utf-8') as f:
        footer = f.read()

    return header, footer

def build_pages():
    header, footer = load_template()

    for source in Path('./pages').glob('*.md'):
        dest = 'static/%s.html' % source.stem
        print('Building %s to %s' % (source, dest))
        with open(dest, 'w', encoding='utf-8') as html:
            converted = pypandoc.convert_file(str(source), 'html5', format='md')
            html.write(header + converted + footer)

def build_posts(name):
    header, footer = load_template()

    with open('templates/%s.html' % name, 'r', encoding='utf-8') as f:
        postshome = f.read()

    # Blog
    posts = []
    for p in Path('./posts/%s/' % name).glob('*.md'):
        post = Post(p)
        if post.status.lower() != 'draft':
            posts += [ post ]

    posts.sort(key=lambda p: p.date, reverse=True)    
    with open('static/%s.html' % name, 'w', encoding='utf-8') as html:
        html.write(header)

        postslist = '<ul class="%slist">' % name
        for p in posts:
            postslist += '<li><h2><a href="/%s/%s.html">%s</a></h2><p class="byline">Posted on %s</p></li>' % (name, p.slug, p.title, p.datestring)
            with open('static/%s/%s.html' % (name, p.slug), 'w', encoding='utf-8') as postspagehtml:
                print('%s: %s - %s' % (name, p.title, p.datestring))
                postspagehtml.write(header)
                postspagehtml.write('<div class="%s post">' % name)
                postspagehtml.write('<h2>%s</h2>' % p.title)
                postspagehtml.write('<p class="byline">Posted on %s</p>' % p.datestring)
                postspagehtml.write('<hr/>')
                p.html = p.html.replace('/images/', '/img/')
                p.html = p.html.replace('{static}', '')
                postspagehtml.write(p.html)
                postspagehtml.write('</div>')
                postspagehtml.write(footer)
        postslist += '</ul>'

        postshome = postshome.replace('$%sLIST' % name.upper(), postslist)
        html.write(postshome)
        html.write(footer)


if __name__ == '__main__':
    if sys.argv[1] == 'blog':
        build_posts('blog')

    if sys.argv[1] == 'listening':
        build_posts('listening')

    if sys.argv[1] == 'pages':
        build_pages()

    print('done!')
