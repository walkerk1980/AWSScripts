#!/bin/bash

region='us-west-2'
#bucket to save query results in
bucket="s3://aws-athena-query-results-319351118808-us-west-2/"
#query to send to Athena
query='select * from cloudtrail_logs limit 1'

qed=$(aws athena start-query-execution --query-string "$query" --result-configuration OutputLocation=$bucket --output text --region $region)

if [ $? -eq 0 ]; then
  echo "Executing query ID:  $qed"
  while [ "$(aws athena get-query-execution --query-execution-id $qed  --query QueryExecution.Status.State --output text --region $region)" == "RUNNING" ]
     do sleep 3
  done
  #Pull results from S3 csv file
  echo
  aws s3 cp $bucket$qed.csv -
  #Pull results directly - this results in output that is harder to parse visually
  #aws athena get-query-results --query-execution-id $qed --query ResultSet.Rows[].Data --region $region
fi

exit 0
