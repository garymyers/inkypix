# inkypix
Inky Impression 7.3" eInk Picture Frame slideshow player for Raspberry PI with a web-UI for image management.


# Setup
Run the `source scripts/setup.py` and then you need to manually add the following line to `/boot/firmware/config.txt` if you see the error message `Chip Select: (line 8, GPIO8) currently claimed by spi0 CS0`.
`dtoverlay=spi0-0cs`

*Note: it may also be `dtoverlay=spi0-cs0` but need to double check that.* 

---
Note: took inspiration and some bash scripting from PiInk (https://github.com/tlstommy/PiInk)
