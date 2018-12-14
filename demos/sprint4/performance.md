# Performance testing

Story covered: [#92](https://github.com/ukaea/ditto/issues/92)

## Setup

Use `configuration.ini` for the ECHO CEPH cluster S3 interface.

Have VM and DITTO API up and running beforehand
* in GitBash navigate to `ditto` repository directory
* `vagrant up`
* `vagrant ssh`
* `cd ditto_web_api`
* `source venv/bin/activate`
* `ditto_web_api/DittoWebApi/run_ditto.py`

## Demo

Show that S3 interface is empty. In Postman on host machine,
* `http://172.28.129.160:8888/listpresent/` with body `{"bucket": "ditto-test"}` and user/password in Authorisation tab

Open another GitBash instance to run performance tests (use this instance from now on)
* navigate to `ditto` repository
* `vagrant ssh`

Show `performanceTests/generateRandomFile.sh`. Comment out larger files (takes long time).

Generate random files in GitBash
* `cd performanceTests`
* `sh generateRandomFile.sh ~/ditto_web_api/data`
* `ls ~/ditto_web_api/data`
* e.g. `ls -l ~/ditto_web_api/data/single32mb/`

Run performance tests in GitBash (will take a few minutes, depending on which files were generated)
* `sh timingTest.sh ~/ditto_web_api/data a.u.thorised foo`

Show that files have transferred to S3 interface. In Postman on host machine,
* `http://172.28.129.160:8888/listpresent/` with body `{"bucket": "ditto-test"}` and user/password in Authorisation tab

On local machine show results in `performanceTests/results.csv`

Can also show results from Abingdon-Harwell test on 12 Dec by discarding changes.
