# Demonstrate the creation and updating of archive files and
# how they are not transferred

## Archive files created in each directory that has files transferred.
## List each file that has been transferred, if it was an update or a new
## upload, it's size and the time in utc of when it was last transferred/updated

## Stories covered
#7 #8

Setup
* Ensure bucket_settings.ini file in code
* Ensure data directory is set to /home/vagrant/ditto_web_api/data for bucket in bucket settings
* Clear out data directory locally and on s3 end 

Bash (Set up - perform pre demo)
1. `vagrant up`
2. `vagrant ssh`
3. `systemctl status minio`
  - `sudo systemctl start minio`
4. `cd ditto_web_api`
5. `source venv/bin/activate`
6. `cd data`
8. `echo "Hello world! \n" >> test_file.txt`
7. `mkdir some_files`
  - `cd some_files`
8. `echo "This is a test file \n" >> another_test_file.txt`
9. `cd ../..`
10. `PYTHONPATH=./ python DittoWebApi/main.py`

Bash (new window)
11. Navigate to data
12. `ls -A` Demonstrate data but no archive file
13. `cd some_files`
14. `ls -A` Again see file but no archive file
15. `cd ..` Get back to root dir for data

Browser
16. http://172.28.129.160:9000/ to show what files exist if
 anything present delete all files and buckets to start from empty

Postman
17. http://172.28.129.160:8888/createbucket/
  body = {"bucket": "ditto-testbucket1"}
18. http://172.28.129.160:8888/copydir/ (post, ensure authentication is as
demonstrated in security demo)
  body = {"bucket": "ditto-testbucket1"} to copy across all files from local

Browser
19. http://172.28.129.160:9000/ Show the files copied across but no archive file


Bash
20. `ls -A` now see archive file
21. `cat .ditto_archived` show content of archive file
22. `cd some_files`
23. `ls -A` now see archive file
24. `cat .ditto_archived` show content of archive file
### Update this file and add a new file to the root data dir but keep the old as it is
25. `echo "updating this file \n" >> another_test_file.txt`
26. `cd ..`
27. `echo "A new file to test" >> test_file_2.txt`

Postman
28. http://172.28.129.160:8888/copyupdate/ (post, ensure authentication is as
demonstrated in security demo)
  body = {"bucket": "ditto-testbucket1"} to copy across new file and update old in sub directory

Browser
29. http://172.28.129.160:9000/ to show files exist, should be all new files and no archive files

Bash
30. `ls -A` show archive file still there
31. `cat .ditto_archived` show new file there, old entry untouched
32. `cd some_files`
33. `ls -A`
34. `cat .ditto_archived` Show file updated
