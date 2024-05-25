import wave

def encode_audio(input_audio, message_file, output_audio, lsb_num):
    # Open the audio file
    audio = wave.open(input_audio, mode='rb')

    # Read frames and convert to byte array
    frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))

    # Read the message from the file
    with open(message_file, 'r') as file:
        message = file.read()

    # Check if payload is too large for cover object. the test text file is 100mb-examplefile-com. just change the line at 43
    if len(message) * 8 > len(frame_bytes) * lsb_num:
        print("Error: The payload is too large for the selected cover object.")
        return

    # Append dummy data to fill out rest of the bytes
    # len(frame_bytes): This retrieves the length of the audio file in terms of bytes.
    # len(message) * 8 * 8: This calculates the number of bits required to represent the message. Each character in the message is represented by 8 bits (1 byte), and len(message) gives the number of characters.
    # len(frame_bytes) - (len(message) * 8 * 8): This calculates the number of remaining bytes in the audio file after considering the bits required for the message.
    # '#': This is a filler character used to pad the message
    message += int((len(frame_bytes)-(len(message)*8*8))/8) *'#'
    
    # Convert text to bit array
    bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in message])))

    # Replace LSB of each byte of the audio data by one bit from the text bit array
    for i, bit in enumerate(bits):
        frame_bytes[i] = (frame_bytes[i] & (255 << lsb_num)) | bit

    # Print the bits being used
    print(f"Bits being used for encoding: {list(range(lsb_num))}")

    # Get the modified frames
    modified_frames = bytes(frame_bytes)

    # Write bytes to a new wave audio file
    with wave.open(output_audio, 'wb') as fd:
        fd.setparams(audio.getparams())
        fd.writeframes(modified_frames)

    audio.close()

# Use the function
encode_audio('Fluffing-a-Duck.wav', 'encode_text.txt', 'output.wav', 6)
