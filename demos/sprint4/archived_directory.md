# Archived directory

The location of the archived directories can be configured to a different location from where the data are stored (typical use case: where the data directory is read-only).

Stories covered: [#7](https://github.com/ukaea/ditto/issues/7), [#8](https://github.com/ukaea/ditto/issues/8)

## Setup

Use `configuration.ini` for the VM Minio S3 interface.

Have VM up and running beforehand
* in console navigate to `ditto` repository directory
* `vagrant up`
* `vagrant ssh`

Open another console instance
* navigate to `ditto` repository
* `vagrant ssh`

Check Minio server is up:
* `systemctl status minio`
* if not, run `sudo systemctl start minio`

Connect to the Minio server GUI in a host machine browser:
* URL `http://172.28.129.160:9000/minio/login`
* access key `AKIAIOSFODNN7EXAMPLE`
* secret key `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`

Have Postman up

## Demo

Show `archived_directory/bucket_settings.ini` and copy it to `ditto_web_api/DittoWebApi`

In one console instance, launch DITTO:
```
cd ditto_web_api
source venv/bin/activate
PYTHONPATH=./ python DittoWebApi/run_ditto.py
```

In the other console instance, create files in the data directories:
```
mkdir /usr/tmp/data/ditto_normal; echo "test" > /usr/tmp/data/ditto_normal/test.txt; mkdir /usr/tmp/data/ditto_normal/subdir/; echo "subtest" > /usr/tmp/data/ditto_normal/subdir/subtest.txt
mkdir /usr/tmp/data/ditto_readonly_data; echo "readtest" > /usr/tmp/data/ditto_readonly_data/readtest.txt; mkdir /usr/tmp/data/ditto_readonly_data/subdir/; echo "subreadtest" > /usr/tmp/data/ditto_readonly_data/subdir/subreadtest.txt
```

In Minio browser view, create buckets `ditto-normal` and `ditto-readonly`

In PostMan, run a `copydir` for `ditto-normal`:
* POST to `http://172.28.129.160:8888/copydir/`
* username `a.u.thorised`, password `foo`
* body `{"bucket":"ditto-normal"}`

Show that files copied to Minio in browser and that `.ditto-archived` files have been written as before:
```
cat /usr/tmp/data/ditto_normal/.ditto_archived
cat /usr/tmp/data/ditto_normal/subdir/.ditto_archived
```

In PostMan, run a `copydir` for `ditto-readonly`:
* POST to `http://172.28.129.160:8888/copydir/`
* username `a.u.thorised`, password `foo`
* body `{"bucket":"ditto-readonly"}`

Show that files copied to Minio in browser and that `.ditto-archived` files have been written in `ditto_readonly_archive` but not in `ditto_readonly_data`:
```
cat /usr/tmp/data/ditto_readonly_archive/.ditto_archived
cat /usr/tmp/data/ditto_readonly_archive/subdir/.ditto_archived
ls  /usr/tmp/data/ditto_readonly_data
ls  /usr/tmp/data/ditto_readonly_data/subdir
```
