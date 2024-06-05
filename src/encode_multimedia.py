import os

import cv2
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QTextEdit, QFileDialog, QHBoxLayout, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QDropEvent
import stego_audio_encode_text


class EncodeMultimediaScreen(QWidget):
    def __init__(self, switch_to_steganography):
        super().__init__()

        self.switch_to_steganography = switch_to_steganography

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)  # Set margins for the main layout
        self.main_layout.setSpacing(10)  # Set spacing between widgets

        # Create back button and set its position
        self.back_button = QPushButton('Back', self)
        self.back_button.clicked.connect(self.on_back_button_clicked)
        self.back_button.setFixedSize(100, 50)
        self.back_button.move(20, 20)

        # Create payload layout
        self.payload_layout = QVBoxLayout()
        self.payload_label_layout = QHBoxLayout()
        self.payload_button_layout = QHBoxLayout()

        # Create label for drag-and-drop payload (text file or message)
        self.payload_label = QLabel("Drag and drop your payload (text file) here or type your message below", self)
        self.payload_label.setStyleSheet("QLabel { border: 2px dashed #aaa; }")
        self.payload_label.setAlignment(Qt.AlignCenter)
        self.payload_label.setFixedHeight(100)
        self.payload_label.setAcceptDrops(True)
        self.payload_label.dragEnterEvent = self.dragEnterEvent
        self.payload_label.dropEvent = self.payload_dropEvent

        # Create buttons to add file from explorer or remove file
        self.choose_payload_button = QPushButton('Add file', self)
        self.choose_payload_button.setFixedWidth(150)
        self.choose_payload_button.clicked.connect(self.select_payload_file)

        self.remove_file_button = QPushButton('Remove file', self)
        self.remove_file_button.setFixedWidth(150)
        self.remove_file_button.clicked.connect(self.remove_payload_file)

        self.bits_label = QLabel()
        self.bits_label.setText("Bits used:")
        self.bits_dropdown = QComboBox()
        self.bits_dropdown.addItems(["1", "2", "3", "4", "5", "6", "7", "8"])

        # Add widgets to payload layout
        self.payload_button_layout.addWidget(self.choose_payload_button)
        self.payload_button_layout.addWidget(self.remove_file_button)
        self.payload_button_layout.addWidget(self.bits_label)
        self.payload_button_layout.addWidget(self.bits_dropdown)
        self.payload_button_layout.setAlignment(Qt.AlignLeft)
        self.payload_label_layout.addWidget(self.payload_label)
        self.payload_layout.addLayout(self.payload_label_layout)
        self.payload_layout.addLayout(self.payload_button_layout)

        # Create text edit for typing secret message
        self.text_edit = QTextEdit(self)
        self.text_edit.setPlaceholderText("Or type your secret message here")
        self.text_edit.setFixedHeight(50)
        self.text_edit.setContentsMargins(20, 0, 20, 0)

        # Create a horizontal layout for cover object and encoded result
        self.cover_result_layout = QHBoxLayout()

        # Create label for drag-and-drop cover object (image)
        self.cover_label = QLabel("Drag and drop your cover multimedia here, the file path will be shown here:", self)
        self.cover_label.setStyleSheet("QLabel { border: 2px dashed #aaa; }")
        self.cover_label.setAlignment(Qt.AlignCenter)
        self.cover_label.setAcceptDrops(True)
        self.cover_label.dragEnterEvent = self.dragEnterEvent
        self.cover_label.dropEvent = self.cover_dropEvent

        self.result_label = QLabel("Encoded multimedia file path will be shown here", self)
        self.result_label.setStyleSheet("QLabel { border: 2px dashed #aaa; }")
        self.result_label.setAlignment(Qt.AlignCenter)

        # Add widgets to main layout (vertical)
        self.main_layout.addWidget(self.back_button)
        self.main_layout.addLayout(self.payload_layout)
        self.main_layout.addWidget(self.text_edit)
        self.cover_result_layout.addWidget(self.cover_label)
        self.cover_result_layout.addWidget(self.result_label)

        # Create a horizontal layout for the encode button and add stretchable spaces on both sides
        self.button_layout = QHBoxLayout()
        self.button_layout.addStretch(1)  # Add stretchable space before the button
        self.encode_button = QPushButton('Encode')
        self.encode_button.setFixedSize(200, 100)
        self.encode_button.clicked.connect(self.encode_audio_text)
        self.button_layout.addWidget(self.encode_button)
        self.button_layout.addStretch(1)  # Add stretchable space after the button

        # Add cover and result layout to main layout

        self.main_layout.addLayout(self.cover_result_layout)

        # Add the button layout to the main layout
        self.main_layout.addLayout(self.button_layout)

        # Set the main layout for the widget
        self.setLayout(self.main_layout)

        # File paths
        self.cover_multimedia_path = ""
        self.payload_data = ""

    def cover_dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls and urls[0].isLocalFile():
            self.cover_multimedia_path = urls[0].toLocalFile()
            self.cover_label.setText(f"Multimedia File added, your file path is: {self.cover_multimedia_path}")

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def payload_dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls and urls[0].isLocalFile():
            file_path = urls[0].toLocalFile()
            if file_path.endswith('.txt'):
                with open(file_path, 'r') as file:
                    self.payload_data = file.read()
                    self.payload_label.setText("Payload uploaded")
                # Disable text edit when a text file is dropped
                self.text_edit.setReadOnly(True)
            else:
                # Handle non-text files if needed
                pass

    def select_payload_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Payload File", "",
                                                   "Text Files (*.txt);;All Files (*)", options=options)
        if file_path:
            with open(file_path, 'r') as file:
                self.payload_data = file.read()
                self.text_edit.setPlainText(self.payload_data)
            # Disable text edit when a text file is selected
            self.text_edit.setReadOnly(True)

    def select_cover_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Cover Image", "",
                                                   "Images (*.png *.jpg *.bmp);;All Files (*)", options=options)
        if file_path:
            self.cover_multimedia_path = file_path
            self.cover_label.setText(f"Cover image selected: {file_path}")
            # Handle cover image file path (file_path)
            # For example, you could display the file path or use it for encoding

    def remove_payload_file(self):
        self.text_edit.setReadOnly(False)
        self.payload_data = ""
        self.payload_label.clear()  # Clear the payload label
        self.payload_label.setText("Drag and drop your payload (text file) here or type your message below")

    def on_back_button_clicked(self):
        self.backbutton_clear()
        self.switch_to_steganography()

    def backbutton_clear(self):
        self.cover_multimedia_path = ""
        self.payload_data = ""
        self.payload_label.setText("Drag and drop your payload (text file) here or type your message below")
        self.text_edit.setPlaceholderText("Or type your secret message here")
        self.cover_label.setText("Drag and drop your cover multimedia here, the file path will be shown here:")
        self.result_label.setText("Encoded multimedia file path will be shown here")

    def encode_audio_text(self):
        if not self.cover_multimedia_path or not self.payload_data:
            self.result_label.setText("Missing, cover multimedia file or payload text file")
            return
        
        output_audio = 'output.wav'
        # Number of bits to encode with
        lsb_num = int(self.bits_dropdown.currentText())

        try:
            stego_audio_encode_text.encode_audio(self.cover_multimedia_path, self.payload_data, output_audio, lsb_num)
            self.result_label.setText(f"Encoding completed. File is saved at {output_audio}")
        except Exception as e:
            self.result_label.setText(f"Error during encoding: {str(e)}")
            print(str(e))