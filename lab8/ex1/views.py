from flask import Flask, request, jsonify, json
from flask import render_template as template, current_app

app= Flask(__name__)

@app.route('/hellojson')
def hellojson():
  msg = 'hello world'
  return jsonify(message=msg)

@app.route('/')  
def index():
  return template('index.html')
    
@app.route('/hellojsonp')
def hellojsonp():
  callback = request.args.get('callback', False)
  result = '{"message":"hello world"}'
  mimetype = 'application/javascript'
  
  if callback and callback != '?':
    content = str(callback) + "(" + result + ");"
    return current_app.response_class(content, mimetype=mimetype)
  else:
    return current_app.response_class(result, mimetype=mimetype)

@app.route('/jsonp')
def jsonp():
  return template('jsonp.html')
    
if __name__ == "__main__":
  app.debug = True
  app.run(port=9000)