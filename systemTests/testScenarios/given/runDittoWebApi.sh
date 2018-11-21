#!/usr/bin/env bash

echo 'Running DITTO web api script'
cd $1
echo `pwd`
source venv/bin/activate
PYTHONPATH=./ python DittoWebApi/main.py
