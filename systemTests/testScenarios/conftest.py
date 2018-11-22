import os
import shutil
import pytest


@pytest.fixture(scope="session", autouse=True)
def set_up_system_test_environment():
    print("Setting up a system test environment")

    home = '/home/vagrant'
    execution_space = os.path.join(home, 'systemTests', 'execution_space')
    copied_src_path = os.path.join(execution_space, 'ditto_web_api', 'DittoWebApi')
    logs_path = os.path.join(execution_space, 'logs')
    local_data_path = os.path.join(execution_space, 'data')

    # Clear out the old programs
    if os.path.isdir(copied_src_path):
        shutil.rmtree(copied_src_path)
    if os.path.isdir(logs_path):
        shutil.rmtree(logs_path)
    if os.path.isdir(local_data_path):
        shutil.rmtree(local_data_path)

    # Copy the web API source code
    shutil.copytree(os.path.join(home, 'ditto_web_api', 'DittoWebApi'), copied_src_path)

    # Create the logging and local data directories
    os.makedirs(logs_path)
    os.makedirs(local_data_path)
