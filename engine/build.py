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
                        try:
                            self.headers[k] = datetime.strptime(v.strip(), '%Y-%m-%d %H:%M')
                        except ValueError:
                            self.headers[k] = datetime.strptime(v.strip(), '%Y-%m-%d')

                        self.datestring = v.strip()
                        self.year = self.headers[k].year
                        self.month = self.headers[k].month
                        self.day = self.headers[k].day

                    elif k == 'Title':
                        self.headers[k] = pypandoc.convert_text(v, 'html5', format='md').replace('<p>', '').replace('</p>', '')

                    else:
                        self.headers[k] = v.strip()
                else:
                    # Markdown body
                    self.markdown += line

        self.html = pypandoc.convert_text(self.markdown, 'html5', format='md')
        self.gmi = pypandoc.convert_text(self.markdown, 'plain', format='md', extra_args=['--lua-filter=/home/hecanjog/sites/hecanjog.com/vendor/gemini-pandoc-lua-filter/gemini.lua'])

        if 'Status' not in self.headers:
            self.headers['Status'] = 'public'

        for k in self.headers.keys():
            setattr(self, k.lower(), self.headers[k])

        slug = pypandoc.convert_text(self.title, 'plain', format='html')
        slug = unicodedata.normalize('NFKD', slug).encode('ascii', 'ignore').decode('ascii')
        slug = re.sub('[-\s]+', '-', re.sub('[^\w\s-]', '', slug).strip().lower())
        self.slug = '%04d%02d%02d-%s' % (self.year, self.month, self.day, slug)


def get_wrappers(wtype):
    now = datetime.now()
    today = '%s-%s-%s' % (now.year, now.month, now.day)

    if wtype == 'html':
        with open('templates/header.html', 'r', encoding='utf-8') as f:
            html_header = f.read()
            html_header = html_header % today
        with open('templates/footer.html', 'r', encoding='utf-8') as f:
            html_footer = f.read()
        return html_header, html_footer

    if wtype == 'gmi':
        with open('templates/header.gmi', 'r', encoding='utf-8') as f:
            gmi_header = f.read()
        with open('templates/footer.gmi', 'r', encoding='utf-8') as f:
            gmi_footer = f.read()
        return gmi_header, gmi_footer

    return None, None

def build_pages():
    html_header, html_footer = get_wrappers('html')
    gmi_header, gmi_footer = get_wrappers('gmi')

    for source in Path('./pages').glob('*.md'):
        # Create HTML page
        dest = 'static/%s.html' % source.stem
        print('Building HTML: %s to %s' % (source, dest))
        with open(dest, 'w', encoding='utf-8') as html:
            converted = pypandoc.convert_file(str(source), 'html5', format='md')
            html.write(html_header + converted + html_footer)

        # Create GMI page
        dest = 'static/gemini/%s.gmi' % source.stem
        print('Building GMI: %s to %s' % (source, dest))
        with open(dest, 'w', encoding='utf-8') as gmi:
            converted = pypandoc.convert_file(str(source), 'plain', format='md', extra_args=['--lua-filter=/home/hecanjog/sites/hecanjog.com/vendor/gemini-pandoc-lua-filter/gemini.lua'])
            converted = converted.replace('.html', '.gmi')
            gmi.write(gmi_header + converted + gmi_footer)


