# Accident Crime Detection on Jetson Nano

Install the accident crime detection on  Jetson Nano.

## Requirements

* Jetson Nano.
* Uses JetPack 4.6.1 or later.

## Installation

### Install Respeaker 4 Mic Array Codec

1. Prepare a PC/VM with supported Ubuntu version as specified in [SDK Manager](https://developer.nvidia.com/sdk-manager).
2. Download and install SDK Manager.
```bash
sudo apt install -y libgconf-2-4 libcanberra-gtk-module
sudo dpkg -i sdkmanager_1.4.0-7363_amd64.deb
```
3. Choose JetPack version (4.6.1 or higher) and its SDK components.
```bash
sdkmanager --cli --query interactive
```
4. Download JetPack and its SDK components by running the Launch command obtained from step 3.
5. Choose L4T sources version (32.7.1 or higher) matched with your JetPack version in [Jetson Download Center](https://developer.nvidia.com/embedded/downloads#?tx=$product,jetson_nano).
6. Open the L4T Development Guide of your L4T sources version, go to the Kernel Customization section and follow the **Manually Download and Expanding Kernel Sources** guide to download the kernel source and extract it.
7. Patch the kernel following steps provided by [AshaTalambedu](https://github.com/AshaTalambedu/seeed-voicecard/blob/jetson-respeaker-4mic-array-compatible/README-jetson-4mic-circular-array-support) or extract Update.zip and replace file in paths.
8. Follow the **Building the NVIDIA Kernel** guide in the Kernel Customization section in L4T Development Guide to build the kernel and apply it to your downloaded JetPack OS.
9. Build the image by running
```bash
cd ~/nvidia/nvidia_sdk/JetPack_4.6.1_Linux_JETSON_NANO_TARGETS/Linux_for_Tegra/
sudo ./apply_binaries.sh -r rootfs
sudo ./tools/jetson-disk-image-creator.sh -o $HOME/sdcard.img -b jetson-nano -r <Jetson_nano_type_code>
```
with <Jetson_nano_type_code> varies from:
* **100** for Jetson Nano A01
* **200** for Jetson Nano A02
* **300** for Jetson Nano B01
10. Flash the SD card with [Balena Etcher](https://www.balena.io/etcher/).
11. Rerun the SDK Manager with same command from step 4 and install the SDK Components through USB/Ethernet. (Try using UI mode if installation failed).
12. Enable the Jetson IO for Respeaker 4 Mic Array by running
```bash
sudo /opt/nvidia/jetson-io/jetson-io.py
```
```
Configure Jetson 40pin Header > Configure for compatible hardware > Respeaker 4 Mic Array
```
13. Reboot.

You can check the result by using Audacity with input default with 4 channels.

### Increase Swap Size

```bash
git clone https://github.com/JetsonHacksNano/resizeSwapMemory.git
cd resizeSwapMemory
./setSwapMemorySize.sh -g 4
```

### Install Tensorflow 2.7

```bash
sudo ln -s /usr/include/locale.h /usr/include/xlocale.h
sudo apt-get install libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev zip libjpeg8-dev liblapack-dev libblas-dev gfortran python3-dev -y
sudo apt-get install python3-pip -y
python3 -m pip install --upgrade pip
sudo python3 -m pip install testresources setuptools virtualenv
python3 -m pip install future mock keras_preprocessing keras_applications gast protobuf pybind11 cython pkgconfig packaging h5py
virtualenv acd
source acd/bin/activate
python3 -m pip install grpcio absl-py py-cpuinfo psutil portpicker six mock requests gast h5py astor termcolor protobuf keras-applications keras-preprocessing wrapt google-pasta setuptools testresources
python3 -m pip install --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v461 tensorflow==2.7.0+nv22.1
```

### Install librosa

```bash
sudo apt-get install llvm-9 llvm-9-dev
export LLVM_CONFIG=/usr/bin/llvm-config-9
sudo apt-get install portaudio19-dev python-all-dev python3-all-dev
sudo mv /usr/include/tbb/tbb.h /usr/include/tbb/tbb.bak
python3 -m pip install librosa
sudo mv /usr/include/tbb/tbb.bak /usr/include/tbb/tbb.h
```

### Install Accident Crime Detection prerequisites
```bash
python3 -m pip install -r install2jetsonnano/requirements.txt
```

### Disable Serial Console and add user to dialout group
```bash
sudo systemctl stop nvgetty
sudo systemctl disable nvgetty
sudo udevadm trigger
sudo usermod -aG dialout <user>
sudo reboot
```