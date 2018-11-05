import subprocess
import os
import io
import sys
import time


class GridftpWithPlugin:
  def __init__(self, context):
    self._context=context

  def is_started(self):
    self._context.gridftp_process = subprocess.Popen(['../run-gridftp-server.sh'], 
    stdout=self._context.console_logger.stdout_log_writer,
    stderr=self._context.console_logger.stderr_log_writer,
    shell=True, cwd=r'/home/vagrant/src/build')

    time.sleep(2) # let the server start