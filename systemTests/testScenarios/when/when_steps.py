from testScenarios.when.copy_dir_when_steps import CopyDirWhenSteps
from testScenarios.when.copy_new_when_steps import CopyNewWhenSteps
from testScenarios.when.copy_update_when_steps import CopyUpdateWhenSteps
from testScenarios.when.create_bucket_when_steps import CreateBucketWhenSteps
from testScenarios.when.delete_file_when_steps import DeleteFileWhenSteps
from testScenarios.when.list_present_when_steps import ListPresentWhenSteps


class WhenSteps(CopyDirWhenSteps,
                CopyNewWhenSteps,
                CopyUpdateWhenSteps,
                CreateBucketWhenSteps,
                DeleteFileWhenSteps,
                ListPresentWhenSteps):

    def environment_is_stopped(self):
        self._context.shut_down_ditto_api()
