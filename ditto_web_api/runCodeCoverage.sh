#!/usr/bin/env bash
python -m pytest --cov-config=.coveragerc --cov-report html --cov-report term --cov=DittoWebApi/src DittoWebApi/tests/
