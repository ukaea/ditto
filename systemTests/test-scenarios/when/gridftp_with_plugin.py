import subprocess
import os
import signal
import io
import sys
import time
import psutil


class GridftpWithPlugin:
  def __init__(self, context):
    self._context = context

  def is_shut_down(self):
    self._context.shut_down_gridftp()


      