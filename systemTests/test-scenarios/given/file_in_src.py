import subprocess
import os
import io
import sys
import time


class FileInSrc:
  def __init__(self, context):
    self._context=context

  def has_other_permissions(self, permission_set):
    os.chmod(os.path.join(self._context.execution_folder_path, 'testing_area/src', 'testPermissions.txt'), (0o770+permission_set))