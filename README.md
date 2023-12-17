# zp-client


## Deployment

### Create image

The easiest way to setup a client is to use the provided image for a raspberry pi 4. In this section we describe how to setup your own client.

**Prerequisites**

- Raspberry Pi 4
- SD-Card
- Internet connection
- RaspberryPi Imager [https://github.com/raspberrypi/rpi-imager](https://github.com/raspberrypi/rpi-imager)

**prepare sd card and install operating system**

- use RaspberryPi Imager to install the latest version of RaspberryPi OS
  - in Settings, you can specify various configuration parameter such as keys for ssh access or WiFi. Leave the host name empty, since it will be defined at boot time of the pi and will include the mac adress of your device
- put the SD-Card into your RaspberryPi and boot it up
- it's a good practice to update all software packages, so login to your raspberrypi either via SSH or via keyboard if it is already connected to a monitor
- open a terminal and execute: `$sudo apt udpate` and then `$sudo apt upgrade`

**deploy zp-client**

We have defined several directories where we store project relevant files and packages, which we will use throughout this documentation.

- create a folder `zp-client` in `/opt`
  - `$sudo mkdir /opt/zp-client`
  - change folder permissions: `sudo chown pi:pi /opt/zp-client`
- deploy backend scripts
  - create folder `backend`: `$mkdir /opt/zp-client/backend`
  - create folder `releases`: `$mkdir /opt/zp-client/backend/releeases`
  - copy the latest release of zp-client to releases folder
