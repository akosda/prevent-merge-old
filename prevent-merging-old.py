import urllib2
import base64
import json
import time
import datetime
import sys
import re

max_hours = 12

if len(sys.argv) != 5:
    print 'Usage: %s <jenkins-url> <jenkins-user> <jenkins-token> <github-token>' % sys.argv[0]
    sys.exit(1)

jenkins_url    = sys.argv[1]
jenkins_user   = sys.argv[2]
jenkins_token  = sys.argv[3]
github_token   = sys.argv[4]

def auth_headers(username, password):
    return 'Basic ' + base64.encodestring('%s:%s' % (username, password)).replace('\n','')
    # base64 strings contain \n at every 76 characters, which must be replaced
    # to avoid invalid headers

def jenkins_json_response(path):
    auth = auth_headers(jenkins_user, jenkins_token)
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

def is_pr_job(job):
    regex = re.compile('PR-.*', re.IGNORECASE)
    job_name = job[u'name'].encode('ascii')
    return re.match(regex, job_name) is not None

def get_last_completed_build_url(url):
    j = jenkins_json_response('%s/api/json' % url)
    return j[u'lastCompletedBuild'][u'url'].encode('ascii')

def get_timestamp(url):
    j = jenkins_json_response('%s/api/json' % url)
    return j[u'timestamp']

def get_commit_hash(url):
    j = jenkins_json_response('%s/api/json' % url)
    revisions = [action[u'lastBuiltRevision'][u'SHA1'].encode('ascii') for action in j[u'actions'] if u'lastBuiltRevision' in action]
    return revisions[0] if revisions else None

def is_timestamp_too_old(timestamp):
    current_timestamp = int(time.time() * 1000)
    return current_timestamp - timestamp > max_hours * 3600 * 1000

# def github_post(repo, commit, context, state, url, description):


def main():
    jobs = get_jobs(jenkins_url)
    pr_jobs = [job for job in jobs if is_pr_job(job)]
    blue_jobs = [job for job in pr_jobs if is_blue_job(job)]
    blue_urls = [job[u'url'].encode('ascii') for job in blue_jobs]
    last_build_urls = [get_last_completed_build_url(url) for url in blue_urls]
    for build_url in last_build_urls:
        print 'Processing %s' % build_url
        timestamp = get_timestamp(build_url)
        timestamp_date = datetime.datetime.fromtimestamp(timestamp / 1000).strftime('%c')
        if(is_timestamp_too_old(timestamp)):
            print "\tJob is outdated (> %s hours)! Setting its GitHub status..." % max_hours
            commit_hash = get_commit_hash(build_url)
            print "\tCommit hash: %s" % commit_hash
        else:
            print "\tOK"
        print ""

main()
