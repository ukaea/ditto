# Performance tests

Run on the Development Environment VM.

Have DITTO server up and running.

## Upload a single large file

Ensure that the bucket `ditto-test` exists in the ECHO CEPH cluster. The local data root directory path needs to be set in the bucket settings, either by writing this in the `bucket_settings.ini` file or by creating the bucket through the DITTO API.

To create a 1GB file, run `generateRandomFile.sh` with the local data root directory path as the argument, e.g.:
```
sh generateRandomFile.sh /usr/tmp/data/
```
Note that it will take a minute or so to generate this 1GB file.

