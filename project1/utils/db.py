from flask.globals import g
from werkzeug.security import generate_password_hash
from datetime import datetime

def user_exists(username):
    """ The following function checks if a user exists in the db """
    cur = g.db.execute('select * from users where username = ?',[username])
    return cur.rowcount() > 0

def get_user(uid):
    """ The following function retrieves a users from the database """
    cur = g.db.execute('select username from users where id = ?',[uid])
    row = cur.fetchone()
    if row :
        return row[0]

def create_user(username, firstname, lastname, password):
    """ Inserts a user record into the database """
    g.db.execute('insert into users (username, password, firstname, lastname) \
                             values (?, ?, ?, ?)',
        [username, generate_password_hash(password), firstname, lastname])
    # werkzeug security hash is used to secure user password
    g.db.commit()

def get_blog_post(id):
    """  The following methods retrieves a blog with the specified ID from the db   """
    cur = g.db.execute('select title, description_enc, date_created, last_modified, tags, '
                       'id, user_id, description from blog where id = (?)', [id])
    row = cur.fetchone()
    if row :
        return dict(title=row[0], desc=row[1], date_created=row[2],last_modified=row[3],
            tags=row[4], id=row[5], uid=row[6], desc_enc=row[7], comments=get_blog_comments(id))


def get_comment_count(blog_id):
    cur = g.db.execute('select count(*) as count from comments where blog_id = (?)', [blog_id])
    return cur.fetchone()[0]

def create_blog_commment(text,blog_id,user_id):
   g.db.execute('insert into comments (comments,date_created,user_id,blog_id)'
                ' values (?,?,?,?)', [text,datetime.now(),user_id,blog_id])
   g.db.commit()


def get_blog_comments(blog_id):
    cur = g.db.execute('select * from comments where blog_id = (?)', [blog_id])
    comments = [dict(text=row[1],date=row[2],uid=row[3],blog_id=row[4]) for row in cur.fetchall()]
    print comments
    return comments