from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy


class SteganographyDecodeOptionScreen(QWidget):
    def __init__(self, switch_to_steganography, switch_to_decode_images, switch_to_decode_multimedia):
        super().__init__()

        self.switch_to_steganography = switch_to_steganography
        self.switch_to_decode_images = switch_to_decode_images
        self.switch_to_decode_multimedia = switch_to_decode_multimedia

        self.main_layout = QVBoxLayout()

        # Create back button and set its position
        self.back_button = QPushButton('Back', self)
        self.back_button.clicked.connect(self.switch_to_steganography)
        self.back_button.setFixedSize(100, 50)
        self.back_button.move(40, 40)

        # Create the layout for the other buttons
        self.decode_image_button = QPushButton('Decode Images (.png, .jpg...)')
        self.decode_multimedia_button = QPushButton('Decode Multimedia (.wav, .mp3...')
        self.decode_image_button.setFixedSize(300, 100)
        self.decode_multimedia_button.setFixedSize(300, 100)

        self.decode_image_button.clicked.connect(self.switch_to_decode_images)
        self.decode_multimedia_button.clicked.connect(self.switch_to_decode_multimedia)

        # Create layout for the encode and decode buttons
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.decode_image_button)
        self.button_layout.addWidget(self.decode_multimedia_button)

        # Add the button layout to the main layout
        self.main_layout.addStretch()
        self.main_layout.addLayout(self.button_layout)
        self.main_layout.addStretch()

        # Set the main layout for the widget
        self.setLayout(self.main_layout)
