#!/usr/bin/env bash
set -e

# http://stackoverflow.com/questions/821396/aborting-a-shell-script-if-any-command-returns-a-non-zero-value
set -e
BRANCH=$1

case "$BRANCH" in
'develop') cluster=testing ;;
'main') cluster=production ;;
*) cluster= ;;
esac

if [ -z "$cluster" ]; then
    echo "Not deploying branch $BRANCH."
    exit 0
else
  # grab config from remote...
  export AWS_STORAGE_BUCKET_NAME=$(aws ssm get-parameter --name "/marketing_center/backend/$cluster/aws_storage_bucket_name" --query "Parameter.Value" | sed s/\"//g)
  echo "======================================"
  echo "Collecting static assets"
  echo "======================================"
  python manage.py collectstatic --noinput

  aws ecs update-service --cluster=$cluster --service="marketing_center-$cluster-web" --force-new-deployment
  # aws ecs update-service --cluster=$cluster --service="marketing_center-$cluster-worker" --force-new-deployment
  ./bin/create-migration-task.sh $cluster

#wait for deployments to complete
  echo "Waiting for mc $cluster deployments to complete..."
  aws ecs wait services-stable --cluster=$cluster --services "marketing_center-$cluster-web"
  # aws ecs wait services-stable --cluster=$cluster --services "marketing_center-$cluster-worker"
  echo "mc $cluster deployments complete..."
fi
