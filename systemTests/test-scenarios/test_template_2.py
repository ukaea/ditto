import unittest
import time

import context

class TestTemplate2(context.BaseSystemTest):                      #class would need a "Test" prefix if it did not inhrit the __init__ method
  def test_template_2(self):                   #this needs the "test_" prefix to get picked up by pytest
    self.given.given_steps()

    self.when.when_steps()

    self.then.then_steps()
