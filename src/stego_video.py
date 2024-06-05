import numpy as np
import cv2

# Convert different types of input to their binary representation
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

# Reads the video file, then allow users to indicate which frame they want the data to be embedded
# then write the modified frames to a new video file
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
    
    if n < 1 or n > max_frame:
        print(f"Wrong frame number: {n}. Please enter a number between 1 and {max_frame}.")
        return

    frame_number = 0
    frame_ = None
    while vidcap.isOpened():
        frame_number += 1
        ret, frame = vidcap.read()
        if not ret:
            break
        if frame_number == n:
            change_frame_with = embed(frame)
            frame_ = change_frame_with
            frame = change_frame_with
        out.write(frame)

    vidcap.release()
    out.release()
    print("\nEncoded the data successfully in the video file.")
    
    with open("frame_number.txt", "w") as file:
        file.write(str(n))
    
    return frame_

# Embed encrypted data into the specified frame
# Read the message from a file, then converted to binary
# binary data then embedded into LSB of the pixel values in the frame
def embed(frame):
    file_path = "test_file/message.txt"
    with open(file_path, 'r') as file:
        data = file.read()

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
    return frame

# Read the encoded video file and extract the data from a specified frame number
# Calls the extract function to decode the data from the frame
def decode_vid_data(frame_):
    with open("frame_number.txt", "r") as file:
        stored_frame_number = int(file.read().strip())

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
    
    if n != stored_frame_number:
        print(f"Wrong frame number: {n}. The correct frame number is required for decryption.")
        return

    vidcap = cv2.VideoCapture('output_video.mp4')
    frame_number = 0
    while vidcap.isOpened():
        frame_number += 1
        ret, frame = vidcap.read()
        if not ret:
            break
        if frame_number == n:
            extract(frame_)
            return
    vidcap.release()

# Extract the binary data from the frame by reading the LSB of the pixel values
# it then converts the binary data back to text, and prints the hidden message
def extract(frame):
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
                    print("\n\nThe Encoded data which was hidden in the Video was :--\n", final_decoded_msg)
                    return

# Sub-Main Function              
def main():
    a = None  #
    while True:
        print("1. Encode the Text message")
        print("2. Decode the Text message")
        print("3. Exit")
        choice1 = int(input("Enter the Choice:"))
        if choice1 == 1:
            a = encode_vid_data()
        elif choice1 == 2:
            if a is not None:
                decode_vid_data(a)
            else:
                print("No encoded data available. Please encode first.")
        elif choice1 == 3:
            break
        else:
            print("Incorrect Choice")
        print("\n")

if __name__ == "__main__":
    main()
