from PIL import Image
import os

# Folder where your WEBP images are located
input_folder = "static/assets/abee"
output_folder = "static/assets/the"

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Loop through each file in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".webp"):
        webp_path = os.path.join(input_folder, filename)
        jpg_filename = filename.replace(".webp", ".jpg")
        jpg_path = os.path.join(output_folder, jpg_filename)

        with Image.open(webp_path) as img:
            rgb_image = img.convert("RGB")
            rgb_image.save(jpg_path, "JPEG")

        print(f"Converted: {filename} → {jpg_filename}")




