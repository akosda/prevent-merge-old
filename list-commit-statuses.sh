#!/usr/bin/env bash

set -eu

curl -s -XGET -H "Authorization: token ${GITHUB_TOKEN}" \
    https://api.github.com/repos/DACH-NY/jenkins-pipeline-playground/statuses/ddd082913e500ab5d9e593dbe901697a07076f07
