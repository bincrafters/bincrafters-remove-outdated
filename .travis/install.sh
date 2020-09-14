#!/bin/bash

set -e
set -x

if [[ "$(uname -s)" == 'Darwin' ]]; then
    rm -rf /usr/local/opt/pyenv;
    rm /usr/local/bin/pyenv;
    rm /usr/local/bin/pyenv-install;
    rm /usr/local/bin/pyenv-uninstall;
    ln -s /usr/local/opt/pyenv/libexec/pyenv /usr/local/bin/pyenv;
    unset PYENV_ROOT;
    curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash;
    export PATH="$HOME/.pyenv/bin:$PATH";
    eval "$(pyenv init -)";
    eval "$(pyenv virtualenv-init -)";
    pyenv --version;
    pyenv install 3.7.6;
    pyenv virtualenv 3.7.6 conan;
    pyenv rehash;
    pyenv activate conan;
fi

pip install codecov
pip install -e .[test]
