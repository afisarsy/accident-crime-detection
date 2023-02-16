#!/bin/bash

sudo apt-get update
sudo apt-get install -y \
    libhdf5-dev libc-ares-dev libeigen3-dev gcc gfortran \
    libgfortran5 libatlas3-base libatlas-base-dev \
    libopenblas-dev libopenblas-base libblas-dev \
    liblapack-dev cython3 libatlas-base-dev openmpi-bin \
    libopenmpi-dev python3-dev
pip3 install pip --upgrade
pip3 install keras_applications --no-deps
pip3 install keras_preprocessing --no-deps
pip3 install numpy
pip3 install h5py
pip3 install pybind11
pip3 install -U six wheel mock
pip3 uninstall tensorflow
