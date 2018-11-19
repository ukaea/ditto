# Web App copies new files to S3 interface and updates those that have changed

## Stories covered
#34 - create a bucket
#29 - delete a file
#5 transfer only new files
#6 transfer new files and update those that have changed



Bash
1. `vagrant up`
2. `vagrant ssh`
3. `systemctl status minio`
  - `sudo systemctl start minio`
4. `cd ditto_web_api`
5. `source venv/bin/activate`
6. `cd data`
7. `mkdir some_files`
  - `cd some_files`
8. `echo "This is a test file \n" >> test_file_1`
9. `cd ../..`
10. `PYTHONPATH=./ python DittoWebApi/main.py`

Browser
11. http://172.28.129.160:9000/ to show what files exist if anything present delete all files and buckets to start from empty

### Story #34 Create a bucket ###

Postman
12. http://172.28.129.160:8888/createbucket/ (post)
  body = {"bucket": "ditto-testbucket1"}

Browser
13. http://172.28.129.160:9000/ Show new bucket

Postman
14. http://172.28.129.160:8888/createbucket/  (post)
  body = {"bucket": "testbucket1"} to show warning when incorrect bucket name

15. http://172.28.129.160:8888/listpresent/ (post) to show an empty bucket
  body = {"bucket": "ditto-testbucket1"}

16. http://172.28.129.160:8888/copydir/ (post)
  body = {"bucket": "ditto-testbucket1", "directory": "some_files"} to copy across files from local

17. http://172.28.129.160:8888/listpresent/ (post) to show the copied files
  body = {"bucket": "ditto-testbucket1"}

### STORY #5 transfer only new files ###
18. http://172.28.129.160:8888/copynew/ (post)
    body = {"bucket": "ditto-testbucket1", "directory": "some_files"}
    Show info when no new files to transfer

BASH (new terminal already at data directory)
19. `cd some_files`
20. `cat test_file_1.txt` show content of a present file
21. `echo "a new line" >> "test_file_1.txt"` update a file already present
22. `cat test_file_1.txt` show update
23. `mkdir some_new_files` create a new subdir and new file
24. `cd some_new_files`
25. `echo "Hello World" >> a_new_file.txt` Create a new file

Postman
26. http://172.28.129.160:8888/copynew/ (post)
    body = {"bucket": "ditto-testbucket1", "directory": "some_files"}
    To show success of new file transferred but updated skipped

27. http://172.28.129.160:8888/listpresent/ (post)
    body = {"bucket": "ditto-testbucket1", "directory": "some_files"}
    To show new file in bucket

Browser
28. http://172.28.129.160:9000/ Show new file in browser

### Story #6 transfer new and update ###
Bash
29. `echo "Hello world again" >> another_new_file.txt` create another new file

Postman
30. http://172.28.129.160:8888/copyupdate/ (post)
    body = {"bucket": "ditto-testbucket1", "directory": "some_files"}
    To show copy and update file  

31. http://172.28.129.160:8888/listpresent/ (post)
    body = {"bucket": "ditto-testbucket1", "directory": "some_files"}
    To show new and updated files

### Story #29 delete a file ###
Postman
32. http://172.28.129.160:8888/deletefile/ (delete)
    body = {"bucket": "ditto-testbucket1", "file": "some_files/some_new_files/a_new_file.txt"}
    To show deleting a file

33. http://172.28.129.160:8888/listpresent/ (post)
    body = {"bucket": "ditto-testbucket1", "directory": "some_files"}
    To show file deleted
