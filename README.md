# LSB Replacement Steganography Tool

This tool provides a graphical user interface (GUI) for hiding and extracting messages in images using the Least Significant Bit (LSB) replacement technique. The application is built using Python, `tkinter` for the GUI, and `Pillow` for image processing.

## Features

- Encode a secret message into an image.
- Decode a hidden message from an image.
- Simple and intuitive GUI.

## Requirements

- Python 3.x
- Pillow library

## Installation

1. **Clone the repository** or download the source code.

```sh
git clone https://github.com/matthiaslim/INF2005ACW1-LSBReplacementStego.git
cd INF2005ACW1-LSBReplacementStego
```

2. **Install the required packages using the requirements text file**.

```sh
pip install -r requirements.txt
```

## Usage

1. **Run the application**.

```sh
python lsb_steganography.py
```

2. **Encode a message**.

    - Click the "Encode Message" button.
    - Select the image file where you want to hide the message.
    - Enter the message you want to hide in the text box.
    - Choose the output image file to save the encoded image.
    - The message will be embedded into the image and saved to the specified location.

3. **Decode a message**.

    - Click the "Decode Message" button.
    - Select the image file from which you want to extract the hidden message.
    - The hidden message will be displayed in a message box.

## Files

- `lsb_steganography.py`: The main application script containing the GUI and steganography functions.
- `README.md`: This file.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
