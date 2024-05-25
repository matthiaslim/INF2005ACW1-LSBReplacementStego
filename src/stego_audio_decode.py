# Wave package for reading and writing .wav audio files
import wave

#import libraries for audio analysis
import thinkdsp
from thinkdsp import read_wave

# Read selected audio file
mySound = wave.open("output.wav",mode = 'rb')
wave = read_wave("output.wav")

# Read frames and convert to byte array
# mySound.readframes: This reads all the audio frames from the WAV file.
# mySound.getnframes: This returns the number of audio frames in the WAV file.
# bytearray(list(...)): This converts the frames into a list and then into a byte array

frameBytes = bytearray(list(mySound.readframes(mySound.getnframes())))
print ("Number of frames: ",mySound.getnframes())
# Display first 10 frames of the list
print ("First 10 of frames list: ",frameBytes[0:10])

# Extract the least Significant bit of each byte.
# This will allow us to hide data in the least significant bits without significantly affecting the audio quality.
extracted = [frameBytes[i] & 1 for i in range(len(frameBytes))]

#Convert the byte array back to string
string = "".join(chr(int("".join(map(str,extracted[i:i+8])),2))for i in range(0,len(extracted),8))

#Display the first 100 string characters since the end result is too huge 
print(string[0:100])

# Remove any filler characters
decoded = string.split("###")[0]
# Print the decoded TEXT
print("The hidden message is: " +decoded)
mySound.close()