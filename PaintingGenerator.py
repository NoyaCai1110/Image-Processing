import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import cv2
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.original_image_path = ""
        self.setWindowTitle('stylize')
        self.resize(1260, 500)
        
        menubar = self.menuBar()
        file_menu = menubar.addMenu('file')
        file_menu.addAction("open")
        file_menu.triggered.connect(self.openFile)

        self.original_image_label = QLabel(self)
        self.original_image_label.setGeometry(20, 30, 600, 400)
        self.original_image_label.setFrameShape(QFrame.Box)
        self.original_image_label.setFrameShadow(QFrame.Raised)
        self.original_image_label.setStyleSheet('border-width: 1px;border-style: solid;border-color: rgb(255, 170, 0);')
        self.original_image_label.setAlignment(Qt.AlignCenter)
        self.original_image_label.setText("input image")

        self.animated_image_label = QLabel(self)
        self.animated_image_label.setGeometry(640, 30, 600, 400)
        self.animated_image_label.setFrameShape(QFrame.Box)
        self.animated_image_label.setFrameShadow(QFrame.Raised)
        self.animated_image_label.setStyleSheet('border-width: 1px;border-style: solid;border-color: rgb(255, 170, 0);')
        self.animated_image_label.setAlignment(Qt.AlignCenter)
        self.animated_image_label.setText("result image")

        self.btn_image1 = QPushButton(self)
        self.btn_image1.setGeometry(100, 450, 93, 28)
        self.btn_image1.setText("animate")
        self.btn_image1.clicked.connect(self.comic)

        self.btn_image2 = QPushButton(self)
        self.btn_image2.setGeometry(200, 450, 93, 28)
        self.btn_image2.setText("sketch")
        self.btn_image2.clicked.connect(self.sketch)

        self.btn_image3 = QPushButton(self)
        self.btn_image3.setGeometry(300, 450, 120, 28)
        self.btn_image3.setText("watercolor")
        self.btn_image3.clicked.connect(self.watercolor)
    
    def comic(self):
        img = cv2.imread(self.original_image_path)
        blur_kernal_size = max(int(min(img.shape[0], img.shape[1]) / 75), 3)
        for _ in range(2):
            img = cv2.bilateralFilter(img, blur_kernal_size, 75, 75)
        canny = cv2.Canny(img, 30, 150)
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                if canny[i][j] == 255:
                    img[i][j][:] = 0
        img = img.astype(np.float32) / 255.0
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
        img[:, :, 2] = 1.5 * img[:, :, 2]
        img[:, :, 2][img[:, :, 2] > 1] = 1
        img = cv2.cvtColor(img, cv2.COLOR_HLS2BGR)
        img = img * 255.0
        img = img.astype(np.uint8)
        result = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        animated_image = QImage(result.data, result.shape[1], result.shape[0], QImage.Format_RGB888)
        animated_pixmap = QPixmap.fromImage(animated_image).scaled(self.animated_image_label.width(), self.animated_image_label.height())
        self.animated_image_label.setPixmap(animated_pixmap)
    
    def sketch(self):
        img = cv2.imread(self.original_image_path)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_gray = cv2.medianBlur(img_gray, 5)
        edges = cv2.Laplacian(img_gray, cv2.CV_8U, ksize=5)
        _, result = cv2.threshold(edges, 100, 255, cv2.THRESH_BINARY_INV)
        sketch_image = QImage(result.data, result.shape[1], result.shape[0], QImage.Format_Indexed8)
        sketch_pixmap = QPixmap.fromImage(sketch_image).scaled(self.animated_image_label.width(), self.animated_image_label.height())
        self.animated_image_label.setPixmap(sketch_pixmap)
    
    def watercolor(self):
        img = cv2.imread(self.original_image_path)
        result = cv2.stylization(img, sigma_s=60, sigma_r=0.6)
        result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
        watercolor_image = QImage(result.data, result.shape[1], result.shape[0], QImage.Format_RGB888)
        watercolor_pixmap = QPixmap.fromImage(watercolor_image).scaled(self.animated_image_label.width(), self.animated_image_label.height())
        self.animated_image_label.setPixmap(watercolor_pixmap)

    def openFile(self):
        self.original_image_path, _ = QFileDialog.getOpenFileName(self, 'open file', '.', 'pictures(*.jpg *.png)')
        original_image = QPixmap(self.original_image_path).scaled(self.original_image_label.width(), self.original_image_label.height())
        self.original_image_label.setPixmap(original_image)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())