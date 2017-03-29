import urllib2
import base64
import json

def auth_headers(username, password):
    return 'Basic ' + base64.encodestring('%s:%s' % (username, password))[:-1]

def jenkins_json(path):
    auth = auth_headers('akoslocal', '623b34224508efb9bad027a7d29e1b3e')
    top_level_url = "http://localhost:8080"
    a_url = "%s/%s" % (top_level_url, path)
    req = urllib2.Request(a_url)
    req.add_header('Authorization', auth)
    return json.load(urllib2.urlopen(req))

def main():
    j = jenkins_json('/api/json?pretty=true')
    print j["jobs"]

main()
