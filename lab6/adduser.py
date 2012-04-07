import sqlite3
import getpass
import crypt
SECRET = 'i luv benny :)'

password = getpass.getpass('your password: ')
hashedpassword = crypt.crypt(password,SECRET)
fullname = raw_input('your fullname: ')
username = raw_input('your user: ')
photo = raw_input('photo url: ')

conn = sqlite3.connect('users.db')

output = conn.execute('INSERT into users (fullname, photo) \
                     values (?, ? )',
    [fullname, photo])
conn.commit()

# get last id
id = output.lastrowid
conn.execute('INSERT into logins (uid,username, password) \
                     values (?, ?, ? )',
    [id,username,hashedpassword])

cur = conn.execute('SELECT * from logins order by uid desc')
conn.commit()
print cur.fetchall()
cur.close()