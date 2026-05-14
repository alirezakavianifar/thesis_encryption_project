import os
from PIL import Image

media_dir = r"e:\projects\thesis_project\vertopal_6a6e478acc1947c1bfecfac3523ed62b\media"

for filename in os.listdir(media_dir):
    if filename.endswith(".tiff"):
        img_path = os.path.join(media_dir, filename)
        new_filename = filename.replace(".tiff", ".png")
        new_path = os.path.join(media_dir, new_filename)
        
        print(f"Converting {filename} to {new_filename}...")
        with Image.open(img_path) as img:
            img.save(new_path, "PNG")
        # Optional: remove original tiff
        # os.remove(img_path)
