#!/usr/bin/bash

set -eux

source /Users/akosfabian/repos/da/dev-env/profile_bash.sh

function http_get() {
    path=$1
}

JOBS=$(curl \
    -X GET \
    --user akoslocal:623b34224508efb9bad027a7d29e1b3e \
    ${JENKINS_URL}/api/json | \
    jq '.jobs | .[] | select(.color == "blue") | .url' | \
    tr -d '"')

for j in $JOBS; do
    echo "The next job is"
    echo $j
done
