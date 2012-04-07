from flask import Flask
from flask import render_template as template

app = Flask(__name__)

@app.route('/')
@app.route('/<name>')
def index(name='Earth'):
    return template('index.html',name=name)


@app.errorhandler(404)
def error404(error):
    return 'Nothing here, sorry'

if __name__ == '__main__':
    app.run()
