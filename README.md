# inkypix
Inky Impression 7.3" eInk Picture Frame slideshow player for Raspberry PI with a web-UI for image management.


# SETUP

## FIRST STEP
Clone this repository to your Raspberry PI.

## HARDWARE
Run the `source scripts/setup.py`. This does the following things:
   - setup the hardware configuration for the INKY
   - add bonjour support to go to the <hostname>.local in case you don't remember the IP address.

Then you need to manually add the following line to `/boot/firmware/config.txt` if you see the error message `Chip Select: (line 8, GPIO8) currently claimed by spi0 CS0`.
`dtoverlay=spi0-0cs`

*Note: it may also be `dtoverlay=spi0-cs0` but need to double check that. Or maybe just a reboot.* 

## SOFTWARE
After the hardware changes are setup, cd into this root of this repository that you cloned. 

### Install requirements
`pip install -r requirements.txt`

### Now run the other scripts
Run `source scripts\service_setup.sh` to setup the linux services. It does the following:
   - copy the slideshow service `inkypix.service` to the `/etc/systemd/system/` directory. 
   - copy the WebUI service `inkyweb.service` to the `/etc/systemd/system/` directory.
   - start the services.
     
---
Note: took inspiration and some bash scripting from PiInk (https://github.com/tlstommy/PiInk)
