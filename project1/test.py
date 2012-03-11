import re
import json
import urllib2


def gm(desc):
	pat = re.compile('((http(s|)://|)(www.|)youtube.(com|nl)/watch\?v=([a-zA-Z0-9-_=]+)|'
                     '(http(s|)://|)(www.|)vimeo.com/([a-zA-Z0-9-_=]+))')
	#pat = re.compile('http://(?:www.)?(vimeo|youtube).com/(?:watch\?v=)?(.*?)(?:\z|&)')
	print pat.sub('something',desc)

def gf(desc):
    pat = re.compile('((http(s|)://|)(www.|)youtube.(com|nl)/watch\?v=([a-zA-Z0-9-_=]+)|'
                     '(http(s|)://|)(www.|)vimeo.com/([a-zA-Z0-9-_=]+))')
    #pat = re.compile('http://(?:www.)?(vimeo|youtube).com/(?:watch\?v=)?(.*?)(?:\z|&)')
    return pat.finditer(desc)


gm('hey there you! http://www.youtube.com/watch?v=38A1NZEHpxY lol~')	
gm('hey there you! http://vimeo.com/7100569 lol~')

iterator = gf('hey there you! http://www.youtube.com/watch?v=38A1NZEHpxY lol~  http://vimeo.com/7100569 ')

for match in iterator:
    print match.span()


def get_twitter_feed(username) :
    if len(username.strip()) > 0 or username is not None:
        url = 'https://twitter.com/users/{uname}.json'.format(uname=username)
        f = urllib2.urlopen(url)
        response = f.read()
        f.close()
        return json.loads(response)
    else:
        return None