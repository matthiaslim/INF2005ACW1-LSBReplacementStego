from PIL import Image
from cryptography.fernet import Fernet
import cv2
import os
import base64

# Extract the frame from the video
def extract_frames(video_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    vidcap = cv2.VideoCapture(video_path)
    success, image = vidcap.read()
    count = 0

    while success:
        cv2.imwrite(f"{output_folder}/frame{count:04d}.png", image)  # Save frame as PNG file
        success, image = vidcap.read()
        count += 1

    vidcap.release()
    print(f"Extracted {count} frames from {video_path}")

# Extract the encrypted message from the frame
def extract_message(image_path, message_length_bits):
    image = Image.open(image_path)
    pixels = image.load()
    width, height = image.size

    binary_message = []
    idx = 0

    for y in range(height):
        for x in range(width):
            pixel = list(pixels[x, y])
            for n in range(3):  # This iterates over the RGB
                if idx < message_length_bits:
                    binary_message.append(pixel[n] & 1)
                    idx += 1
                else:
                    break
            if idx >= message_length_bits:
                break
        if idx >= message_length_bits:
            break


    if len(binary_message) != message_length_bits:
        print(f"Error: Expected {message_length_bits} bits, but got {len(binary_message)} bits")
        return None

    binary_message_str = ''.join(map(str, binary_message))
    print(f"Binary message: {binary_message_str}")  # Debug print

    if len(binary_message_str) % 8 != 0:
        binary_message_str = binary_message_str.ljust((len(binary_message_str) + 7) // 8 * 8, '0')

    # Convert binary string to bytes
    encrypted_message = int(binary_message_str, 2).to_bytes((message_length_bits + 7) // 8, byteorder='big')
    print(f"Encrypted message (bytes): {encrypted_message}") 

    return encrypted_message

# Decrypt the extracted message
def decrypt_message(encrypted_message, key):
    if encrypted_message is None:
        print("Error: No message to decrypt")
        return None

    try:
        cipher_suite = Fernet(key)
        decrypted_text = cipher_suite.decrypt(encrypted_message)
        return decrypted_text.decode('utf-8')
    except Exception as e:
        print(f"Decryption error: {e}")
        return None

# Main process
output_video_path = 'output_video.mp4'
output_frames_folder = 'output_frames'
message_length_bits = 800  
key = b'D0K4BRt0lRrl6y0ReHiVNKnU-jaTGgjTijB6GWP3pHA=' 

# Execution
extract_frames(output_video_path, output_frames_folder)
extracted_message = extract_message(f'{output_frames_folder}/frame0000.png', message_length_bits)
print(f"Extracted message: {extracted_message}")  
if extracted_message:
    decrypted_message = decrypt_message(extracted_message, key)
    if decrypted_message:
        print(f"Decrypted message: {decrypted_message}")
    else:
        print("Failed to decrypt the message.")
else:
    print("Failed to extract the message.")
