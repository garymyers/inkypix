#!/usr/bin/env python3

import pathlib
import sys
import os
import random
from PIL import Image
from inky.auto import auto
import time

class InkyPix:

    def __init__(self):
        self.inky = auto()
        self.resolution = self.inky.resolution
        self.picture_directory = None
        self.orientation = 0  # portrait
        self.saturation = 0.5
        self.interval = 2
        self.images = []
        self.last = None

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
        print(f"Sleeping for {self.interval} seconds")
        time.sleep(self.interval)
        self.show_next_image()

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
        


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser("inkypix - runs the inkypix program")
    parser.add_argument("--saturation", "-s", type=float, default=0.5, help="Colour palette saturation")
    parser.add_argument("--orientation", "-o", type=int, default=0, help="0 for portrait; 1 for landscape")
    parser.add_argument("--folder", "-f", type=str, default="./images", help="Image folder")
    parser.add_argument("--interval", "-i",  type=int, default=2, help="number of minutes for each interval")

    args = parser.parse_args()

    if not args.folder:
        print(f"""Usage:
        {sys.argv[0]} --folder ./images (--saturation 0.5)""")
        sys.exit(1)

    i = InkyPix()
    i.saturation = args.saturation
    i.picture_directory = str(args.folder).strip()
    i.orientation = args.orientation
    i.interval = args.interval * 60
    i.slide_show()
