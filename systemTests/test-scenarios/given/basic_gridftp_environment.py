import subprocess
import os
import io
import sys
import time


class BasicGridftpEnvironment:
	def __init__(self, context):
		self._context = context

	def is_running(self):
		os.system("globus-gridftp-server -control-interface 127.0.0.1 -aa -p 5000 &")

