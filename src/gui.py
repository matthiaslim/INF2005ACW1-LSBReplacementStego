import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
import home, steganalysis, steganography, encode_images, decode_options, encode_options, encode_multimedia, decode_images, decode_multimedia


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Steganography Tool')

        # stack widget
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Screens
        self.main_screen = home.MainScreen(self.show_steganography_screen, self.show_steganalysis_screen)
        self.steganography_screen = steganography.SteganographyScreen(self.show_main_screen,
                                                                      self.show_encode_options_screen,
                                                                      self.show_decode_options_screen)
        self.encode_options_screen = encode_options.SteganographyEncodeOptionScreen(self.show_steganography_screen,
                                                                                    self.show_encode_images_screen,
                                                                                    self.show_encode_multimedia_screen)
        self.decode_options_screen = decode_options.SteganographyDecodeOptionScreen(self.show_steganography_screen,
                                                                                    self.show_decode_images_screen,
                                                                                    self.show_decode_multimedia_screen)
        self.steganalysis_screen = steganalysis.SteganalysisScreen(self.show_main_screen)
        self.encode_images_screen = encode_images.EncodeImageScreen(self.show_encode_options_screen)
        self.encode_multimedia_screen = encode_multimedia.EncodeMultimediaScreen(self.show_encode_options_screen)
        self.decode_images_screen = decode_images.DecodeImageScreen(self.show_decode_options_screen)
        self.decode_multimedia_screen = decode_multimedia.DecodeMultimediaScreen(self.show_decode_options_screen)

        self.stacked_widget.addWidget(self.main_screen)
        self.stacked_widget.addWidget(self.steganography_screen)
        self.stacked_widget.addWidget(self.steganalysis_screen)
        self.stacked_widget.addWidget(self.encode_images_screen)
        self.stacked_widget.addWidget(self.encode_multimedia_screen)
        self.stacked_widget.addWidget(self.encode_options_screen)
        self.stacked_widget.addWidget(self.decode_options_screen)
        self.stacked_widget.addWidget(self.decode_images_screen)
        self.stacked_widget.addWidget(self.decode_multimedia_screen)



        self.showMaximized()
        self.show()

    def show_main_screen(self):
        self.stacked_widget.setCurrentWidget(self.main_screen)

    def show_steganography_screen(self):
        self.stacked_widget.setCurrentWidget(self.steganography_screen)

    def show_steganalysis_screen(self):
        self.stacked_widget.setCurrentWidget(self.steganalysis_screen)

    def show_encode_images_screen(self):
        self.stacked_widget.setCurrentWidget(self.encode_images_screen)

    def show_encode_multimedia_screen(self):
        self.stacked_widget.setCurrentWidget(self.encode_multimedia_screen)

    def show_encode_options_screen(self):
        self.stacked_widget.setCurrentWidget(self.encode_options_screen)

    def show_decode_options_screen(self):
        self.stacked_widget.setCurrentWidget(self.decode_options_screen)

    def show_decode_images_screen(self):
        self.stacked_widget.setCurrentWidget(self.decode_images_screen)
    
    def show_decode_multimedia_screen(self):
        self.stacked_widget.setCurrentWidget(self.decode_multimedia_screen)



def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
