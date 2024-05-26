import cv2
import os
from cryptography.fernet import Fernet
from PIL import Image
import binascii
from moviepy.editor import ImageSequenceClip

#Extract frame
def extract_frames(video_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    vidcap = cv2.VideoCapture(video_path)
    success, image = vidcap.read()
    count = 0

    while success:
        cv2.imwrite(f"{output_folder}/frame{count:04d}.png", image) #Save frame as PNG file
        success, image = vidcap.read()
        count += 1

    vidcap.release()

#Encrypt text message
def encrypt_message(message, key):
    cipher_suite = Fernet(key)
    encrypted_text = cipher_suite.encrypt(message.encode())
    print(f"Encrypted message: {encrypted_text}")
    return encrypted_text

#Embed the encrypted text inside the png frame
def embed_message(image_path, message):
    image = Image.open(image_path)
    binary_message = ''.join(format(byte, '08b') for byte in message)
    message_length = len(binary_message)

    print(f"Embedding message of length {message_length} bits into {image_path}")

    pixels = image.load()
    width, height = image.size

    idx = 0
    for y in range(height):
        for x in range(width):
            pixel = list(pixels[x,y])
            for n in range(3): #This iterates over the RGB
                if idx < message_length:
                    pixel[n] = pixel[n] & ~1 | int(binary_message[idx])
                    idx += 1
                else:
                    break

    image.save(image_path)
    print(f"Message embedded in {image_path}")

#Reassemble the frames back into MP4
def create_videos_from_frames(frames_folder, output_video_path, fps=24):
    frame_files = [os.path.join(frames_folder, f) for f in sorted(os.listdir(frames_folder)) if f.endswith('.png')]
    clip = ImageSequenceClip(frame_files, fps = fps)
    clip.write_videofile(output_video_path, codec='libx264')
    print(f"Created video {output_video_path} from frames in {frames_folder}")

#Main process
video_path = 'input_video.mp4'
frames_folder = 'frames'
output_video_path = 'output_video.mp4'
key = Fernet.generate_key()

print(f"Generated encryption key: {key.decode()}")
extract_frames(video_path, frames_folder)

with open('message.txt', 'r') as file:
    message = file.read()
print(f"Read message: {message}")

encrypted_message = encrypt_message(message, key)
embed_message(f'{frames_folder}/frame0000.png', encrypted_message)
create_videos_from_frames(frames_folder, output_video_path)

print(f'Encryption key: {key.decode()}')