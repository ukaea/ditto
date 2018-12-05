Walk through [Data Security wiki page](https://github.com/ukaea/ditto/wiki/Data-Security)

Put example `security_configuration.ini` file in `ditto/ditto_web_api/DittoWebApi/`.

Vagrant VM up and running. In GitBash:
* `cd` to `ditto` repository
* `vagrant up`
* `vagrant ssh`
* `sudo systemctl start minio`
* `cd ditto_web_api`
* `source venv/bin/activate`
* `PYTHONPATH=./ python DittoWebApi/main.py`

In Postman:
* POST request to `http://172.28.129.160:8888/listpresent/` is refused
* Authentication tab > Basic Auth in drop-down menu > enter Username and Password
  - Correct credentials; one or other incorrect
  - Show both authentication and authorisation
