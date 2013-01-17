#!/bin/bash

check() {
    if [[ "$?" -ne "0" ]]
    then
        echo "$0 FAILED"
        exit 1
    fi
}

virtualenv python_env
. python_env/bin/activate

pip install numpy==1.6.2
check
pip install wsgiref==0.1.2
check
