import os
import shutil
import pytest


@pytest.fixture(scope="session", autouse=True)
def set_up_system_test_environment():
    print("Setting up a system test environment")

    home = '/home/vagrant'

    # Clear out the old programs
    execution_space = os.path.join(home, 'execution_space')
    if os.path.isdir(execution_space):
        shutil.rmtree(execution_space)

    # Create the execution space
    os.makedirs(execution_space)

    # Copy the web API source code
    shutil.copytree(
        os.path.join(home, 'ditto_web_api', 'DittoWebApi'),
        os.path.join(execution_space, 'ditto_web_api', 'DittoWebApi')
    )

    # Create the logging and local data directories
    os.makedirs(os.path.join(execution_space, 'logs'))
    os.makedirs(os.path.join(execution_space, 'data'))
