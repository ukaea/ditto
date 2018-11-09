# Set up Development Environment

## Stories covered

**14** Set up virtual development environment
https://github.com/ukaea/ditto/issues/14

## Demo

Show documentation
* https://github.com/ukaea/ditto/wiki/DevEnvSetUp

Show code
* https://github.com/ukaea/ditto/blob/master/Vagrantfile
* https://github.com/ukaea/ditto/tree/master/dev-environment

Bash
1. `vagrant up`
2. `vagrant ssh`
3. `systemctl status minio`
  - `sudo systemctl start minio`
4. `cd ditto_web_api`
5. `source venv/bin/activate`
6. `PYTHONPATH=./ python DittoWebApi/main.py`
7. `sh runCodeAnalysis.sh`
8. `sh runCodeCoverage.sh`

Browser
7. http://172.28.129.160:9000/
