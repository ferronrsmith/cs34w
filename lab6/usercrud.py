from flask import Flask, request, g,render_template, \
           url_for, redirect, flash, send_from_directory, session
import sqlite3, os
import crypt

SECRET_KEY = "the global object 'g' needs this"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config.from_object(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# database method, which is triggered
# before each request
def connect_db():
    return sqlite3.connect('./users.db')

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route('/create', methods=['POST'])
def create():
    content_length = request.headers['Content-Length']

    if int(content_length) > 102450:
        file = request.files['photo']
        flash(file.filename + ' is too large')
        return redirect(url_for('read'))
    else :
        fullname = request.form['fullname']
        username = request.form['username']
        file = request.files['photo']
        if file and allowed_file(file.filename):
            photo = file.filename
            file.save(os.path.join('uploads', photo))
            g.db.execute('insert into users (fullname, username, photo) \
                             values (?, ?, ?)',
                                         [fullname, username, photo])
            g.db.commit()
            flash('New entry was successfully posted')
            return redirect(url_for('read'))
        else:
            return redirect(url_for('read'))


@app.route('/read')
def read():
    cur = g.db.execute('select fullname,username,photo \
                   from users order by id desc')

    users = [dict(fullname=row[0], username=row[1],photo=row[2]) \
                           for row in cur.fetchall()]

    return render_template('users.html',users=users)


@app.route('/update_user/<username>')
def update_user(username):
    cur = g.db.execute('select fullname, username, photo from users where username = ?', [username])
    row = cur.fetchone()
    if row:
        user = dict(fullname=row[0], username=row[1],photo=row[2])
        return render_template('update.html',user=user)

@app.route('/update', methods=['POST'])
def update():
    fullname = request.form['fullname']
    username = request.form['username']
    usernm = request.form['usernm']
    file = request.files['photo']
    if file and allowed_file(file.filename):
        photo = file.filename
        file.save(os.path.join('uploads', photo))
        g.db.execute('update users set fullname=?, username=?, photo=?\
                      where username=?',[fullname, username, photo, usernm])
        g.db.commit()
    else:
        g.db.execute('update users set fullname=?, username=?\
                      where username=?',[fullname, username, usernm])
        g.db.commit()
    flash('Entry successfully updated')
    return redirect(url_for('read'))

@app.route('/delete/<username>')
def delete(username):
    cur = g.db.execute('select photo from users where username = ?', [username])
    row = cur.fetchone()
    if row:
        cur = g.db.execute('delete from users where username = ?', [username])
        g.db.commit()
        os.remove(os.path.join("uploads", row[0]))
        return redirect(url_for('read'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads',
                           filename)

@app.route('/', methods=['GET', 'POST'])
def login():
   error = None
   if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if login_user(username,password):
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('add_user'))
        else:
            error = 'Invalid username or password'
   return render_template('login.html', error=error)

@app.route('/adduser',methods=['GET', 'POST'])
def adduser():
    if request.method == 'POST':
        username = request.form['username']
        fullname = request.form['fullname']
        photo = request.form['photo']
        password = request.form['password']
        cur = g.db.execute('insert into users (fullname,photo) \
                             values (?, ?)',
            [fullname, photo])
        g.db.execute('insert into logins (username,password,uid) \
                             values (?, ?, ?)',
            [username, password, cur.lastrowid])
        g.db.commit()
        flash('New user added successfully')
        #return redirect(url_for('read'))
    return render_template('adduser.html')

def login_user(username,password):
    cur = g.db.execute('select id from users where username = ? and password = ?', [username, hash_pass(password)])
    row = cur.fetchone()
    if row:
        session['uid']=row[0]
        return True
    else:
        return False

def hash_pass(password):
	return crypt.crpyt(password,SECRET_KEY)

if __name__ == "__main__":
    app.debug = True
    app.run(port=9000)
