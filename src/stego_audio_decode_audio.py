import wave

def decode_audio(stego_audio, output_secret_audio, secret_audio_params):
    # Open the stego audio file
    stego_wave = wave.open(stego_audio, mode='rb')
    stego_frames = bytearray(list(stego_wave.readframes(stego_wave.getnframes())))
    
    # Extract the least significant bits from each byte
    extracted_bits = [stego_frames[i] & 1 for i in range(len(stego_frames))]
    
    # Convert the bit array back to bytes
    secret_bytes = bytearray()
    for i in range(0, len(extracted_bits), 8):
        byte = ''.join(map(str, extracted_bits[i:i+8]))
        secret_bytes.append(int(byte, 2))
    
    # Write the extracted bytes to a new wave audio file
    with wave.open(output_secret_audio, 'wb') as output_wave:
        output_wave.setparams(secret_audio_params)
        output_wave.writeframes(bytes(secret_bytes))
    
    stego_wave.close()
    print("Decoding complete. The hidden audio file is:", output_secret_audio)

# Use the function
secret_wave = wave.open('omgeavesdrop.wav', mode='rb')

# Get the secret audio parameters (needed to correctly decode the hidden audio)
secret_audio_params = secret_wave.getparams()

decode_audio('output.wav', 'extracted_secret.wav', secret_audio_params)

secret_wave.close()