"""

"""
from __future__ import with_statement
import sqlite3
from flask import Flask, request, session, redirect, url_for,\
    render_template, flash
from werkzeug.security import check_password_hash

from utils.snippets import timesince, login_required
from utils.db  import *

app = Flask(__name__)
app.config.from_pyfile('app.cfg')
app.jinja_env.filters['timesince'] = timesince
app.jinja_env.filters['get_user'] = get_user
app.jinja_env.filters['get_comment_count'] = get_comment_count
app.jinja_env.filters['get_blog_comments'] = get_blog_comments

def connect_db():
    """Returns a new connection to the database."""
    return sqlite3.connect(app.config['DATABASE'])


@app.before_request
def before_request():
    """Make sure we are connected to the database each request."""
    g.db = connect_db()
    g.logged_in = bool(session.get('logged_in'))


@app.teardown_request
def teardown_request(exception):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/')
def show_entries():
    """ Retrieve blog entries from the database """
    cur = g.db.execute('select title, description_enc, date_created, last_modified,'
                       ' tags, user_id, id from blog order by id desc')
    posts = [dict(title=row[0], desc=row[1], date_created=row[2],
        last_modified=row[3], tags=row[4], uid=row[5], id=row[6]) \
             for row in cur.fetchall()]
    return render_template('show_entries.html', posts=posts)

@app.route('/post/<id>')
def view_post(id):
    """ Retrieve a particular blog post from the database """
    return render_template('post.html', post=get_blog_post(id))


@app.route('/add', methods=['POST'])
@login_required
def add_entry():
    """ Adds a  blog post to the database """
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        desc_enc = request.form.get('desc_enc')
        tags = request.form.get('tags')

        g.db.execute('insert into blog (title, description, description_enc, date_created, tags, user_id) '
                     'values (?, ?, ?, ?, ?, ?)',
        [title,description,desc_enc,datetime.now(),tags,session.get('u_id')])
        g.db.commit()
        flash('New entry was successfully posted')

    return redirect(url_for('show_entries'))


@app.route('/comment', methods=['POST'])
@login_required
def comment():
    """ adds a blog comment """
    if request.method == 'POST':
        text = request.form.get('comment')
        uid = session.get('u_id')
        blog_id = request.form.get('blog_id')
        create_blog_comment(text,blog_id,uid)
        flash('Your comment has been successfully added')
    return redirect(url_for('show_entries'))


@app.route('/delete/<id>')
@login_required
def delete(id):
    """ delete a blog post"""
    g.db.execute('delete from comments where blog_id = ?', [id])
    g.db.execute('delete from blog where id = ?', [id])
    g.db.commit()
    flash('Blog post successfully deleted')
    return redirect(url_for('show_entries'))


@app.route('/update', methods=['POST'])
@app.route('/update/<id>', methods=['GET'])
@login_required
def update(id=0):
    """ update blog post """
    if request.method == 'GET':
        return render_template('update.html', post=get_blog_post(id))

    elif request.method == 'POST' :
        title = request.form.get('title')
        description = request.form.get('description')
        desc_enc = request.form.get('desc_enc')
        tags = request.form.get('tags')

        g.db.execute('update blog set title=?, description=?, description_enc=?,\
                      tags=?, last_modified=? where user_id=?',
            [title, description, desc_enc, tags,datetime.now(), session.get('u_id')])
        g.db.commit()
        flash('Entry successfully updated')
        return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Authenticate user credentials """
    error = None
    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        cur = g.db.execute('select id, password from users where username = ?',[username])
        row = cur.fetchone()

        if row and check_password_hash(row[1],password) :
            session['logged_in'] = True
            session['u_id'] = row[0]
            flash('You were logged in')
            return redirect(url_for('show_entries'))
        else :
            error = 'Invalid username or password'

    return render_template('login.html', error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """ Register/Create a new user account """
    error = None
    if request.method == 'POST':
        uname =request.form.get('username')
        firstname  =request.form.get('firstname')
        lastname =request.form.get('lastname')
        passwd = request.form.get('password')
        spasswd =  request.form.get('spassword')

        if not uname.strip():
            error = "Username field cannot be empty"
        elif not firstname.strip():
            error = "First name field cannot be empty"
        elif not lastname.strip():
            error = "Last name field cannot be empty"
        elif user_exists(uname):
            error = "Username is already in use. Choose another"
        elif not (passwd or spasswd):
            error = 'Password field cannot be empty'
        elif spasswd != passwd:
            error = 'Passwords do not match'
        else :
            create_user(uname,firstname,lastname,passwd)
            flash("Registration was successful")
            return redirect(url_for("login"))

    return render_template('register.html',error=error)

@app.route('/logout')
def logout():
    """ Remove user session and logs a user out """
    session.pop('logged_in', None)
    session.pop('u_id', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    app.run()
