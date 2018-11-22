#!/usr/bin/env bash

echo 'Running DITTO web api script'
cd $1
echo $PWD
source /home/vagrant/ditto_web_api/venv/bin/activate
PYTHONPATH=./ python DittoWebApi/main.py
