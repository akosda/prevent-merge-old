import urllib2
import base64
import json

def auth_headers(username, password):
    return 'Basic ' + base64.encodestring('%s:%s' % (username, password))[:-1]

def jenkins_json_response(path):
    auth = auth_headers('akoslocal', '623b34224508efb9bad027a7d29e1b3e')
    req = urllib2.Request(path)
    req.add_header('Authorization', auth)
    resp = urllib2.urlopen(req)
    return json.load(resp)

def is_blue_job(job):
    color_key = u'color'
    if color_key in job:
        if job[color_key] == u'blue':
            return True
        else:
            return False
    else:
        return False

def main():
    j = jenkins_json_response('http://localhost:8080/api/json?pretty=true')
    jobs = j["jobs"]
    blue_jobs = [j for j in jobs if is_blue_job(j)]
    blue_urls = [j[u'url'].encode('ascii') for j in blue_jobs]
    for url in blue_urls:
        print url
        last_completed_build_json = jenkins_json_response('%s/api/json' % url)
        print last_completed_build_json[u'lastCompletedBuild'][u'url']
        print ""

def debug():
    j = jenkins_json_response('http://localhost:8080/job/cred/api/json')

main()
#debug()
