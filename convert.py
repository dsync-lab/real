from PIL import Image
import os
import shutil

SOURCE_DIR = "/home/ukov/Downloads/ikl"
WEBP_ARCHIVE_DIR = "/home/ukov/Downloads/ikl_webp_backup"

# create archive folder if it doesn't exist
os.makedirs(WEBP_ARCHIVE_DIR, exist_ok=True)

for filename in os.listdir(SOURCE_DIR):
    if filename.lower().endswith(".webp"):
        webp_path = os.path.join(SOURCE_DIR, filename)
        jpg_path = os.path.join(
            SOURCE_DIR,
            filename.rsplit(".", 1)[0] + ".jpg"
        )

        # convert to JPEG
        img = Image.open(webp_path).convert("RGB")
        img.save(jpg_path, "JPEG", quality=90)

        # move original WEBP
        shutil.move(
            webp_path,
            os.path.join(WEBP_ARCHIVE_DIR, filename)
        )

        print(f"Converted & moved: {filename}")
