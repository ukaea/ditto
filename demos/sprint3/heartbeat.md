Vagrant VM up and running. In GitBash:
* `cd` to `ditto` repository
* `vagrant up`
* `vagrant ssh`
* `sudo systemctl start minio`
* `cd ditto_web_api`
* `source venv/bin/activate`
* `PYTHONPATH=./ python DittoWebApi/main.py`

In Postman:
* GET request to `http://172.28.129.160:8888/` shows system is up and running
