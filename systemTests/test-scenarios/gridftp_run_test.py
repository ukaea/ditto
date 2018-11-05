# import unittest
# import time

# import context

# class GridftpRun(context.BaseSystemTest):                      #class would need a "Test" prefix if it did not inhrit the __init__ method
#     def test_Gridftp_basic_setup_runs(self):                   #this needs the "test_" prefix to get picked up by pytest
#         self.given.simple_test_file_is_setup()
#         self.given.gridftp_basic_server().is_running()
        
#         self.when.target_folder_listed('/')
#         self.when.simple_file_is_copied()

#         self.then.simple_test_file_is_transferred()
#         self.then.contents_of_copied_file_unchanged()
#         #delete the files created and copied across (if not already done in teardown)