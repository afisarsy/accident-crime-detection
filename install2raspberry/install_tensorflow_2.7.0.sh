#!/bin/bash

TFVER=2.7.0
PYVER=37

ARCH=`python -c 'import platform; print(platform.machine())'`
echo CPU ARCH: ${ARCH}

pip3 install \
--no-cache-dir \
tensorflow-${TFVER}-cp${PYVER}-none-linux_${ARCH}.whl
