import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget
from views import home,steganalysis,steganography, encode, decode


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Steganography Tool')

        # stack widget
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Screens
        self.main_screen = home.MainScreen(self.show_steganography_screen, self.show_steganalysis_screen)
        self.steganography_screen = steganography.SteganographyScreen(self.show_main_screen, self.show_encode_screen, self.show_decode_screen)
        self.steganalysis_screen = steganalysis.SteganalysisScreen(self.show_main_screen)
        self.encode_screen = encode.EncodeScreen(self.show_steganography_screen)
        self.decode_screen = decode.DecodeScreen(self.show_steganography_screen)

        self.stacked_widget.addWidget(self.main_screen)
        self.stacked_widget.addWidget(self.steganography_screen)
        self.stacked_widget.addWidget(self.steganalysis_screen)
        self.stacked_widget.addWidget(self.encode_screen)
        self.stacked_widget.addWidget(self.decode_screen)

        self.setFixedSize(1920, 1080)
        self.show()

    def show_main_screen(self):
        self.stacked_widget.setCurrentWidget(self.main_screen)

    def show_steganography_screen(self):
        self.stacked_widget.setCurrentWidget(self.steganography_screen)

    def show_steganalysis_screen(self):
        self.stacked_widget.setCurrentWidget(self.steganalysis_screen)

    def show_encode_screen(self):
        self.stacked_widget.setCurrentWidget(self.encode_screen)

    def show_decode_screen(self):
        self.stacked_widget.setCurrentWidget(self.decode_screen)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
