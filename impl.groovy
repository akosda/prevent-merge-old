// This is a pseudo code to summarize the concepts
// of blocking PR merges if the PR's job has not run for a while.

def repo = 'DACH-NY/da'
def upToDateContext = "continuous-integration/jenkins/job-up-to-date-check"
def maxTimeDiff = '12 hours'


class PrJob {
    def run() {
        try {
            doTheUsualStuff()
        } finally {
            def commit = Git.getHeadCommit()
            GitHubApi.setContextStatus(repo, commit, upToDateContext, 'success', ENV.JOB_URL, 'Job is up-to-date')
        }
    }
}

class Manual {
    def doit() {
        GitHubApi.addRequiredStatus(repo, 'master', upToDateContext)
        // Without this: the not-met status is visible in the PRs but not blocking
        // With this: the status is required on EVERY branch that needs to be merged to master
    }
}

class PeriodicJob {
    def run() {
        def blueJobUrls = JenkinsApi.getBlueJobUrls()
        def targetJobUrls = blueJobUrls.filter { it.name.matches('PR-.*') }
        targetJobUrls.each { jobUrl ->
            def lastCompletedBuildUrl = JenkinsApi.getLastCompletedBuildUrl(jobUrl)
            def buildTimestamp = JenkinsApi.getBuildTimestamp(lastCompletedBuildUrl)
            if(timestampTooOld(buildTimestamp)) {
                def commit = JenkinsApi.getCommitHash(lastCompletedBuildUrl)
                GitHubApi.setContextStatus(repo, commit, upToDateContext, 'failure', lastCompletedBuildUrl, 'Job is outdated')
            }
        }
    }

    def timestampTooOld(timestamp) {
        return abs(now - timestamp) > maxTimeDiff
    }
}

class GitHubApi {
    void setContextStatus(repo, commit, context, state, url, description) {
        HTTP.post("${repo}/statuses/${commit}", context, state, url, description)
    }
}

class JenkinsApi {
    def getBlueJobUrls() {
        def jobs = HTTP.get('http://localhost:8080/api/xml?xpath=//job[color=%27blue%27]/url') // actual Jenkins URL
        return jobs // list of urls as strings
    }

    def getLastCompletedBuildUrl(jobUrl) {
        def buildUrl = HTTP.get("${jobUrl}/api/xml?xpath=//lastCompletedBuild/jobUrl") // actual Jenkins URL
        return buildUrl
    }

    def getBuildTimestamp(buildUrl) {
        def timestamp = HTTP.get("${buildUrl}/api/xml?xpath=//timestamp") // actual Jenkins URL
        return timestamp
    }

    def getCommitHash(buildUrl) {
        def commitHash = HTTP.get("{buildUrl}/api/xml?xpath=//lastBuiltRevision/SHA1") // actual Jenkins URL
        return commitHash
    }
}
