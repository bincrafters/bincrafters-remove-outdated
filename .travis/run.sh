#!/bin/bash

set -e
set -x

if [[ "$(uname -s)" == 'Darwin' ]]; then
    export PATH="$HOME/.pyenv/bin:$PATH";
    eval "$(pyenv init -)";
    eval "$(pyenv virtualenv-init -)";
    pyenv activate conan
fi

if [[ "${TRAVIS_EVENT_TYPE}" != "cron" ]]; then
    python setup.py sdist
    tox -v

    python setup.py install
    bincrafters-remove-outdated --version
else

    python setup.py install
    conan remote add bincrafters ${REMOTE}
    conan user -r bincrafters -p ${PASSWORD} ${LOGIN_USERNAME}
    bincrafters-remove-outdated bincrafters --ignore --yes
fi
