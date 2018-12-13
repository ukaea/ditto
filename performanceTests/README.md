# Performance tests

## Uploading random files

Run on the Development Environment VM.

### Setup

Ensure that the bucket `ditto-test` exists in the ECHO CEPH cluster. The local data root directory path needs to be set in the bucket settings, either by writing this in the `bucket_settings.ini` file or by creating the bucket through the DITTO API.

To create the files, run `generateRandomFile.sh` with the local data root directory path as the argument, e.g.:
```
sh generateRandomFile.sh /usr/tmp/data/
```
Note that it will take several minutes to generate the files.

### Run test

Have DITTO server up and running.

Run `timingTest.sh` with the following arguments:
1. the local data root directory
2. the username for a user that who authorised for the `ditto-test` bucket
3. the password for that user

For example,
```
sh timingTest.sh /usr/temp/data/ a.u.thorised foo
```

The test will take several minutes to complete. The results will be written into `results.csv`.
