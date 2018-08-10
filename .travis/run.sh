#!/bin/bash

set -e
set -x

if [[ "$(uname -s)" == 'Darwin' ]]; then
    if which pyenv > /dev/null; then
        eval "$(pyenv init -)"
    fi
    pyenv activate conan
fi

if [[ "${TRAVIS_EVENT_TYPE}" != "cron" ]]; then
    python setup.py sdist
    pushd tests
    pytest -v -s --cov=bincrafters_remove_outdated.bincrafters_remove_outdated
    mv .coverage ..
    popd

    python setup.py install
    bincrafters-remove-outdated --version
else

    python setup.py install
    conan remote add bincrafters ${REMOTE}
    conan user -r bincrafters -p ${PASSWORD} ${LOGIN_USERNAME}
    bincrafters-remove-outdated bincrafters --ignore --yes
fi
