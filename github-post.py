import urllib
import urllib2
import os


github_token = os.environ['GITHUB_TOKEN']

def github_post(repo, commit, context, state, job_url, description):
    url = '%s/statuses/%s' % (repo, commit)
    print "Setting status on %s" % url
    values = {  'context': context,
                'state': state,
                'target_url': job_url,
                'description': description }
    token_string = 'token %s' % github_token
    headers = { 'Authorization': token_string }
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(req)
    the_page = response.read()
    print response.getcode()

github_post(
    'http://api.github.com/repos/DACH-NY/jenkins-pipeline-playground',
    'ddd082913e500ab5d9e593dbe901697a07076f07',
    'continuous-integration/jenkins/pr-job-up-to-date-check',
    'failure',
    'http://xjob.com',
    'nodescription')
