stage('poll pr jobs') {
    node('ghc8-centos:7_ami-07f21d11_t2_medium') {
        checkout scm
        def jenkinsUrl="${env.JENKINS_URL}/job/devops/job/jenkins-pipeline-playground"
        def jenkinsUser = "akos.fabian@digitalasset.com"
        def gitHubUrl = "https://api.github.com/repos/DACH-NY/jenkins-pipeline-playground"
        withCredentials([
            [$class: 'StringBinding', credentialsId: 'akosda-github-personal-token', variable: 'GITHUB_TOKEN'],
            [$class: 'StringBinding', credentialsId: 'akosda-jenkins-token', variable: 'JENKINS_TOKEN'],
            ]) {
                sh """
                    python prevent-merging-old.py \
                        $jenkinsUrl \
                        $jenkinsUser \
                        \$JENKINS_TOKEN \
                        $gitHubUrl \
                        \$GITHUB_TOKEN \
                        'akos-.*'
                """
            }
    }
}
