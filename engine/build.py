from datetime import datetime
from pathlib import Path

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
                    else:
                        self.headers[k] = v.strip()
                else:
                    # Markdown body
                    self.markdown += line

        self.html = pypandoc.convert_text(self.markdown, 'html5', format='md')

        for k in self.headers.keys():
            setattr(self, k.lower(), self.headers[k])

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

def build_posts():
    header, footer = load_template()

    # Listening Journal
    listening = []
    for p in Path('./posts').glob('*.md'):
        post = Post(p)
        if 'listening' in post.tags:
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
    build_pages()
    build_posts()
    print('done!')
