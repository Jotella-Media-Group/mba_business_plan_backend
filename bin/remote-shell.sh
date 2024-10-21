#!/usr/bin/env bash
# Open Remote Shell
# Example: ./remote-shell.sh testing {start,stop}
set -e

export APP=marketing_center
export CLUSTER=$1
export COMMAND=$2
export PROFILE=$4
existing_arg=$3

check_existing_task() {
  echo $(
    aws ecs list-tasks \
      --cluster=$CLUSTER \
      --profile=$PROFILE \
      --family=$APP-$CLUSTER-shell \
      --output=json \
      --desired-status=RUNNING |
      python -c 'import sys,json;print((json.load(sys.stdin).get("taskArns") or ["all stopped"])[0])'
  )
}

start_shell() {
  TSHELL_ARN=$(check_existing_task)

  if [[ $TSHELL_ARN == 'all stopped' || $existing_arg != '--existing' ]]; then
    TSHELL_ARN=$(
      aws ecs run-task \
        --cluster=$CLUSTER \
        --task-definition=$APP-$CLUSTER-shell \
        --count=1 \
        --profile=$PROFILE \
        --launch-type=FARGATE \
        --network-configuration="awsvpcConfiguration={subnets=[subnet-073f3eb7993cadd41],securityGroups=[sg-0e694079a5d80aff6],assignPublicIp=ENABLED}" \
        --output=json |
        python -c 'import sys,json;print(json.load(sys.stdin)["tasks"][0]["taskArn"])'
    )
  else
    echo already running shell found $TSHELL_ARN
  fi

  echo "waiting for remote shell to be ready..."
  aws ecs wait tasks-running --cluster=$CLUSTER --tasks $TSHELL_ARN --output=json --profile=$PROFILE \

  TSHELL_IP=$(
    aws ecs describe-tasks --cluster=$CLUSTER --tasks $TSHELL_ARN --output=json --profile=$PROFILE  |
      python -c 'import sys,json;print(json.load(sys.stdin)["tasks"][0]["attachments"][0]["details"][-1]["value"])'
  )

  echo "remote shell is ready. ip: ${TSHELL_IP}"
  echo "Create ssh tunnel using command: ssh -i ~/.ssh/keys/leads.pem -L 8888:${TSHELL_IP}:8888 first_name@bastion.leads.com"
  echo "Then open in browser: http://localhost:8888"
  echo "Don't forget to shutdown shell after use. ./remote-shell.sh ${CLUSTER} ${APP} stop"
}

stop_shell() {
  TSHELL_ARN=$(check_existing_task)

  if [[ $TSHELL_ARN == 'all stopped' ]]; then
    echo "no active shells"
    exit 0
  fi

  aws ecs stop-task --cluster=$CLUSTER --task=$TSHELL_ARN --output=json --profile=$PROFILE >/dev/null
  echo "shutting down remote shell..."
  aws ecs wait tasks-stopped --cluster=$CLUSTER --tasks $TSHELL_ARN --output=json --profile=$PROFILE
}

case $COMMAND in
'start')
  start_shell
  ;;
'stop')
  stop_shell
  ;;
*)
  echo "Unknown command: ${COMMAND}. Available: start,stop"
  ;;
esac
