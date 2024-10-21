#!/usr/bin/env bash
set -e
BRANCH=$1

case "$BRANCH" in
'develop') TAG=testing ;;
'staging') TAG=staging ;;
'main') TAG=production ;;
*) TAG=latest ;;
esac

aws ecr get-login-password --region us-west-1 | \
docker login --username AWS --password-stdin 369308009396.dkr.ecr.us-west-1.amazonaws.com
docker tag marketing_center:latest 369308009396.dkr.ecr.us-west-1.amazonaws.com/marketing_center:$TAG &&
docker push 369308009396.dkr.ecr.us-west-1.amazonaws.com/marketing_center:$TAG
