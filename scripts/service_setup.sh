#!/bin/bash

# run as SUDO
cp ./scripts/inkyweb.service /etc/systemd/system/
cp ./scripts/inkypix.service /etc/systemd/system/
systemctl daemon-reload

systemctl enable inkypix.service
systemctl enable inkyweb.service
