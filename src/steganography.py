from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy


class SteganographyScreen(QWidget):
    def __init__(self, switch_to_main, switch_to_encode, switch_to_decode):
        super().__init__()

        self.switch_to_main = switch_to_main
        self.switch_to_encode = switch_to_encode
        self.switch_to_decode = switch_to_decode

        self.main_layout = QVBoxLayout()



        # Create back button and set its position
        self.back_button = QPushButton('Back',self)
        self.back_button.clicked.connect(self.switch_to_main)
        self.back_button.setFixedSize(100,50)
        self.back_button.move(40,40)

        # Create the layout for the other buttons
        self.encode_button = QPushButton('Encode')
        self.decode_button = QPushButton('Decode')
        self.encode_button.setFixedSize(200, 100)
        self.decode_button.setFixedSize(200, 100)

        self.encode_button.clicked.connect(self.switch_to_encode)
        self.decode_button.clicked.connect(self.switch_to_decode)

        # Create layout for the encode and decode buttons
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.encode_button)
        self.button_layout.addWidget(self.decode_button)

        # Add the button layout to the main layout
        self.main_layout.addStretch()
        self.main_layout.addLayout(self.button_layout)
        self.main_layout.addStretch()

        # Set the main layout for the widget
        self.setLayout(self.main_layout)






