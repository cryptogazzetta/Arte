from PIL import Image
import requests
from io import BytesIO
import os

def resize_image(image_url, width_limit, height_limit, output_directory):
    try:
        # Get the image from the URL
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))

        # Get the original dimensions
        original_width, original_height = img.size

        # Calculate the new dimensions while preserving aspect ratio
        if original_width > width_limit or original_height > height_limit:
            width_ratio = width_limit / original_width
            height_ratio = height_limit / original_height
            resize_ratio = min(width_ratio, height_ratio)
            new_width = int(original_width * resize_ratio)
            new_height = int(original_height * resize_ratio)
        else:
            # Image is already within the size limits
            new_width, new_height = original_width, original_height

        # Resize the image
        resized_img = img.resize((new_width, new_height), Image.ANTIALIAS)

        # Generate a new filename for the resized image
        base_filename = os.path.basename(image_url)
        output_filename = os.path.join(output_directory, base_filename)

        # Save the resized image to the output directory
        resized_img.save(output_filename)

        return output_filename
    except Exception as e:
        print("Error:", str(e))
        return None

# Example usage:
image_url = "https://example.com/image.jpg"
width_limit = 800  # Set your width limit
height_limit = 600  # Set your height limit
output_directory = "/path/to/output/directory"

resized_image_url = resize_image(image_url, width_limit, height_limit, output_directory)
if resized_image_url:
    print("Resized image URL:", resized_image_url)
else:
    print("Failed to resize the image.")