def build_posts(name):
    # Get wrappers
    html_header, html_footer = get_wrappers('html')
    gmi_header, gmi_footer = get_wrappers('gmi')

    # Collate posts
    posts = []
    for p in Path('./posts/%s/' % name).glob('*.md'):
        post = Post(p)
        posts += [ post ]
    posts.sort(key=lambda p: p.date, reverse=True)    


    ########
    # HTML #
    ########

    # Get index listing (home) template
    with open('templates/%s.html' % name, 'r', encoding='utf-8') as f:
        postshome = f.read()

    # Create HTML index listing page
    with open('static/%s.html' % name, 'w', encoding='utf-8') as html:
        html.write(html_header)
        postslist = '<ul class="%slist list">' % name
        for p in posts:
            if p.status.lower() != 'draft':
                postslist += '<li><h2><a href="/%s/%s.html">%s</a></h2><p class="byline">Posted on %s</p></li>' % (name, p.slug, p.title, p.datestring)
        postslist += '</ul>'
        postshome = postshome.replace('$%sLIST' % name.upper(), postslist)
        html.write(postshome)
        html.write(html_footer)

    # Create standalone HTML pages
    for p in posts:
        _render_html_post(name, p)

    #######
    # GMI #
    #######

    # Get index listing (home) template
    with open('templates/%s.gmi' % name, 'r', encoding='utf-8') as f:
        postshome = f.read()

    # Create HTML index listing page
    with open('static/gemini/%s.gmi' % name, 'w', encoding='utf-8') as gmi:
        gmi.write(gmi_header)
        postslist = ''
        for p in posts:
            if p.status.lower() != 'draft':
                postslist += '=> /%s/%s.gmi %s\nPosted on %s\n\n' % (name, p.slug, p.title, p.datestring)
        postshome = postshome.replace('$%sLIST' % name.upper(), postslist)
        gmi.write(postshome)
        gmi.write(gmi_footer)

    # Create standalone GMI pages
    for p in posts:
        _render_gmi_post(name, p)


def _render_html_post(name, p):
    html_header, html_footer = get_wrappers('html')

    if name == 'releases':
        with open('templates/release.html', 'r', encoding='utf-8') as f:
            release_template = f.read()

        with open('static/%s/%s.html' % (name, p.slug), 'w', encoding='utf-8') as html:
            print('%s: %s - %s' % (name, p.title, p.datestring))
            html.write(html_header)
            release_html = release_template.replace('$TITLE', p.title)
            release_html = release_html.replace('$IMAGE', p.image)
            release_html = release_html.replace('$CONTENT', p.html)
            release_html = release_html.replace('$DATETIME', p.datestring)
            release_html = release_html.replace('$BANDCAMP', p.bandcamp)
            html.write(release_html)
            html.write(html_footer)


    else:
        with open('static/%s/%s.html' % (name, p.slug), 'w', encoding='utf-8') as postspagehtml:
            print('%s: %s - %s' % (name, p.title, p.datestring))
            postspagehtml.write(html_header)
            postspagehtml.write('<div class="%s post">' % name)
            postspagehtml.write('<h2>%s</h2>' % p.title)
            postspagehtml.write('<p class="byline">Posted on %s</p>' % p.datestring)
            postspagehtml.write('<hr/>')
            p.html = p.html.replace('/images/', '/img/')
            p.html = p.html.replace('{static}', '')
            postspagehtml.write(p.html)
            postspagehtml.write('</div>')
            postspagehtml.write(html_footer)

def _render_gmi_post(name, p):
    gmi_header, gmi_footer = get_wrappers('gmi')
    with open('static/gemini/%s/%s.gmi' % (name, p.slug), 'w', encoding='utf-8') as postspagegmi:
        print('%s: %s - %s' % (name, p.title, p.datestring))
        postspagegmi.write(gmi_header)
        postspagegmi.write('## %s\n' % p.title)
        postspagegmi.write('Posted on %s\n\n' % p.datestring)
        p.gmi = p.gmi.replace('/images/', '/img/')
        p.gmi = p.gmi.replace('{static}', '')
        p.gmi = p.gmi.replace('html', 'gmi')
        postspagegmi.write(p.gmi)
        postspagegmi.write(gmi_footer)



if __name__ == '__main__':
    if sys.argv[1] == 'blog':
        build_posts('blog')

    if sys.argv[1] == 'listening':
        build_posts('listening')

    if sys.argv[1] == 'releases':
        build_posts('releases')

    if sys.argv[1] == 'pages':
        build_pages()

    print('done!')
