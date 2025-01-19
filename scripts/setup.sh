#!/bin/bash

#enable spi
sudo sed -i 's/^dtparam=spi=.*/dtparam=spi=on/' /boot/config.txt
sudo sed -i 's/^#dtparam=spi=.*/dtparam=spi=on/' /boot/config.txt
sudo raspi-config nonint do_spi 0
print_success "SPI Interface has been enabled."
#enable i2c
sudo sed -i 's/^dtparam=i2c_arm=.*/dtparam=i2c_arm=on/' /boot/config.txt
sudo sed -i 's/^#dtparam=i2c_arm=.*/dtparam=i2c_arm=on/' /boot/config.txt
sudo raspi-config nonint do_i2c 0
print_success "I2C Interface has been enabled.\n"

#set up Bonjour
print_header "Setting up Bonjour so you can find at <hostname>.local, where hostname is:"
cat /etc/hostname

sudo apt-get install -y avahi-daemon > /dev/null &
show_loader "   [1/2] Installing avahi-daemon."

sudo apt-get install -y netatalk > /dev/null &
show_loader "   [2/2] Installing netatalk.    "

print_success "Bonjour set up!\n"
