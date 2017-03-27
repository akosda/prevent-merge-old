#!/usr/bin/env bash

set -eux

curl -XPOST -H "Authorization: token ${MY_GIT_TOKEN}" https://api.github.com/repos/akosda/prevent-merge-old/statuses/1e37f061ed8c6a0c82567495206dcc01b65b0aae -d "{
  \"state\": \"success\",
  \"target_url\": \"http://job-url.com\",
  \"description\": \"Job ran recently\",
  \"context\": \"continuous-integration/jenkins/pr-job-up-to-date-check\"
}"
