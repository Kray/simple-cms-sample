# (C) Konsta Kokkinen 2013
# Do whatever you want with this...


import decorator
import bottle
from bottle_sqlite import SQLitePlugin
from beaker.middleware import SessionMiddleware
import markdown
import sqlite3

class Config:
    def get(db, key):
        try:
            return db.execute('SELECT value FROM config WHERE key = ?', (key,)).fetchone()[0]
        except:
            return ''

    def set(db, key, value):
        db.execute('INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)', (key, value))
        db.commit()


db = sqlite3.connect('db.db')
db.execute('CREATE TABLE IF NOT EXISTS pages (url UNIQUE, title, content)')
db.execute('CREATE TABLE IF NOT EXISTS layout (part, key, value)')
db.execute('CREATE TABLE IF NOT EXISTS config (key UNIQUE, value)')
db.commit()

# Set some defaults on first run
if Config.get(db, 'installed') == '':
    db.execute('INSERT OR IGNORE INTO pages VALUES ("", "Front page", "This is the default front page")')
    db.execute('INSERT INTO layout VALUES ("navbar", "/", "Front page")')
    Config.set(db, 'title', 'CMS')
    Config.set(db, 'installed', '1')

app = bottle.app()

app.install(SQLitePlugin(dbfile='db.db'))


session_opts = {
    'session.type': 'file',
    'session.data_dir': './data',
    'session.auto': True
}
app = SessionMiddleware(app, session_opts)


# Decorator enforcing admin status
@decorator.decorator
def requireadmin(func, *args, **kwargs):
    # TODO: real authentication stuff...
    session = bottle.request.environ.get('beaker.session')
    if session.get('user') != 'admin':
        return bottle.redirect('/_/login')
    return func(*args, **kwargs)


# Layout helper
class Layout:
    def __init__(self):
        self.load()

    def load(self):
        db = sqlite3.connect('db.db')

        self.title = Config.get(db, 'title')

        self.navbar = ''
        for row in db.execute('SELECT key, value FROM layout WHERE part = "navbar"').fetchall():
            if row[0] and len(row[0]) > 0:
                if row[0].startswith('/') or row[0].startswith('http://') or row[0].startswith('https://'):
                    self.navbar += '<a href="' + bottle.html_escape(row[0]) + '">'
                    if row[1] and len(row[1]) > 0:
                        self.navbar += bottle.html_escape(row[1])
                    elif row[0].startswith('/'):
                        try:
                            self.navbar += db.execute('SELECT title FROM pages WHERE url = ?', (row[0][1:],)).fetchone()[0]
                        except:
                            self.navbar += bottle.html_escape(row[0])
                    else:
                        self.navbar += bottle.html_escape(row[0])
                    self.navbar += '</a>'
            elif row[1]:
                self.navbar += '<span>' + bottle.html_escape(row[1]) + '</span>'
        db.close()

layout = Layout()

@bottle.route('/static/<filename>')
def serve_static(filename):
    return bottle.static_file(filename, root='./static/')

@bottle.route('/')
def index(db):
    return page(db, '')

@bottle.route('/<url>')
def page(db, url):
    page = db.execute('SELECT title, content FROM pages WHERE url = ?', (url,)).fetchone()
    if not page:
        return bottle.HTTPError(404, "Page not found")
    title = page[0]
    content = markdown.markdown(page[1], safe_mode='escape', extensions=['headerid(level=3)'])
    return bottle.template('page', layout=layout, title=title, content=content)



@bottle.get('/_/login')
def ctrl_login_form(last_failed=False):
    return bottle.template('ctrl_login', layout=layout, last_failed=last_failed)
@bottle.post('/_/login')
def ctrl_login_submit():
    forms = bottle.request.forms.decode()
    user = forms.get('user')
    password = forms.get('password')

    # TODO: real authentication stuff...
    if user != 'admin' or password != 'password':
        return ctrl_login_form(last_failed=True)

    session = bottle.request.environ.get('beaker.session')
    session['user'] = 'admin'
    session.save()

    bottle.redirect('/_/')


@bottle.route('/_/')
@requireadmin
def ctrl_index():
    bottle.redirect('/_/pages')


@bottle.route('/_/pages')
@bottle.route('/_/pages/')
@requireadmin
def ctrl_pages():
    pages = []

    rows = db.execute('SELECT url, title FROM pages').fetchall()
    for row in rows:
        pages.append({ 'url': row[0], 'title': row[1] })
    return bottle.template('ctrl_pages', layout=layout, pages=pages)


@bottle.get('/_/config')
@bottle.get('/_/config/')
@requireadmin
def ctrl_layout():
    config = db.execute('SELECT key, value FROM config')
    return bottle.template('ctrl_config', layout=layout, config=config)

@bottle.post('/_/config/')
@requireadmin
def ctrl_layout_edit(db):
    forms = bottle.request.forms.decode()
    key = forms.get('key')
    value = forms.get('value')
    db.execute('INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)', (key, value))
    db.commit()
    layout.load()
    bottle.redirect('/_/config')


@bottle.get('/_/layout')
@bottle.get('/_/layout/')
@requireadmin
def ctrl_layout():
    navbar = db.execute('SELECT rowid, key, value FROM layout WHERE part = "navbar"')
    return bottle.template('ctrl_layout', layout=layout, navbar=navbar)


@bottle.get('/_/layout/new/<part>')
@requireadmin
def ctrl_layout_new(db, part):
    db.execute('INSERT INTO layout (part) VALUES (?)', (part,))
    db.commit()
    layout.load()
    bottle.redirect('/_/layout')


@bottle.post('/_/layout/edit/<id>')
@requireadmin
def ctrl_layout_edit(db, id):
    forms = bottle.request.forms.decode()
    key = forms.get('key')
    value = forms.get('value')
    db.execute('UPDATE layout SET key = ?, value = ? WHERE rowid = ?', (key, value, id))
    db.commit()
    layout.load()
    bottle.redirect('/_/layout')


@bottle.get('/_/new')
@requireadmin
def ctrl_new_form():
    return bottle.template('ctrl_edit', layout=layout)

@bottle.post('/_/new')
@requireadmin
def ctrl_new_submit(db):
    forms = bottle.request.forms.decode()
    url = forms.get('page_url')
    title = forms.get('page_title')
    content = forms.get('page_content')
    db.execute('INSERT INTO pages (url, title, content) VALUES(?,?,?)', (url, title, content))
    db.commit()
    bottle.redirect('/' + str(url))


@bottle.get('/_/edit/')
@bottle.get('/_/edit/<url>')
@requireadmin
def ctrl_edit_form(db, url=''):
    page = db.execute('SELECT title, content FROM pages WHERE url = ?', (url,)).fetchone()
    if not page:
        return bottle.redirect('/_/new')
    title = page[0]
    content = page[1]

    return bottle.template('ctrl_edit', layout=layout, url=url, title=title, content=content)

@bottle.post('/_/edit/')
@bottle.post('/_/edit/<url>')
@requireadmin
def ctrl_edit_submit(db, url=''):
    forms = bottle.request.forms.decode()
    title = forms.get('page_title')
    content = forms.get('page_content')
    db.execute('UPDATE pages SET title = ?, content = ? WHERE url = ?', (title, content, url))
    return bottle.redirect('/' + url)


bottle.run(app=app, host='0.0.0.0', port=3000, debug=True)

