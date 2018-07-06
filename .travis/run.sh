#!/bin/bash

set -e
set -x

if [[ "$(uname -s)" == 'Darwin' ]]; then
    if which pyenv > /dev/null; then
        eval "$(pyenv init -)"
    fi
    pyenv activate conan
fi

if [[ "${TRAVIS_EVENT_TYPE}" != 'cron' ]]; then
    python setup.py sdist
    pushd tests
    pytest -v -s --cov=bincrafters_remove_outdated.bincrafters_remove_outdated
    mv .coverage ..
    popd

else

    python setup.py install
    conan remote add bincrafters ${CONAN_UPLOAD}
    conan user -r bincrafters -p ${CONAN_PASSWORD} ${CONAN_LOGIN_USERNAME}
    bincrafters-remove-outdated bincrafters --ignore --yes
fi