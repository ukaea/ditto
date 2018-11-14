import os
import shutil
import pytest

@pytest.fixture(scope="session", autouse=True)
def set_up_system_test_environment(request):
    print("setting up a system test environment")

    # clear out the old programs
    execution_space = '../execution_space'
    if (os.path.isdir(execution_space)):
        shutil.rmtree(execution_space)

    os.makedirs(execution_space)

    os.makedirs(execution_space + '/logs')
    os.makedirs(execution_space + '/testing_area/src')
    os.makedirs(execution_space + '/testing_area/staging')
    os.makedirs(execution_space + '/testing_area/target')

