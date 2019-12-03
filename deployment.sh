#!/bin/bash
echo $PWD
aws s3 sync . s3://test-automation-pydata --region=us-east-1 --exclude '.git/*'
python launch_server.py