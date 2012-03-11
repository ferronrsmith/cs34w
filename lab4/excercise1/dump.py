import json, urllib2
import requests

def get_twitter_feed(username) :
    if len(username.strip()) > 0 or username is not None:
        url = 'https://twitter.com/users/{uname}.json'.format(uname=username)
        return requests.get(url)

    else:
        return None




req = get_twitter_feed('ferronrsmith');
bdict = json.loads(req.text)
print bdict['name']