import numpy as np
import cv2
import secrets

#convert different type of input to their binary representation
def msgtobinary(msg):
    if type(msg) == str:
        result = ''.join([format(ord(i), "08b") for i in msg])
    elif type(msg) == bytes or type(msg) == np.ndarray:
        result = [format(i, "08b") for i in msg]
    elif type(msg) == int or type(msg) == np.uint8:
        result = format(msg, "08b")
    else:
        raise TypeError("Input type is not supported in this function")
    return result

#Encrypt the plaintext using a generated key and RC4 encryption algorithm
def encryption(plaintext, key):
    key = preparing_key_array(key)
    S = KSA(key)
    keystream = np.array(PRGA(S, len(plaintext)), dtype=np.uint8)
    plaintext = np.array([ord(i) for i in plaintext], dtype=np.uint8)
    cipher = keystream ^ plaintext
    ctext = ''.join([chr(c) for c in cipher])
    return ctext

#Decrypts the ciphertext using the same key and RC4 algorithm
def decryption(ciphertext, key):
    key = preparing_key_array(key)
    S = KSA(key)
    keystream = np.array(PRGA(S, len(ciphertext)), dtype=np.uint8)
    ciphertext = np.array([ord(i) for i in ciphertext], dtype=np.uint8)
    decoded = keystream ^ ciphertext
    dtext = ''.join([chr(c) for c in decoded])
    return dtext

#Generate a random key for encryption
def generate_key(length=16):
    return ''.join(secrets.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(length))

#Converts key into a list of ASCII values
def preparing_key_array(s):
    return [ord(c) for c in s]

#Key Scheduling Algorithm for RC4, initialize the permutation in array S
def KSA(key):
    key_length = len(key)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]
    return S

#Pseudo-Random Generation Algorithm for RC4, generates the keystream
def PRGA(S, n):
    i = 0
    j = 0
    key = []
    while n > 0:
        n -= 1
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        key.append(K)
    return key

#Reads the video file, then allow users to indicate which frame they want the data to be embedded
#then write the modified frames to a new video file
def encode_vid_data():
    cap = cv2.VideoCapture("test_file/input_video.mp4")
    vidcap = cv2.VideoCapture("test_file/input_video.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    frame_width = int(vidcap.get(3))
    frame_height = int(vidcap.get(4))

    size = (frame_width, frame_height)
    out = cv2.VideoWriter('output_video.mp4', fourcc, 25.0, size)
    max_frame = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        max_frame += 1
    cap.release()
    print("Total number of Frames in selected Video:", max_frame)
    print("Enter the frame number where you want to embed data:")
    n = int(input())
    frame_number = 0
    frame_ = None
    while vidcap.isOpened():
        frame_number += 1
        ret, frame = vidcap.read()
        if not ret:
            break
        if frame_number == n:
            change_frame_with, key = embed(frame)
            frame_ = change_frame_with
            frame = change_frame_with
        out.write(frame)

    vidcap.release()
    out.release()
    print("\nEncoded the data successfully in the video file.")
    return frame_, key

#Embded encrypted data into the specified frame
#Read the message from a file, encrypted using a generated key, then converted to binary
#binary data then embedded into LSB of the pixel values in the frame
def embed(frame):
    file_path = "test_file\message.txt"
    with open(file_path, 'r') as file:
        data = file.read()
    
    key = generate_key()
    data = encryption(data, key)
    print("The encrypted data is:", data)
    if len(data) == 0:
        raise ValueError('Data entered to be encoded is empty')

    data += '*^*^*'
    binary_data = msgtobinary(data)
    length_data = len(binary_data)
    index_data = 0

    for i in frame:
        for pixel in i:
            r, g, b = msgtobinary(pixel)
            if index_data < length_data:
                pixel[0] = int(r[:-1] + binary_data[index_data], 2)
                index_data += 1
            if index_data < length_data:
                pixel[1] = int(g[:-1] + binary_data[index_data], 2)
                index_data += 1
            if index_data < length_data:
                pixel[2] = int(b[:-1] + binary_data[index_data], 2)
                index_data += 1
            if index_data >= length_data:
                break
        if index_data >= length_data:
            break
    return frame, key

#Read the encoded video file and extract the data from a specified frame number
#Calls the extract function to decode the data from the frame
def decode_vid_data(frame_, key):
    cap = cv2.VideoCapture('output_video.mp4')
    max_frame = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        max_frame += 1
    cap.release()
    print("Total number of Frames in selected Video:", max_frame)
    print("Enter the secret frame number from where you want to extract data")
    n = int(input())
    vidcap = cv2.VideoCapture('output_video.mp4')
    frame_number = 0
    while vidcap.isOpened():
        frame_number += 1
        ret, frame = vidcap.read()
        if not ret:
            break
        if frame_number == n:
            extract(frame_, key)
            return
    vidcap.release()

#Extract the binary data from the frame by reading the LSB of the pixel values
#it then converts the binary data back to text, decrypt it using provided key
#and print hidden message
def extract(frame, key):
    data_binary = ""
    final_decoded_msg = ""
    for i in frame:
        for pixel in i:
            r, g, b = msgtobinary(pixel)
            data_binary += r[-1]
            data_binary += g[-1]
            data_binary += b[-1]
            total_bytes = [data_binary[i:i+8] for i in range(0, len(data_binary), 8)]
            decoded_data = ""
            for byte in total_bytes:
                decoded_data += chr(int(byte, 2))
                if decoded_data[-5:] == "*^*^*":
                    for i in range(0, len(decoded_data)-5):
                        final_decoded_msg += decoded_data[i]
                    final_decoded_msg = decryption(final_decoded_msg, key)
                    print("\n\nThe Encoded data which was hidden in the Video was :--\n", final_decoded_msg)
                    return
#Sub-Main Function              
def vid_steg():
    a = None  # Initialize a to None
    key = None
    while True:
        print("VIDEO STEGANOGRAPHY OPERATIONS")
        print("1. Encode the Text message")
        print("2. Decode the Text message")
        print("3. Exit")
        choice1 = int(input("Enter the Choice:"))
        if choice1 == 1:
            a, key = encode_vid_data()
            print(f"Save this key to decode the message: {key}")
        elif choice1 == 2:
            if a is not None:
                user_key = input("Enter the key: ")
                if user_key == key:
                    decode_vid_data(a, key)
                else:
                    print("Incorrect key. Cannot decode the message.")
            else:
                print("No encoded data available. Please encode first.")
        elif choice1 == 3:
            break
        else:
            print("Incorrect Choice")
        print("\n")

#Main function
def main():
    while True:
        print("1. Steganography for MP4 Files")
        print("2. Exit\n")
        choice1 = int(input("Enter the Choice: "))
        if choice1 == 1:
            vid_steg()
        elif choice1 == 2:
            break
        else:
            print("Incorrect Choice")
        print("\n\n")

if __name__ == "__main__":
    main()