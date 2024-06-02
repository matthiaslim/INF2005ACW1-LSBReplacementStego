import os
import cv2
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QTextEdit, QFileDialog, QHBoxLayout, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QDropEvent
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import steganalysis_rgb_compare
import random


class SteganalysisScreen(QWidget):
    def __init__(self,switch_to_main):
        super().__init__()
        self.switch_to_main = switch_to_main

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(10, 20, 10, 20)  # Set margins for the main layout
        self.main_layout.setSpacing(10)  # Set spacing between widgets

        # Back Button
        self.back_button = QPushButton('Back', self)
        self.back_button.clicked.connect(self.on_back_button_clicked)
        self.back_button.setFixedSize(100,50)
        self.back_button.move(20,20)
        
        #Steg layout (contains the steganalysis and image loading)
        self.steg_layout = QHBoxLayout()
        self.file_layout = QVBoxLayout()

        # Original file widgets and loadout
        self.original_file_layout = QVBoxLayout()

        self.original_image_label = QLabel("Drag and drop your original file here")
        self.original_image_label.setStyleSheet("QLabel { border: 2px dashed #aaa; }")
        self.original_image_label.setAlignment(Qt.AlignCenter)
        #self.original_image_label.setFixedHeight(300)
        self.original_image_label.setAcceptDrops(True)
        self.original_image_label.dragEnterEvent = self.dragEnterEvent
        self.original_image_label.dropEvent = self.original_dropEvent

        self.choose_original_image_button = QPushButton('Add file', self)
        self.choose_original_image_button.setFixedWidth(150)
        self.choose_original_image_button.clicked.connect(self.select_original_file)

        self.remove_original_image_button = QPushButton('Remove file', self)
        self.remove_original_image_button.setFixedWidth(150)
        self.remove_original_image_button.clicked.connect(self.remove_original_file)

        self.original_buttons_layout = QHBoxLayout()
        self.original_buttons_layout.addWidget(self.choose_original_image_button)
        self.original_buttons_layout.addWidget(self.remove_original_image_button)
        self.original_buttons_layout.setAlignment(Qt.AlignLeft)
        
        self.original_file_label_layout = QVBoxLayout()
        self.original_file_label_layout.addWidget(self.original_image_label)
        self.original_file_layout.addLayout(self.original_file_label_layout)
        self.original_file_layout.addLayout(self.original_buttons_layout)
        
        # Suspected file widgets and loadout
        self.suspected_file_layout = QVBoxLayout()

        self.suspected_image_label = QLabel("Drag and drop your suspected file here")
        self.suspected_image_label.setStyleSheet("QLabel { border: 2px dashed #aaa; }")
        self.suspected_image_label.setAlignment(Qt.AlignCenter)
        #self.suspected_image_label.setFixedHeight(300)
        self.suspected_image_label.setAcceptDrops(True)
        self.suspected_image_label.dragEnterEvent = self.dragEnterEvent
        self.suspected_image_label.dropEvent = self.suspected_dropEvent

        self.choose_suspected_image_button = QPushButton('Add file', self)
        self.choose_suspected_image_button.setFixedWidth(150)
        self.choose_suspected_image_button.clicked.connect(self.select_suspected_file)

        self.remove_suspected_image_button = QPushButton('Remove file', self)
        self.remove_suspected_image_button.setFixedWidth(150)
        self.remove_suspected_image_button.clicked.connect(self.remove_suspected_file)

        self.suspected_buttons_layout = QHBoxLayout()
        self.suspected_buttons_layout.addWidget(self.choose_suspected_image_button)
        self.suspected_buttons_layout.addWidget(self.remove_suspected_image_button)
        self.suspected_buttons_layout.setAlignment(Qt.AlignLeft)
        
        self.suspected_file_layout.addWidget(self.suspected_image_label)
        self.suspected_file_layout.addLayout(self.suspected_buttons_layout)

        self.file_layout.addLayout(self.original_file_layout)
        self.file_layout.addLayout(self.suspected_file_layout)


        # Label for matplot
        self.figure = plt.figure()
        self.matplot_label = FigureCanvas(self.figure)
        self.matplot_label.setStyleSheet("QLabel { border: 2px dashed #aaa; }")
        self.matplot_label.setFixedWidth(1200)

        self.steg_layout.addLayout(self.file_layout)
        self.steg_layout.addWidget(self.matplot_label)

        self.main_layout.addWidget(self.back_button)

        # Analyse Button
        self.button_layout = QHBoxLayout()
        self.button_layout.addStretch(1)
        self.analyse_button = QPushButton('Analyse', self)
        self.analyse_button.setFixedSize(200,100)
        self.analyse_button.clicked.connect(self.analyse_images)
        self.button_layout.addWidget(self.analyse_button)
        self.button_layout.addStretch(1)

        self.main_layout.addWidget(self.back_button)
        self.main_layout.addLayout(self.steg_layout)
        self.main_layout.addLayout(self.button_layout)

        self.setLayout(self.main_layout)

        self.original_path = ""
        self.suspected_path = ""

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def original_dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls and urls[0].isLocalFile():
            self.original_path = urls[0].toLocalFile()
            pixmap = QPixmap(self.original_path)
            if not pixmap.isNull():
                max_width = self.original_image_label.width()
                max_height = self.original_image_label.height()
                self.original_image_label.setPixmap(pixmap.scaled(max_width,max_height,Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                self.original_image_label.clear()
    
    def suspected_dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls and urls[0].isLocalFile():
            self.suspected_path = urls[0].toLocalFile()
            pixmap = QPixmap(self.suspected_path)
            if not pixmap.isNull():
                max_width = self.suspected_image_label.width()
                max_height = self.suspected_image_label.height()
                self.suspected_image_label.setPixmap(pixmap.scaled(max_width,max_height,Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                self.suspected_image_label.clear()
    
    def select_original_file(self):
        options = QFileDialog.Option()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Cover Image", "",
                                                   "Images (*.png *.jpg *.bmp);;All Files (*)", options=options)
        if file_path:
            self.original_path = file_path
            pixmap = QPixmap(self.original_path)
            if not pixmap.isNull():
                max_width = self.original_image_label.width()
                max_height = self.original_image_label.height()
                self.original_image_label.setPixmap(pixmap.scaled(max_width,max_height,Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                self.original_image_label.clear()
    
    def select_suspected_file(self):
        options = QFileDialog.Option()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Cover Image", "",
                                                   "Images (*.png *.jpg *.bmp);;All Files (*)", options=options)
        if file_path:
            self.suspected_path = file_path
            pixmap = QPixmap(self.suspected_path)
            if not pixmap.isNull():
                max_width = self.suspected_image_label.width()
                max_height = self.suspected_image_label.height()
                self.suspected_image_label.setPixmap(pixmap.scaled(max_width,max_height,Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                self.suspected_image_label.clear()

    def remove_original_file(self):
        self.original_path = ""
        self.original_image_label.clear()
        self.original_image_label.setText("Drag and drop your original file here")

    def remove_suspected_file(self):
        self.suspected_path = ""
        self.suspected_image_label.clear()
        self.suspected_image_label.setText("Drag and drop your suspected file here")

    def on_back_button_clicked(self):
        self.backbutton_clear()
        self.switch_to_main()
    
    def backbutton_clear(self):
        self.original_path = ""
        self.suspected_path = ""
        self.original_image_label.setText("Drag and drop your original file here")
        self.suspected_image_label.setText("Drag and drop your suspected file here")
    
    def analyse_images(self):
        self.figure.clear()
        steganalysis_rgb_compare.compare_images(self.original_path, self.suspected_path)
        # random data
        data = [random.random() for i in range(10)]
        ax = self.figure.add_subplot(111)
  
        # plot data
        ax.plot(data, '*-')
        self.matplot_label.draw()
    
