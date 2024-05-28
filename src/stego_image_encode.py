from PIL import Image
from utils import to_bin  
from stego_image import encode_image  # Import core function

def read_text_from_file(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
        print("Contents of text file:", repr(text))  # Print the contents of the text file
        return file.read()

# Use the function
image_path = 'images/original/quack.png'  # Path to the input image file
text_file_path = 'encode_image.txt'  # Path to the text file containing the message
output_path = 'output_image.png'  # Path to save the encoded image file
lsb_count = 2  # Number of LSBs to use for encoding, can be any value from 1 to 8

# Read the message from the text file
text = read_text_from_file(text_file_path)

# Call the encoding function
encode_image(image_path, text, lsb_count, output_path)
