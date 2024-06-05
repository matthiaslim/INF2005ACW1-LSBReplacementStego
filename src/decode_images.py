import os

import cv2
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QTextEdit, QFileDialog, QHBoxLayout, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QDropEvent
import stego_image


class DecodeImageScreen(QWidget):
    def __init__(self, switch_to_steganography):
        super().__init__()

        self.switch_to_steganography = switch_to_steganography

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(10, 20, 10, 20)  # Set margins for the main layout
        self.main_layout.setSpacing(10)  # Set spacing between widgets

        # Create back button and set its position
        self.back_button = QPushButton('Back', self)
        self.back_button.clicked.connect(self.on_back_button_clicked)
        self.back_button.setFixedSize(100, 50)
        self.back_button.move(20, 20)

        # Layout of the image to drag and drop into the steg image
        self.payload_layout = QVBoxLayout()

        # Layout of the payload buttons (eg. bits etc)
        self.payload_button_layout = QHBoxLayout()

        # Create label to hold the drag and drop encoded image to be decoded
        self.encoded_image_label = QLabel("Drag and drop your encoded image here (png, bitmap)")
        self.encoded_image_label.setStyleSheet("QLabel { border: 2px dashed #aaa; }")
        self.encoded_image_label.setAlignment(Qt.AlignCenter)
        self.encoded_image_label.setFixedHeight(700)
        self.encoded_image_label.setAcceptDrops(True)
        # Change this function accordingly ***
        self.encoded_image_label.dragEnterEvent = self.dragEnterEvent
        self.encoded_image_label.dropEvent = self.stegimage_dropEvent

        # Create buttons to add file from explorer or remove file
        self.choose_image_button = QPushButton('Add file', self)
        self.choose_image_button.setFixedWidth(150)
        # Change function accordingly
        self.choose_image_button.clicked.connect(self.select_decode_image)

        self.remove_file_button = QPushButton('Remove file', self)
        self.remove_file_button.setFixedWidth(150)
        # Change function accordingly
        self.remove_file_button.clicked.connect(self.remove_payload_file)

        # Allow users to choose bits to decode with
        self.bits_label = QLabel()
        self.bits_label.setText("Bits used:")
        self.bits_dropdown = QComboBox()
        self.bits_dropdown.addItems(["1", "2", "3", "4", "5", "6", "7", "8"])

        # Add widgets to the payload layout respectively
        self.payload_button_layout.addWidget(self.choose_image_button)
        self.payload_button_layout.addWidget(self.remove_file_button)
        self.payload_button_layout.addWidget(self.bits_label)
        self.payload_button_layout.addWidget(self.bits_dropdown)
        self.payload_button_layout.setAlignment(Qt.AlignLeft)
        self.payload_layout.addWidget(self.encoded_image_label)
        self.payload_layout.addLayout(self.payload_button_layout)

        # Create text edit for your secret message result
        self.decoded_text = QTextEdit(self)
        self.decoded_text.setPlaceholderText("Your Secret Message lies here after decoding")
        self.decoded_text.setFixedHeight(50)
        self.decoded_text.setContentsMargins(10, 0, 10, 0)
        self.decoded_text.setReadOnly(True)

        # Add all the widgets into main layout
        self.main_layout.addWidget(self.back_button)
        self.main_layout.addLayout(self.payload_layout)
        self.main_layout.addWidget(self.decoded_text)

        self.button_layout = QHBoxLayout()
        self.button_layout.addStretch(1)
        self.decode_button = QPushButton('Decode')
        self.decode_button.setFixedSize(200,100)
        self.decode_button.clicked.connect(self.decode_message)
        self.button_layout.addWidget(self.decode_button)
        self.button_layout.addStretch(1)

        self.main_layout.addLayout(self.button_layout)
        self.setLayout(self.main_layout)

        self.steg_image_path = ""

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def stegimage_dropEvent(self,event):
        urls = event.mimeData().urls()
        if urls and urls[0].isLocalFile():
            self.steg_image_path = urls[0].toLocalFile()
            pixmap = QPixmap(self.steg_image_path)
            if not pixmap.isNull():
                max_width = self.encoded_image_label.width()
                max_height = self.encoded_image_label.height()
                self.encoded_image_label.setPixmap(pixmap.scaled(max_width, max_height, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                self.encoded_image_label.clear()

    def select_decode_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Decode Image", "",
                                                   "Images (*.png *.bmp);;All Files (*)", options=options)
        if file_path:
            self.steg_image_path = file_path
            pixmap = QPixmap(self.steg_image_path)
            if not pixmap.isNull():
                max_width = self.encoded_image_label.width()
                max_height = self.encoded_image_label.height()
                self.encoded_image_label.setPixmap(pixmap.scaled(max_width, max_height, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                self.encoded_image_label.clear()
                self.encoded_image_label.setText("Invalid image file. Please select a valid PNG or BMP image.")

    def remove_payload_file(self):
        self.steg_image_path = ""
        self.encoded_image_label.clear()
        self.encoded_image_label.setText("Drag and drop your encoded image here (png, bitmap)")

    def decode_message(self):
        if not self.steg_image_path:
            self.decoded_text.setText("No image selected or invalid path")
            return

        lsb_use = int(self.bits_dropdown.currentText())
        try:
            decoded_data = stego_image.decode(self.steg_image_path,lsb_use)
            self.decoded_text.setText(f"{decoded_data}")
        except Exception as e:
            self.decoded_text.setText(f"Error: {str(e)}")

    def backbutton_clear(self):
        self.steg_image_path = ""
        self.decoded_text.setText("Your Secret Message lies here after decoding")
        self.encoded_image_label.clear()
        self.encoded_image_label.setText("Drag and drop your encoded image here (png, bitmap)")

    def on_back_button_clicked(self):
        self.backbutton_clear()
        self.switch_to_steganography()
