from PIL import Image
from utils import bits_to_text  # Assuming this function is in utils.py and converts binary to text
from stego_image import decode_image  # Import the core function

# Use the function
image_path = 'output_image.png'  # Path to the encoded image file
lsb_count = 1  # Number of LSBs used for encoding, should match the one used during encoding

# Call the decoding function
try:
    decoded_message = decode_image(image_path, lsb_count)
    print(f'Decoded message: {decoded_message}')
except Exception as e:
    print(f"Error decoding image: {e}")
