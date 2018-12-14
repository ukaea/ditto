# Bucket settings

Story covered: [#28](https://github.com/ukaea/ditto/issues/28), [#82](https://github.com/ukaea/ditto/issues/82)

If a separate `archive_root` is specified for a given bucket, the `.ditto-archived` files are written to this directory (and matching sub-directories) instead of the `data_root` directory. If no `archive_root` is specified, `.ditto-archived` files are still written in the data directory.

When `createbucket` is called by an admin user, the arguments `groups` and `data_root` are now required. `archive_root` is optional. So long as the bucket does not already exist, it is created at the S3 end (as before) and added to the `bucket_settings.ini` file (new functionality). When `createbucket` is called by a non-admin user the request is refused.

## Setup

DITTO configuration
* Use `configuration.ini` for the VM Minio S3 interface.
* Do not use a `bucket_settings.ini` file.
* One user needs to be in a group names as `AdminGroups` in `configuration.ini`.

Have VM up and running beforehand
* in GitBash navigate to `ditto` repository directory
* `vagrant up`
* `vagrant ssh`
* `cd ditto_web_api`
* `source venv/bin/activate`

Check Minio server is up:
* `systemctl status minio`
* if not, run `sudo systemctl start minio`

Connect to the Minio server GUI in a host machine browser:
* URL `http://172.28.129.160:9000/minio/login`
* access key `AKIAIOSFODNN7EXAMPLE`
* secret key `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`

## Demo
