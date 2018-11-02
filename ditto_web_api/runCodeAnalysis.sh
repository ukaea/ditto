#!/usr/bin/env bash

echo "======================"
echo "Running flake8 ..."
flake8 DittoWebApi

echo 
echo "======================"
echo "Running pylint ..."
pylint DittoWebApi
