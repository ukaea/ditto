# Web App copies new files to S3 interface and updates those that have changed

## Stories covered

Bash
1. `vagrant up`
2. `vagrant ssh`
3. `systemctl status minio`
  - `sudo systemctl start minio`
4. `cd ditto_web_api`
5. `source venv/bin/activate`
6. `PYTHONPATH=./ python DittoWebApi/main.py`

Browser
7. http://172.28.129.160:9000/ to show what files exist

Postman
8. http://172.28.129.160:8888/createbucket/ (post)
  body = {"bucket": "ditto-testbucket1"}

Browser
9. http://172.28.129.160:9000/ Show new bucket

Postman
10. http://172.28.129.160:8888/createbucket/  (post)
  body = {"bucket": "testbucket1"} to show error when incorrect bucket name

11. http://172.28.129.160:8888/listpresent/ (post) to show an empty bucket
  body = {"bucket": "ditto-testbucket1"}
12. http://172.28.129.160:8888/copydir/ (post)
  body = {"bucket": "ditto-testbucket1", "directory": "some_files"}

13. http://172.28.129.160:8888/listpresent/ (post)
  body = {"bucket": "ditto-testbucket1"}

14. http://172.28.129.160:8888/copynew/ (post)
    body = {"bucket": "ditto-testbucket1", "directory": "some_files"}
    Show error when no new files

BASH (new terminal already at data directory)
15. `cd some_files`
16. `cat test_file_1.txt`
17. `echo "a new line" >> "test_file_1.txt"`
18. `cat test_file_1.txt`
19. `mkdir some_new_files`
20. `cd some_new_files`
21. `echo "Hello World" >> a_new_file.txt`

Postman
22. http://172.28.129.160:8888/copynew/ (post)
    body = {"bucket": "ditto-testbucket1", "directory": "some_files"}
    To show success of new file transferred but updated skipped

23. http://172.28.129.160:8888/listpresent/ (post)
    body = {"bucket": "ditto-testbucket1", "directory": "some_files"}
    To show new file in bucket

24. http://172.28.129.160:8888/deletefile/ (delete)
    body = {"bucket": "ditto-testbucket1", "file": "some_files/some_new_files/a_new_file.txt"}
    To show deleting a file

25. http://172.28.129.160:8888/listpresent/ (post)
    body = {"bucket": "ditto-testbucket1", "directory": "some_files"}
    To show file deleted

26. http://172.28.129.160:8888/copyupdate/ (post)
    body = {"bucket": "ditto-testbucket1", "directory": "some_files"}
    To show copy and update file  

27. http://172.28.129.160:8888/listpresent/ (post)
    body = {"bucket": "ditto-testbucket1", "directory": "some_files"}
    To show new and updated files
