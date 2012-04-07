from flask import Flask, request, json, render_template as template, g
import sqlite3


SECRET_KEY = "the global object 'g' needs this"
app= Flask(__name__)

# database method, which is triggered
# before each request
def connect_db():
    return sqlite3.connect('./cellar.db')

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route('/wines')
@app.route('/wines/<id>', methods=['PUT','POST','GET'])
def getwines(id=None):
    if request.method == 'GET' and id:
        cur = g.db.execute('select * FROM wine where id = ?', [id])
        row = cur.fetchone()
        if row :
            wine = dict(id=row[0], name=row[1],year=row[2],\
                grapes=row[3],country=row[4],region=row[5], description=row[6], picture=row[7])
            return json.dumps(wine)
    elif request.method == 'GET':
        cur = g.db.execute('select * FROM wine ORDER BY name')
        wines = [dict(id=str(row[0]), name=row[1],year=row[2],\
                 grapes=row[3],country=row[4],region=row[5], description=row[6], picture=row[7])
                 for row in cur.fetchall()]
        return json.dumps(wines)
    elif request.method == 'POST':
        record = json.loads(request.data)
        if record:
            g.db.execute('insert into wine (name,year,grapes,country,region,description) \
                                 values (?, ?, ?, ?, ?, ?, ?)', \
                [record['name'],record['year'],record['grapes'],record['country'],
                 record['region'],record['description']])
            g.db.commit()
        return json.dumps(record)
    elif request.method == 'PUT':
        record = json.loads(request.data)
        if record:
            g.db.execute('UPDATE wine SET name=?, grapes=?, country=?, '
                         'region=?, year=?, description=? WHERE id=?',\
                [record['name'],record['grapes'],record['country'],record['region'],
                 record['year'],record['description'],id])
            g.db.commit()
        return json.dumps(record)
    elif request.method == 'DELETE':
        g.db.execute('DELETE FROM wine WHERE id=?',[id])
        g.db.commit()


@app.route('/wines/search/<query>')
def findbyname(query):
    cur = g.db.execute('select * FROM wine where name like ? order by name', ['%' + query.upper() + '%'])
    wines = [dict(id=row[0], name=row[1],year=row[2],\
        grapes=row[3],country=row[4],region=row[5], description=row[6], picture=row[7])
             for row in cur.fetchall()]
    return json.dumps(wines)

@app.route('/', methods=['GET', 'POST'])
def index():
    return template("index.html")

@app.route('/welcome')
def welcome_page():
    return template("welcome.html")

@app.route('/winelist')
def wine_list():
    return template("wine-list.html")

@app.route('/winedetails')
def wine_details():
    return template("wine-details.html")

if __name__ == "__main__":
  app.debug = True
  app.run(port=9000)