import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget, QLabel


class SteganalysisScreen(QWidget):
    def __init__(self,switch_to_main):
        super().__init__()
        self.switch_to_main = switch_to_main
        self.layout = QVBoxLayout(self)

        self.back_button = QPushButton('Back')
        self.title_label = QLabel('Welcome to Analysis', self)

        self.back_button.clicked.connect(self.switch_to_main)

        self.layout.addWidget(self.back_button)
        self.layout.addWidget(self.title_label)