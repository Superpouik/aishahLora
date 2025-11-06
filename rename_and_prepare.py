#!/usr/bin/env python3
import os
import shutil

# Read the list of images
with open('/tmp/image_list.txt', 'r') as f:
    images = [line.strip() for line in f.readlines()]

print(f"Found {len(images)} images to process")

# Create a directory for renamed images
base_dir = '/home/user/aishahLora'
os.chdir(base_dir)

# Rename images sequentially
for idx, old_path in enumerate(images, start=1):
    # Get the extension
    _, ext = os.path.splitext(old_path)

    # New filename
    new_name = f"{idx}{ext}"
    new_path = os.path.join(base_dir, new_name)

    # Rename the image
    if os.path.exists(old_path):
        shutil.move(old_path, new_path)
        print(f"Renamed: {os.path.basename(old_path)} -> {new_name}")

        # Create associated text file
        txt_file = os.path.join(base_dir, f"{idx}.txt")
        with open(txt_file, 'w') as f:
            f.write("")  # Create empty file for now
        print(f"Created: {idx}.txt")
    else:
        print(f"Warning: {old_path} not found")

print("\nRenaming and text file creation completed!")
