import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Лабораторная_3')
        self.setGeometry(100, 100, 800, 600)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.open_button = QPushButton('Загрузить', self)
        self.open_button.clicked.connect(self.open_image)

        self.erode_button = QPushButton('Эрозия', self)
        self.erode_button.clicked.connect(self.apply_erosion)
        self.erode_button.setEnabled(False)

        self.dilate_button = QPushButton('Дилатация', self)
        self.dilate_button.clicked.connect(self.apply_dilation)
        self.dilate_button.setEnabled(False)

        self.opening_button = QPushButton('Открытие', self)
        self.opening_button.clicked.connect(self.apply_opening)
        self.opening_button.setEnabled(False)

        self.closing_button = QPushButton('Закрытие', self)
        self.closing_button.clicked.connect(self.apply_closing)
        self.closing_button.setEnabled(False)

        self.gradient_button = QPushButton('Градиент', self)
        self.gradient_button.clicked.connect(self.apply_gradient)
        self.gradient_button.setEnabled(False)

        button_layout = QVBoxLayout()
        button_layout.addWidget(self.open_button)
        button_layout.addWidget(self.erode_button)
        button_layout.addWidget(self.dilate_button)
        button_layout.addWidget(self.opening_button)
        button_layout.addWidget(self.closing_button)
        button_layout.addWidget(self.gradient_button)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.image = None

    def open_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "",
                                                   "Images (*.png *.xpm *.jpg *.bmp);;All Files (*)", options=options)
        if file_name:
            self.image = cv2.imread(file_name)
            self.display_image(self.image)
            self.erode_button.setEnabled(True)
            self.dilate_button.setEnabled(True)
            self.opening_button.setEnabled(True)
            self.closing_button.setEnabled(True)
            self.gradient_button.setEnabled(True)

    def display_image(self, img):
        qformat = QImage.Format_Indexed8
        if len(img.shape) == 3:
            if img.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        out_image = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
        out_image = out_image.rgbSwapped()
        self.image_label.setPixmap(QPixmap.fromImage(out_image).scaledToHeight(500))
        self.image_label.setScaledContents(True)

    def apply_erosion(self):
        if self.image is not None:
            kernel = np.ones((5, 5), np.uint8)
            eroded_image = cv2.erode(self.image, kernel, iterations=1)
            self.display_image(eroded_image)

    def apply_dilation(self):
        if self.image is not None:
            kernel = np.ones((5, 5), np.uint8)
            dilated_image = cv2.dilate(self.image, kernel, iterations=1)
            self.display_image(dilated_image)

    def apply_opening(self):
        if self.image is not None:
            kernel = np.ones((5, 5), np.uint8)
            opening_image = cv2.morphologyEx(self.image, cv2.MORPH_OPEN, kernel)
            self.display_image(opening_image)

    def apply_closing(self):
        if self.image is not None:
            kernel = np.ones((5, 5), np.uint8)
            closing_image = cv2.morphologyEx(self.image, cv2.MORPH_CLOSE, kernel)
            self.display_image(closing_image)

    def apply_gradient(self):
        if self.image is not None:
            kernel = np.ones((5, 5), np.uint8)
            gradient_image = cv2.morphologyEx(self.image, cv2.MORPH_GRADIENT, kernel)
            self.display_image(gradient_image)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
