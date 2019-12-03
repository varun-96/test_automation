#!/bin/sh
apt-get update -y
apt-get --assume-yes install python-pip unzip curl
pip install awscli==1.15.45
#####################
# sync the codebase #
#####################
aws s3 sync s3://test-automation-pydata /home/ubuntu/test_automation/

chown ubuntu:ubuntu -R /home/ubuntu/test_automation

# curl --header "Content-Type: application/json" --request POST --data '{"text":"NER v3 codebase and word2vec vectors synced", "username":"Trainer", "icon_emoji": ":spacy:"}' https://hooks.slack.com/services/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

###########################
# Download tagged dataset #
###########################
aws s3 cp s3://test-automation-pydata/DATA/ /home/ubuntu/test_automation/data/
aws s3 cp s3://test-automation-pydata/CODEBASE/ /home/ubuntu/test_automation/


####################################
# Set up conda environment #
####################################
wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh && \
  sudo  /bin/bash miniconda.sh -b -p /opt/conda && \
   sudo ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh


# avail `conda` command in PATH
chmod +x /opt/conda/etc/profile.d/conda.sh
. /opt/conda/etc/profile.d/conda.sh

# curl --header "Content-Type: application/json" --request POST --data '{"text":"Setting up python enviroment..", "username":"Trainer", "icon_emoji": ":spacy:"}' https://hooks.slack.com/services/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

# Set up python enviroment
conda create --name train_env python=3.6
conda activate train_env

# To avoid RuntimeError of click
# RuntimeError: Click will abort further execution because Python 3..
# more on:
# http://click.palletsprojects.com/en/7.x/python3/
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

# start training
python test_automation/train.py
# curl --header "Content-Type: application/json" --request POST --data '{"text":"NER v3 training done!", "username":"Trainer", "icon_emoji": ":spacy:"}' https://hooks.slack.com/services/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

aws s3 cp /home/ubuntu/test_automation/iris_model.pkl s3://test-automation-pydata/

# curl --header "Content-Type: application/json" --request POST --data '{"text":"NER v3 model pushed to `s3://cypher-ner/uznani/`", "username":"Trainer", "icon_emoji": ":spacy:"}' https://hooks.slack.com/services/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

# aws s3 cp /var/log/cloud-init-output.log s3://cypher-ner/uznani/uznani_ner_model/

shutdown now