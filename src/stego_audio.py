from pydub import AudioSegment
from utils import to_bin, bits_to_text


def encode_audio(audio_path, text, lsb_count, output_path):
    audio = AudioSegment.from_file(audio_path, format="wav")
    samples = audio.get_array_of_samples()
    sample_width = audio.sample_width
    num_samples = len(samples)

    text += chr(0)  # Append null character to mark end of text
    text_bits = to_bin(text)

    if len(text_bits) > num_samples * lsb_count:
        raise ValueError("Text too long to encode in audio with the given number of LSBs.")

    encoded_samples = samples[:]
    for i in range(len(text_bits)):
        encoded_samples[i] = (encoded_samples[i] & ~(1 << i % sample_width)) | (int(text_bits[i]) << i % sample_width)

    encoded_audio = audio._spawn(encoded_samples)
    encoded_audio.export(output_path, format="wav")


def decode_audio(audio_path, lsb_count):
    audio = AudioSegment.from_file(audio_path, format="wav")
    samples = audio.get_array_of_samples()

    bits = []
    for sample in samples:
        for i in range(lsb_count):
            bits.append((sample >> i) & 1)

    bits = ''.join(map(str, bits))
    message = bits_to_text(bits)
    return message.split(chr(0))[0]
