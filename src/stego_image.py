from PIL import Image
from utils import to_bin, bits_to_text


def encode_image(image_path, text, lsb_count, output_path):
    image = Image.open(image_path)
    width, height = image.size
    index = 0

    text += chr(0)  # Append null character to mark end of text
    text_bits = to_bin(text)

    if len(text_bits) > width * height * lsb_count:
        raise ValueError("Text too long to encode in image with the given number of LSBs.")

    encoded_image = image.copy()
    pixels = encoded_image.load()

    for y in range(height):
        for x in range(width):
            if index < len(text_bits):
                pixel = list(pixels[x, y])
                for i in range(3):  # Iterate over RGB values
                    for j in range(lsb_count):
                        if index < len(text_bits):
                            pixel[i] = (pixel[i] & ~(1 << j)) | (int(text_bits[index]) << j)
                            index += 1
                pixels[x, y] = tuple(pixel)
            else:
                break

    encoded_image.save(output_path)


def decode_image(image_path, lsb_count):
    image = Image.open(image_path)
    width, height = image.size
    bits = []

    pixels = image.load()
    for y in range(height):
        for x in range(width):
            pixel = pixels[x, y]
            for i in range(3):  # Iterate over RGB values
                for j in range(lsb_count):
                    bits.append((pixel[i] >> j) & 1)

    bits = ''.join(map(str, bits))
    message = bits_to_text(bits)
    print("Decoded bits:", bits) # Debugging
    return message.split(chr(0))[0]  # Remove any extra data after the null character
