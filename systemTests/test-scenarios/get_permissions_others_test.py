import unittest
import time

import context

class GetPermissionsOthers(context.BaseSystemTest):                      #class would need a "Test" prefix if it did not inhrit the __init__ method
  def test_Get_permissions_others_1(self):                   #this needs the "test_" prefix to get picked up by pytest
    self.given.gridftp_plugin_server().is_started()
    self.given.a_file_in_src().has_other_permissions(1)
    self.given.an_ftp_client_is_connected()
    
    self.when.get_permissions_called_for_file()

    self.then.logs_get_permissions()