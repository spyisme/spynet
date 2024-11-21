from pathlib import Path
from PIL import Image

image_path = Path("./img1.png")


def downloadimage():
    print("soooo")

def is_valid_image(file_path):
    """Check if the file is a valid image."""
    try:
        with Image.open(file_path) as img:
            img.verify()  # Verify the file is a valid image
        return True
    except Exception:
        return False


while True:
    # Check if the image exists and is valid
    if image_path.exists() and is_valid_image(image_path):
        print("Valid image downloaded.")
        break
    else:
        print("Image is invalid or missing. Redownloading...")
        downloadimage()