import wave

def encode_audio(input_audio, secret_audio, output_audio):
    # Open the input audio file
    input_wave = wave.open(input_audio, mode='rb')
    input_frames = bytearray(list(input_wave.readframes(input_wave.getnframes())))
    
    # Open the secret audio file
    secret_wave = wave.open(secret_audio, mode='rb')
    secret_frames = bytearray(list(secret_wave.readframes(secret_wave.getnframes())))
    
    # Ensure the secret audio can fit into the input audio
    if len(secret_frames) * 8 > len(input_frames):
        print("Error: The secret audio file is too large to be hidden in the input audio file.")
        return
    
    # Convert secret audio to bit array
    secret_bits = ''.join(f'{byte:08b}' for byte in secret_frames)
    
    # Replace LSB of each byte of the input audio data by one bit from the secret audio bit array.
    # NOTE TO SELF: The ~ operator is a bitwise NOT operation, which inverts all the bits of a number. When you use & ~1, you are effectively clearing the least significant bit (LSB) of a byte before setting it to the desired value.
    # nOT ME SPENDING HOURS FIGURING IT BECAUSE I NEVER ADD ~ 
    for i in range(len(secret_bits)):
        input_frames[i] = (input_frames[i] & ~1) | int(secret_bits[i])
    
    # Write the modified frames to a new wave audio file
    with wave.open(output_audio, 'wb') as output_wave:
        output_wave.setparams(input_wave.getparams())
        output_wave.writeframes(bytes(input_frames))
    
    input_wave.close()
    secret_wave.close()
    print("Encoding complete. The output file is:", output_audio)

# Use the function
encode_audio('Fluffing-a-Duck.wav', 'omgeavesdrop.wav', 'output.wav')