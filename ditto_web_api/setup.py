from DittoWebApi import version
from setuptools import setup, find_packages

setup(
    # Application name:
    name='DittoWebApi',

    # Version number (initial):
    version=version.__version__,

    # Application author details:
    author="DITTO team",
    author_email="some@email",

    # Packages
    packages=find_packages(),
    package_data={
        # Include the configuration file in the resulting wheel
        '': ['example_configuration.ini', 'example_bucket_settings.ini'],
    },

    description="Data replication tool for UKAEA-to-STFC storage.",

    # Dependent packages (distributions)
    install_requires=[
        "Tornado-JSON",
        "requests"
    ],

    # entry points
    entry_points={
        'console_scripts': [
            'ditto_server = DittoWebApi.main'
        ]
    },
)
