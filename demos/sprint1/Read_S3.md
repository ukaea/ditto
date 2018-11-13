# Web App reads from S3 interface

## Stories covered

**3** Web service reads from S3 interface
https://github.com/ukaea/ditto/issues/3

## Demo

Bash
1. `vagrant up`
2. `vagrant ssh`
3. `systemctl status minio`
  - `sudo systemctl start minio`
4. `cd ditto_web_api`
5. `source venv/bin/activate`
6. `PYTHONPATH=./ python DittoWebApi/main.py`

Browser
7. http://172.28.129.160:9000/ to show what files exist

Postman
8. http://172.28.129.160:8888/listpresent/ to confirm
9. http://172.28.129.160:8888/listpresent/subdir/ to display subdirectory
