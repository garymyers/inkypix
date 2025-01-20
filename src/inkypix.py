#!/usr/bin/env python3

import pathlib
import sys
import os
import random
from PIL import Image
from inky.auto import auto
import time
from subprocess import check_call
from gpiozero import Button

# Define the directory where images will be stored
CONFIG_DIR = "./config"
if not os.path.exists(CONFIG_DIR):
    os.makedirs(CONFIG_DIR)
REFRESH_INTERVAL_FILE = f"{CONFIG_DIR}/refresh_interval.txt"

# extensions to load
EXTENSIONS = ('*.png', '*.jpg')

# Gpio pins for each button (from top to bottom)
BUTTONS = [5, 6, 16, 24]

# These correspond to buttons A, B, C and D respectively
LABELS = ['A', 'B', 'C', 'D']

class InkyPix:

    def __init__(self):
        self.inky = auto()
        # self.add_buttons()
        self.resolution = self.inky.resolution
        self.picture_directory = None
        self.orientation = 0  # portrait
        self.saturation = 0.5
        self.interval = None
        self.images = []
        self.last = None
        self.add_buttons()

    def get_refresh_interval(self):
        if self.interval: 
            return self.interval
        if os.path.exists(REFRESH_INTERVAL_FILE):
            with open(REFRESH_INTERVAL_FILE, "r") as f:
                print("openeing file")
                return int(f.read().strip())
        else:
            return 2 # Default to 2 minutes

    def transform_image(self, image_path):
        # Open the image
        with Image.open(image_path) as img:
            # Check orientation and rotate if necessary
            width, height = img.size
            aspect_ratio = width / height
            
            if width < height:  # Portrait orientation
                img = img.rotate(90, expand=True)
                width, height = height, width
            
            # Calculate the target aspect ratio
            target_aspect_ratio = self.resolution[0] / self.resolution[1]
            
            # Determine crop dimensions to match the target aspect ratio
            if aspect_ratio > target_aspect_ratio:
                # Crop width-wise
                new_width = int(height * target_aspect_ratio)
                left = (width - new_width) // 2
                img = img.crop((left, 0, left + new_width, height))
            elif aspect_ratio < target_aspect_ratio:
                # Crop height-wise
                new_height = int(width / target_aspect_ratio)
                top = (height - new_height) // 2
                img = img.crop((0, top, width, top + new_height))
            
            # Resize the image to the specified resolution
            img = img.resize(self.resolution, Image.Resampling.BICUBIC)
        return img


    def show_image(self, fq_name):
        print(f"showing {fq_name}")
        self.last = fq_name
        img = self.transform_image(fq_name)
        self.inky.set_image(img, saturation=self.saturation)
        self.inky.set_border(self.inky.BLACK)
        self.inky.show()

    def show_next_image(self):
        if not self.images:
            print("No images found in the directory.")
            return
                
        # Select a random image from the list
        selected_image = random.choice(self.images)
        if len(self.images) > 1:
            while selected_image == self.last:
                selected_image = random.choice(self.images)
        image = self.show_image(selected_image)
        ri = self.get_refresh_interval() * 60
        print(f"Sleeping for {ri} seconds")
        time.sleep(ri)
        self.slide_show() # reload

        # Schedule the next image update after a delay (e.g., 1 second)
        # self.sleep
        # self.root.after(self.interval, self.show_next_image)

    def slide_show(self):
        self.images = []
        
        # Load images from the directory
        for filename in os.listdir(self.picture_directory):
            if filename.lower().endswith(('.jpg', '.png')):
                file_path = os.path.join(self.picture_directory, filename)
                self.images.append(file_path)

        self.show_next_image()

    # "handle_button" will be called every time a button is pressed
    # It receives one argument: the associated input pin.
    def handle_button(self, button):
        label = LABELS[BUTTONS.index(button.pin.number)]
        print(f"PRESSED {button.pin.number} / {label}")
        if label == 'A':
            self.show_next_image()
        elif label == 'D':
            check_call(['sudo', 'poweroff'])
            #subprocess.run("sudo shutdown --poweroff now", shell=True)
    
    def add_buttons(self):
        print('Adding button hooks')
        for pin in BUTTONS:
            button = Button(pin=pin, hold_time=2)
            button.when_held = self.handle_button



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser("inkypix - runs the inkypix program")
    parser.add_argument("--saturation", "-s", type=float, default=0.5, help="Colour palette saturation")
    parser.add_argument("--orientation", "-o", type=int, default=0, help="0 for portrait; 1 for landscape")
    parser.add_argument("--folder", "-f", type=str, default="./images", help="Image folder")
    parser.add_argument("--interval", "-i",  type=int, help="number of minutes for each interval")

    args = parser.parse_args()

    if not args.folder:
        print(f"""Usage:
        {sys.argv[0]} --folder ./images (--saturation 0.5)""")
        sys.exit(1)

    interval = None

    i = InkyPix()
    i.saturation = args.saturation
    i.picture_directory = str(args.folder).strip()
    i.orientation = args.orientation
    if args.interval:
        i.interval = args.interval
    i.slide_show()
