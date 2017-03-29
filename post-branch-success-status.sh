#!/usr/bin/env bash

set -eux

curl -XPOST -H "Authorization: token ${MY_GIT_TOKEN}" https://api.github.com/repos/akosda/prevent-merge-old/statuses/4d8ea62d0d45012401e63be3d2f61e6dcd58ee77 -d "{
  \"state\": \"failure\",
  \"target_url\": \"http://job-url.com\",
  \"description\": \"Job is outdated\",
  \"context\": \"continuous-integration/jenkins/pr-job-up-to-date-check\"
}"
