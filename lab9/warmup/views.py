from flask import Flask, request, jsonify, json
from flask import render_template as template

app= Flask(__name__)

@app.route('/')
def drag():
  return template('drag.html')  

if __name__ == "__main__":
  app.debug = True
  app.run(port=9000)