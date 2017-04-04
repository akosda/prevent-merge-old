#!/usr/bin/env bash

set -eux

curl -XPOST -H "Authorization: token ${GITHUB_TOKEN}" https://api.github.com/repos/DACH-NY/jenkins-pipeline-playground/statuses/ddd082913e500ab5d9e593dbe901697a07076f07 -d "{
  \"state\": \"failure\",
  \"target_url\": \"http://job-url.com\",
  \"description\": \"Job is outdated\",
  \"context\": \"continuous-integration/jenkins/pr-job-up-to-date-check\"
}"
