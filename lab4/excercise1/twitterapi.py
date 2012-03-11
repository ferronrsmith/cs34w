from flask import Flask, render_template
import json, urllib2

app = Flask(__name__)

@app.route('/feed/<name>')
def index(name=None):
    return render_template('feed.html',name=get_twitter_feed(name))

def get_twitter_feed(username) :
    if len(username.strip()) > 0 or username is not None:
        url = 'https://twitter.com/users/{uname}.json'.format(uname=username)
        f = urllib2.urlopen(url)
        response = f.read()
        f.close()
        return json.loads(response)
    else:
        return None

if __name__ == "__main__" :
    app.run()