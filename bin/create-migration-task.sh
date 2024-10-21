#!/usr/bin/env bash

set -e

cluster=$1

MIGRATION_TASK_ARN=$(
  aws ecs run-task \
    --cluster=$cluster \
    --task-definition=marketing_center-$cluster-migration \
    --count=1 \
    --launch-type=FARGATE \
    --network-configuration="awsvpcConfiguration={subnets=[subnet-073f3eb7993cadd41],securityGroups=[sg-0e694079a5d80aff6],assignPublicIp=ENABLED}" \
    --output=json |
    python -c 'import sys,json;print(json.load(sys.stdin)["tasks"][0]["taskArn"])'
)

MIGRATION_TASK_ID=$(echo $MIGRATION_TASK_ARN | cut -d "/" -f 3)

echo "waiting for migration to start..."
aws ecs wait tasks-running --cluster=$cluster --tasks $MIGRATION_TASK_ARN --output=json

echo "migration is running"

aws ecs wait tasks-stopped --cluster=$cluster --tasks $MIGRATION_TASK_ARN --output=json

echo "migration completed"

MIGRATION_LOG=$(
  aws logs get-log-events \
    --start-from-head \
    --log-group-name=/ecs/leads-$cluster \
    --log-stream-name=ecs/leads-$cluster-migration/$MIGRATION_TASK_ID \
    --output=json |
    python -c 'import sys;import json;print("\n".join([l["message"] for l in json.load(sys.stdin)["events"]]))'
)

echo $MIGRATION_LOG
if [[ $MIGRATION_LOG == *"Traceback"* ]]; then
  exit 1
fi
