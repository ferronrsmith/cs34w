import random
from flask import request, redirect, url_for, json, render_template as template, g
from models import Cellar
from application import app


@app.route('/wines', methods=['PUT','POST','GET', 'DELETE'])
@app.route('/wines/<id>', methods=['PUT','POST','GET', 'DELETE'])
def getwines(id=None):
    if request.method == 'GET' and id:
        qry = Cellar.query(Cellar.id == id)
        row = qry.get()
        if row :
            wine = dict(id=row.id, name=row.name,year=row.year,\
                grapes=row.grapes,country=row.country,region=row.region, description=row.description, picture=row.picture)
            return json.dumps(wine)
    elif request.method == 'GET':
        qry = Cellar.query().order(Cellar.name)
        wines = [dict(id=str(row.id), name=row.name,year=row.year,\
                 grapes=row.grapes,country=row.country,region=row.region, description=row.description, picture=row.picture)
                 for row in qry]
        return json.dumps(wines)
    elif request.method == 'POST':
        ls = request.form
        if ls:
            raw = ls.keys()[0]
            record = json.loads(raw)
            query = Cellar.query()
            count = query.count()
            print str(count) + ' this is the count value'
            wine = Cellar(
                id = str(random.randint(count, count*1000)),
                name = record['name'],
                year = record['year'],
                grapes = record['grapes'],
                country = record['country'],
                region = record['region'],
                description = record['description']
            )
            wine.put()
            return raw
    elif request.method == 'PUT':
        record = json.loads(request.data)
        if record:
            qry = Cellar.query(Cellar.id == id)
            wine = qry.get()
            wine.name = record['name']
            wine.year = record['year']
            wine.grapes = record['grapes']
            wine.country = record['country']
            wine.region = record['region']
            wine.description = record['description']
            wine.put()

        return json.dumps(record)
    elif request.method == 'DELETE':
        qry = Cellar.query(Cellar.id == id)
        wine = qry.get()
        wine.key.delete()
        return redirect(url_for('index'))

@app.route('/wines/search/<query>')
def findbyname(query):
    cur = g.db.execute('select * FROM wine where name like ? order by name', ['%' + query.upper() + '%'])
    wines = [dict(id=row[0], name=row[1],year=row[2],\
        grapes=row[3],country=row[4],region=row[5], description=row[6], picture=row[7])
             for row in cur.fetchall()]
    return json.dumps(wines)

@app.route('/')
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
