# Deployment

Story covered: [#28](https://github.com/ukaea/ditto/issues/28)

[Wiki page](https://github.com/ukaea/ditto/wiki/Deployment)

## Setup

Use `configuration.ini` for the VM Minio S3 interface.

Have VM up and running beforehand
* in GitBash navigate to `ditto` repository directory
* `vagrant up`
* `vagrant ssh`

## Demo

Update tag in GitHub:
* "release" link between "branches" and "contributors"
* "Draft a new release"
  - version number, e.g. `0.0.1`
  - release title, e.g. `First release`

Update version on host machine
* run `./build_version_number.sh` (`.git` directory must be present)
* show `version.py` file in `ditto_web_api`

Build wheel
* source virtual environment (`source venv/Scripts/activate` on a Windows machine)
* run `./build_package.sh`
* show wheel file in `ditto_web_api/dist`

Move wheel file to `DittoWebApi` (this is synced with the VM)

Deploy wheel on Virtual Machine (use GitBash SSH'ed into VM)
* `mv ditto_web_api/DittoWebApi/DittoWebApi-{version}-py3-none-any.whl /usr/tmp/`
* make a folder to deploy into and move to it (e.g. `mkdir deployment`, `cd deployment`)
* make a python venv and source it: `python36 -m venv .`, `source ~/ditto_web_api/bin/activate`
* Install the package: `pip install /usr/tmp/DittoWebApi-{version}-py3-none-any.whl`

Copy over configuration files
* `cp ~/ditto_web_api/DittoWebApi/configuration.ini lib/python3.6/site-packages/DittoWebApi/configuration.ini`
* `cp ~/ditto_web_api/DittoWebApi/security_configuration.ini lib/python3.6/site-packages/DittoWebApi/security_configuration.ini`
* `cp ~/ditto_web_api/DittoWebApi/bucket_settings.ini lib/python3.6/site-packages/DittoWebApi/bucket_settings.ini`

Run the server
* `ditto_server`

Call the server as normal
* e.g. check heartbeat from Postman on host machine `http://172.28.129.160:8888/`
