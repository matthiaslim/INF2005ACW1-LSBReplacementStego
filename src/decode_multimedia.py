import os

import cv2
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QTextEdit, QFileDialog, QHBoxLayout, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QDropEvent
import stego_audio_decode_text


class DecodeMultimediaScreen(QWidget):
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
        self.encoded_multimedia_label = QLabel("Drag and drop your encoded multimedia here (.wav, .mp4)")
        self.encoded_multimedia_label.setStyleSheet("QLabel { border: 2px dashed #aaa; }")
        self.encoded_multimedia_label.setAlignment(Qt.AlignCenter)
        self.encoded_multimedia_label.setFixedHeight(700)
        self.encoded_multimedia_label.setAcceptDrops(True)
        # Change this function accordingly ***
        self.encoded_multimedia_label.dragEnterEvent = self.dragEnterEvent
        self.encoded_multimedia_label.dropEvent = self.stegimage_dropEvent

        # Create buttons to add file from explorer or remove file
        self.choose_image_button = QPushButton('Add file', self)
        self.choose_image_button.setFixedWidth(150)
        # Change function accordingly
        self.choose_image_button.clicked.connect(self.select_decode_multimedia)

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
        self.payload_layout.addWidget(self.encoded_multimedia_label)
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

        self.steg_multimedia_path = ""

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def stegimage_dropEvent(self,event):
        urls = event.mimeData().urls()
        if urls and urls[0].isLocalFile():
            self.steg_multimedia_path = urls[0].toLocalFile()
            self.encoded_multimedia_label.setText(f"Multimedia File added, your file path is: {self.steg_multimedia_path}")

    def select_decode_multimedia(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Decode Multimedia", "",
                                                   "Multimedia Files (*.wav *.mp4 *.avi);;All Files (*)", options=options)
        if file_path:
            self.steg_multimedia_path = file_path
            self.encoded_multimedia_label.setText(f"Multimedia file selected: {self.steg_multimedia_path}")
        else:
            self.encoded_image_label.setText("Invalid image file. Please select a valid PNG or BMP image.")

    def remove_payload_file(self):
        self.steg_multimedia_path = ""
        self.encoded_image_label.clear()
        self.encoded_image_label.setText("Drag and drop your encoded multimedia file here (.wav, .mp4)")

    def decode_message(self):
        if self.steg_multimedia_path.endswith('.wav'):
            try:
                hidden_message = stego_audio_decode_text.decode_wav_message(self.steg_multimedia_path)
                self.decoded_text.setPlainText(hidden_message)
            except Exception as e:
                self.decoded_text.setPlainText(f"Error decoding message: {e}")
        else:
            self.encoded_image_label.setText("Unsupported file type for decoding")
            self.steg_multimedia_path = ""

    def backbutton_clear(self):
        self.steg_multimedia_path = ""
        self.decoded_text.setText("Your Secret Message lies here after decoding")
        self.encoded_image_label.clear()
        self.encoded_image_label.setText("Drag and drop your encoded multimedia file here (.wav, .mp4)")

    def on_back_button_clicked(self):
        self.backbutton_clear()
        self.switch_to_steganography()
