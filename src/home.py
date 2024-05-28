import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget

class MainScreen(QWidget):
    def __init__(self,switch_to_steganography,switch_to_steganalysis):
        super().__init__()

        self.switch_to_steganography = switch_to_steganography
        self.switch_to_steganalysis = switch_to_steganalysis

        self.main_layout = QVBoxLayout(self)
        self.button_layout = QHBoxLayout()

        self.encode_decode_button = QPushButton('Steganography Encode/Decode')
        self.steganalysis_button = QPushButton('Steganalysis')

        self.encode_decode_button.setFixedSize(400, 200)
        self.steganalysis_button.setFixedSize(400, 200)

        self.encode_decode_button.clicked.connect(self.switch_to_steganography)
        self.steganalysis_button.clicked.connect(self.switch_to_steganalysis)

        self.button_layout.addWidget(self.encode_decode_button)
        self.button_layout.addWidget(self.steganalysis_button)
        self.main_layout.addLayout(self.button_layout)