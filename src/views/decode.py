from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout


class DecodeScreen(QWidget):
    def __init__(self, switch_to_steganography):
        super().__init__()

        self.switch_to_steganography = switch_to_steganography

        self.main_layout = QVBoxLayout()

        # Create back button and set its position
        self.back_button = QPushButton('Back', self)
        self.back_button.clicked.connect(self.switch_to_steganography)
        self.back_button.setFixedSize(100, 50)
        self.back_button.move(20, 20)

        # Create the layout for the other buttons
        self.encode_button = QPushButton('Decode',self)
        self.encode_button.setFixedSize(200, 100)



        # Add the button layout to the main layout
        self.main_layout.addStretch()
        # self.main_layout.addLayout(self.button_layout)
        self.main_layout.addStretch()

        # Set the main layout for the widget
        self.setLayout(self.main_layout)
