import numpy as np


def to_bin(data):
    """Convert 'data' to binary format as string.

    Args:
        data (str, bytes, np.ndarray, int, np.uint8): Data to be converted to binary.

    Returns:
        str or list of str: Binary representation of the input data.

    Raises:
        TypeError: If the data type is not supported.
    """
    if isinstance(data, str):
        return ''.join([format(ord(i), "08b") for i in data])
    elif isinstance(data, bytes) or isinstance(data, np.ndarray):
        return [format(i, "08b") for i in data]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, "08b")
    else:
        raise TypeError("Type not supported")


def bits_to_text(bits):
    """Convert a binary string to text.

    Args:
        bits (str): Binary string to be converted to text.

    Returns:
        str: The resulting text.
    """
    chars = [bits[i:i + 8] for i in range(0, len(bits), 8)]
    return ''.join(chr(int(char, 2)) for char in chars)