import urllib2
import base64
import json
import time

jenkins_url = 'http://localhost:8080'

def auth_headers(username, password):
    return 'Basic ' + base64.encodestring('%s:%s' % (username, password))[:-1]

def jenkins_json_response(path):
    auth = auth_headers('akoslocal', '623b34224508efb9bad027a7d29e1b3e')
    req = urllib2.Request(path)
    req.add_header('Authorization', auth)
    resp = urllib2.urlopen(req)
    return json.load(resp)

def get_jobs(url):
    j = jenkins_json_response('%s/api/json' % url)
    return j["jobs"]

def is_blue_job(job):
    color_key = u'color'
    if color_key in job:
        if job[color_key] == u'blue':
            return True
        else:
            return False
    else:
        return False

def get_last_completed_build_url(url):
    j = jenkins_json_response('%s/api/json' % url)
    return j[u'lastCompletedBuild'][u'url'].encode('ascii')

def get_timestamp(url):
    j = jenkins_json_response('%s/api/json' % url)
    return j[u'timestamp']

def get_commit_hash(url):
    j = jenkins_json_response('%s/api/json' % url)
    action = j[u'actions'][1]
    commit = None
    if u'lastBuiltRevision' in action:
        commit = action[u'lastBuiltRevision'][u'SHA1']
    return commit

def is_timestamp_too_old(timestamp):
    current_timestamp = int(time.time() * 1000)
    return current_timestamp - timestamp > 15 * 24 * 3600 * 1000

def main():
    jobs = get_jobs(jenkins_url)
    blue_jobs = [job for job in jobs if is_blue_job(job)]
    blue_urls = [job[u'url'].encode('ascii') for job in blue_jobs]
    last_build_urls = [get_last_completed_build_url(url) for url in blue_urls]
    for build_url in last_build_urls:
        print build_url
        timestamp = get_timestamp(build_url)
        print timestamp
        if(is_timestamp_too_old(timestamp)):
            print "Job is NOT recent"
            commit_hash = get_commit_hash(build_url)
            print "Setting status on commit hash %s" % commit_hash
        print ""

main()
