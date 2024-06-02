from PIL import Image
import numpy as np
import cv2


def to_bin(data):
    if isinstance(data, str):
        return ''.join([format(ord(i), "08b") for i in data])
    elif isinstance(data, bytes) or isinstance(data, np.ndarray):
        return [format(i, "08b") for i in data]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, "08b")
    else:
        raise TypeError("Not supported")

# converting types to binary


def encode(image_name, payload_data, lsb_use):
    image = cv2.imread(image_name)
    n_bytes = image.shape[0] * image.shape[1] * 3 // 8
    print("max byte to encode: ", n_bytes)
    payload_data += "====="
    if len(payload_data) > n_bytes:
        raise ValueError("Insufficient bytes, need bigger image or less data")
    print("Encoding...")

    data_index = 0
    print(payload_data)
    binary_secret_data = to_bin(payload_data)
    data_len = len(binary_secret_data)

    if data_len % lsb_use != 0:
        binary_secret_data += '0' * (8 - (data_len % lsb_use))

    for row in image:
        for pixel in row:
            r, g, b = to_bin(pixel)
            if data_index < data_len:
                pixel[0] = int(
                    r[:-lsb_use] + binary_secret_data[data_index:data_index + lsb_use], 2)
                data_index += lsb_use
            if data_index < data_len:
                pixel[1] = int(
                    g[:-lsb_use] + binary_secret_data[data_index:data_index + lsb_use], 2)
                data_index += lsb_use
            if data_index < data_len:
                pixel[2] = int(
                    b[:-lsb_use] + binary_secret_data[data_index:data_index + lsb_use], 2)
                data_index += lsb_use
            if data_index >= data_len:
                break
    print("Reached end of encode")
    return image


def decode(image_name, lsb_use):
    print("[+] decoding...")
    image = cv2.imread(image_name)
    binary_data = ""
    for row in image:
        for pixel in row:
            r, g, b = to_bin(pixel)
            binary_data += r[-lsb_use:]
            binary_data += g[-lsb_use:]
            binary_data += b[-lsb_use:]

    all_bytes = [binary_data[i:i + 8] for i in range(0, len(binary_data), 8)]

    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        #print(decoded_data + "\n")
        if decoded_data[-5:] == "=====":
            break
    return decoded_data[:-5]

#
# if __name__ == "__main__":
#     input_image = "instagram.png"
#     output_image = "instagram_stg.png"
#     secret_data = "messagemessagemessage"
#
#     encoded_image = encode(input_image, secret_data, 5)
#     cv2.imwrite(output_image, encoded_image)
#     print("Encoded image now to decode")
#
#     decoded_data = decode(output_image, 5)
#     print(decoded_data)
