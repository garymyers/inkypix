#!/bin/bash

# run as SUDO
sudo cp ./scripts/inkyweb.service /etc/systemd/system/
sudo cp ./scripts/inkypix.service /etc/systemd/system/
sudo systemctl daemon-reload

sudo systemctl enable inkypix.service
sudo systemctl enable inkyweb.service
