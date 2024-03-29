# Accident Crime Detection on Raspberry

Install the accident crime detection on Raspberry Pi.

## Requirements

* Raspberry Pi 4+.
* Uses Raspbian buster arm64 or later.

## Installation

### Install mic driver

If you use [ReSpeaker Mic](https://wiki.seeedstudio.com/ReSpeaker/) run the following script.

```bash
sudo apt-get update
git clone https://github.com/respeaker/seeed-voicecard.git
cd seeed-voicecard
sudo ./install_arm64.sh
sudo reboot
```

**As for now ReSpeaker Mic only supported on Raspbian Buster or older.**

Check the installation using following script. Installation succeed if you see your ReSpeaker Device.

```bash
arecord -L
```

### Install tensorflow 2.7

Run this script using bash.

```bash
./download_tensorflow-2.7.0-cp37-none-linux_aarch64_numpy1214.sh
./install_tensorflow_2.7.0_prerequisites.sh
./install_tensorflow_2.7.0.sh
```

**Tensorflow 2.7 cannot be installed on Raspberry older than Raspberry Pi 4 with OS older than Raspbian Buster arm64.**

### Install Accident Crime Detection prerequisites
```bash
sudo apt-get install portaudio19-dev
sudo apt-get install python-pyaudio
pip3 install -r requirements.txt
```