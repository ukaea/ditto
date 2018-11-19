from .log_file_steps import LogFileSteps


class ThenSteps:
    def __init__(self, context):
        self._context = context
        self.console_output = LogFileSteps(context, 'console-stdout.log')
        self.console_error = LogFileSteps(context, 'console-stderr.log')
        self.ditto_api_log = LogFileSteps(context, 'ditto_api_server.log')

    def simple_test_file_is_transferred(self):
        # example step that will check that files are transferred to the correct output directory
        assert 1 == 0

    def contents_of_copied_file_unchanged(self):
        # example step that will check that a file copied across has the same contents as the input file
        assert 1 == 0
