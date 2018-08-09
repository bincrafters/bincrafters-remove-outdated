[![Build Status: Linux and Macos](https://travis-ci.org/bincrafters/bincrafters-remove-outdated.svg?branch=master)](https://travis-ci.org/bincrafters/bincrafters-remove-outdated)
[![Build status: Windows](https://ci.appveyor.com/api/projects/status/github/bincrafters/bincrafters-remove-outdated?svg=true)](https://ci.appveyor.com/project/bincrafters/bincrafters-remove-outdated)
[![codecov](https://codecov.io/gh/bincrafters/bincrafters-remove-outdated/branch/master/graph/badge.svg)](https://codecov.io/gh/bincrafters/bincrafters-remove-outdated)
[![Pypi Download](https://img.shields.io/badge/download-pypi-blue.svg)](https://pypi.python.org/pypi/bincrafters-remove-outdated)

# Conan Remove Outdated

## A script to remove all outdated packages from remote

![logo](logo.png)

#### Requirements
  * Python 2.7 or 3
  * the [Conan](https://conan.io) client

#### INSTALL
To install by pip is just one step

##### Local
If you want to install by local copy

    pip install .

##### Remote
Or if you want to download our pip package

    pip install bincrafters_remove_outdated

#### RUN

- Make sure your remote is properly listed on Conan remote list (`conan remote list`)
- Make sure your Conan client is logged in (`conan user`) the repository you want to clean. Then:

    $ bincrafters-remove-outdated <repository>

To remove **ALL** outdated packages on Bincrafters https://api.bintray.com/conan/bincrafters/public-conan

    $ bincrafters-remove-outdated bincrafters

#### USAGE

```
bincrafters-remove-outdated [-h] [--yes] [--ignore] [--dry-run] [--pattern PATTERN] [--version] remote

Conan Remove Outdated

positional arguments:
  remote         Conan remote to be cleaned e.g conan-center

optional arguments:
  -h, --help     show this help message and exit
  --yes, -y      Do not ask for confirmation
  --ignore, -i   Ignore errors receive from remote
  --dry-run, -d  Check which packages will be removed only
  --pattern PATTERN, -p PATTERN Pattern to filter package name to be removed. e.g Boost/*
  --version, -v  show program's version number and exit
```

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
After to create a new tag, the package will be uploaded automatically to PyPi.  
Both username and password (encrypted) are in travis file.  
Only one job (Python 3.6) will upload, the others will be skipped.


##### Command line
To upload this package on pypi (legacy mode):

    pip install twine
    python setup.py sdist
    twine upload dist/*


#### LICENSE
[MIT](LICENSE.md)
