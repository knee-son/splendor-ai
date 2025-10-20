# downscales AI generated images located in frontend

import os
from PIL import Image

input_dir = "../frontend-ministry/src/assets/images/hi-res/"
output_dir = "../frontend-ministry/src/assets/images/"

print(os.listdir('../frontend-ministry/src/assets/images/hi-res/'))

WIDTH = 300
HEIGHT = 450
# gems are smaller
GEM_HEIGHT = 50

for filename in os.listdir(output_dir):
    file_path = os.path.join(output_dir, filename)
    if os.path.isfile(file_path):
        os.remove(file_path)

for filename in os.listdir(input_dir):
    if filename.lower().endswith((".png", ".jpg")):
        base_name = os.path.splitext(filename)[0]
        height = HEIGHT

        if(base_name.split('_')[-1] == 'gem'):
            height = GEM_HEIGHT

        img = Image.open(os.path.join(input_dir, filename))
        scale = height / img.height

        if(base_name.split('_')[0] == 'noble'):
            scale = WIDTH / img.width

        new_size = (int(img.width * scale), int(img.height * scale))

        if(base_name == 'backside_card'):
            new_size = (WIDTH, HEIGHT)
        elif(base_name == 'backside_noble'):
            new_size = (WIDTH, WIDTH)

        resized = img.resize(new_size, Image.Resampling.LANCZOS)

        out_path = os.path.join(output_dir, f"{base_name}.png")
        resized.save(out_path, format="PNG")

        print(f"✔️  {filename} downscaled by {scale}")

print("✅ All images downscaled successfully.")
