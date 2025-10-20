# downscales AI generated images located in frontend

import os
from PIL import Image

input_dir = "images/"
output_dir = "downscaled/"

SCALE = 0.3
# gems are smaller
GEM_SCALE = 0.1

for filename in os.listdir(input_dir):
    print(filename)
    if filename.lower().endswith((".png")):
        scale = SCALE

        img = Image.open(os.path.join(input_dir, filename))
        new_size = (int(img.width * scale), int(img.height * scale))
        resized = img.resize(new_size, Image.Resampling.LANCZOS)
        resized.save(os.path.join(output_dir, filename))

        print(f"✔️ {filename} downscaled by {scale}")

print("✅ All images downscaled successfully.")
