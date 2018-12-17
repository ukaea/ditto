# Bucket settings

Story covered: [#82](https://github.com/ukaea/ditto/issues/82)

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

Create a bucket _without_ an `archive_root` specified:
* POST to `http://172.28.129.160:8888/createbucket/`
* show with non-admin user (username `a.u.thorised`, password `foo`) first (fails), then with admin user (username `a.d.ministrator`, password `IAmAdmin`)
* body:
```
{
	"bucket": "ditto-normal",
  "groups": ["main"],
  "data_root": "/usr/tmp/data/ditto_normal"
}
```

Show that `ditto_web_api/DittoWebApi/bucket_settings.ini` exists and now contains the `ditto-normal` bucket settings.

Show that bucket created in Minio web view

Create a bucket _with_ an `archive_root` specified:
* POST to `http://172.28.129.160:8888/createbucket/`
* then with admin user (username `a.d.ministrator`, password `IAmAdmin`)
* body:
```
{
	"bucket": "ditto-readonly",
  "groups": ["main"],
  "data_root": "/usr/tmp/data/ditto_readonly_data",
  "archive_root": "/usr/tmp/data/ditto_readonly_archive"
}
```

Show that `ditto_web_api/DittoWebApi/bucket_settings.ini` now also contains the `ditto-readonly` bucket settings.

Show that bucket created in Minio web view
