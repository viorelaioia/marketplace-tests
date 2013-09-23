#!/bin/bash

PROJECT_DIR=$1

# Change directory to project directory
pushd $PROJECT_DIR

# Do the work
python jenkins_status.py

# Commit to the repo and push
git add status.json
git commit -m "status update at $(date)"
git push https://$GH_USER:$GH_PASS@github.com/mozilla/marketplace-tests.git gh-pages

# Where you were...
popd
