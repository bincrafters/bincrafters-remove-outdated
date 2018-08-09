[![Build Status: Linux and Macos](https://travis-ci.org/bincrafters/bincrafters-remove-outdated.svg?branch=master)](https://travis-ci.org/bincrafters/bincrafters-remove-outdated)
[![Build status: Windows](https://ci.appveyor.com/api/projects/status/github/bincrafters/bincrafters-remove-outdated?svg=true)](https://ci.appveyor.com/project/bincrafters/bincrafters-remove-outdated)
[![codecov](https://codecov.io/gh/bincrafters/bincrafters-remove-outdated/branch/master/graph/badge.svg)](https://codecov.io/gh/bincrafters/bincrafters-remove-outdated)
[![Pypi Download](https://img.shields.io/badge/download-pypi-blue.svg)](https://pypi.python.org/pypi/bincrafters-remove-outdated)

# Conan Remove Outdated

## A script to remove all outdated packages from remote

![logo](logo.png)

#### Requirements
  * Python 3

#### INSTALL
To install by pip is just one step

##### Local
If you want to install by local copy

    pip install .

##### Remote
Or if you want to download our pip package

    pip install bincrafters_remove_outdated

#### RUN
To remove **ALL** outdated packages on Bincrafters https://api.bintray.com/conan/bincrafters/public-conan

    $ bincrafters-remove-outdated bincrafters


##### Testing and Development
To install extra packages required to test

    pip install .[test]


#### TESTING
To run all unit test + code coverage, just execute:

    pip install -r bincrafters_remove_outdated/requirements_test.txt
    cd tests
    pytest -v --cov=bincrafters_remove_outdated


#### REQUIREMENTS and DEVELOPMENT
To develop or run conan remove outdated

    pip install -r bincrafters_remove_outdated/requirements.txt


#### UPLOAD
There are two ways to upload this project.

##### Travis CI
After to create a new tag, the package will be uploaded automatically to Pypi.  
Both username and password (encrypted) are in travis file.  
Only one job (python 2.7) will upload, the second one will be skipped.


##### Command line
To upload this package on pypi (legacy mode):

    pip install twine
    python setup.py sdist
    twine upload dist/*


#### LICENSE
[MIT](LICENSE.md)
