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
        self.permalink = '/posts/%s.html' % (self.slug)


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

def build_blog_posts():
    header, footer = load_template()

    with open('templates/blog.html', 'r', encoding='utf-8') as f:
        bloghome = f.read()

    # Blog
    blog = []
    for p in Path('./posts/blog/').glob('*.md'):
        post = Post(p)
        if post.status.lower() != 'draft':
            blog += [ post ]

    blog.sort(key=lambda p: p.date, reverse=True)    
    with open('static/blog.html', 'w', encoding='utf-8') as html:
        html.write(header)

        bloglist = '<ul class="bloglist">'
        for p in blog:
            bloglist += '<li><h2><a href="%s">%s</a></h2><p class="byline">Posted on %s</p></li>' % (p.permalink, p.title, p.datestring)
            with open('static/posts/%s.html' % p.slug, 'w', encoding='utf-8') as blogpagehtml:
                print('Blog: %s - %s' % (p.title, p.datestring))
                blogpagehtml.write(header)
                blogpagehtml.write('<div class="blog post">')
                blogpagehtml.write('<h2>%s</h2>' % p.title)
                blogpagehtml.write('<p class="byline">Posted on %s</p>' % p.datestring)
                blogpagehtml.write('<hr/>')
                p.html = p.html.replace('/images/', 'img/')
                blogpagehtml.write(p.html)
                blogpagehtml.write('</div>')
                blogpagehtml.write(footer)
        bloglist += '</ul>'

        bloghome = bloghome.replace('$BLOGLIST', bloglist)
        html.write(bloghome)

        html.write(footer)

def build_listening_posts():
    header, footer = load_template()

    # Listening Journal
    listening = []
    for p in Path('./posts/listening/').glob('*.md'):
        post = Post(p)
        if post.status.lower() != 'draft':
            listening += [ post ]

    listening.sort(key=lambda p: p.date, reverse=True)    
    with open('static/listening.html', 'w', encoding='utf-8') as html:
        html.write(header)
        html.write('<h2>Listening Journal</h2>')
        for p in listening:
            print('Listening: %s - %s' % (p.title, p.datestring))
            html.write('<hr/>')
            html.write('<div class="listening post">')
            html.write('<h3>%s</h3>' % p.title)
            p.html = p.html.replace('/images/', 'img/')
            html.write(p.html)
            html.write('</div>')

        html.write(footer)


if __name__ == '__main__':
    if sys.argv[1] == 'blog':
        build_blog_posts()

    if sys.argv[1] == 'listening':
        build_listening_posts()

    if sys.argv[1] == 'pages':
        build_pages()

    print('done!')
