from testScenarios.context import BaseSystemTest


class TestTemplate(BaseSystemTest):
    def test_template(self):
        self.given.given_steps()
        self.when.when_steps()
        self.then.then_steps()
