#!~/ditto_web_api/venv/bin/python
python -m pytest --cov-config=.coveragerc --cov-report html --cov-report term --cov=DittoWebApi/src DittoWebApi/tests/
