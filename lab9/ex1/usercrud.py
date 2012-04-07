from flask import Flask, request, g,render_template, \
           url_for, redirect, flash, send_from_directory
import sqlite3, os

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
    fullname = request.form['fullname']
    username = request.form['username']
    fileobjs = request.files.iterlistvalues()
    for files in  fileobjs:
        for file in files:
            if file and allowed_file(file.filename):
                photo = file.filename
                file.save(os.path.join('uploads', photo))
                g.db.execute('insert into users (fullname, username, photo) \
                                     values (?, ?, ?)',
                    [fullname, username, photo])
        g.db.commit()
        flash('New entry was successfully posted')
    return redirect(url_for('read'))


@app.route('/read')
@app.route('/')
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
    row = cur.fetchall()
    if row:
        cur = g.db.execute('delete from users where username = ?', [username])
        g.db.commit()
        for i in range(row.rowcount):
            os.remove(os.path.join("uploads", row[i]))
        return redirect(url_for('read'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads',
                           filename)
    #return render_template('multiple_uploads.html')
    #not sure but i think u mite need the html file to tell it wat to
    #do here...wen i try to select multiple files it doesnt work...

if __name__ == "__main__":
    app.debug = True
    app.run(port=9000)
