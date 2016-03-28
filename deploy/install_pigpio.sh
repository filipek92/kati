#!/usr/bin/env bash

# must run as root!

set -x

pkill pigpiod
rm master.zip
rm -rf pigpio-master
wget https://github.com/joan2937/pigpio/archive/master.zip
unzip master.zip
cd pigpio-master
make -j4
make install
