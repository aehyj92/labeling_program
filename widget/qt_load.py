import os
from PyQt5.QtWidgets import QFileDialog, QDialog
from widget.qt_form import Ui_Load

class LoadDialog(QDialog, Ui_Load):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.image_file = []
        self.image_flag = 0

        
        self.image_files = []
        self.images = []
        self.item = {'.jpg', '.bmp', '.png','.tiff'}
        self.buttonBox.accepted.connect(self.accepted_button)
        self.buttonBox.rejected.connect(self.rejected_button)
        self.toolButton.clicked.connect(self.image_direc)
        self.pushButton.clicked.connect(self.image_file_find)

    def accepted_button(self):
        self.accept()

    def rejected_button(self):
        self.reject()

    def showModal(self):
        return super().exec_()

    def image_direc(self):
        
        options = QFileDialog.Options()  
        options |= QFileDialog.ShowDirsOnly
        self.image_dir = (QFileDialog.getExistingDirectory(self))
        if self.image_dir == "":
            
            return super()

        self.images = []
        self.images.append(os.listdir(self.image_dir))
        for s in self.images[0]:
            for i in self.item:
                if i in s:
                    self.image_files.append(self.image_dir + '/' + s)
                    self.listWidget.addItem(self.image_dir + '/' + s)
        self.textEdit_4.setText(self.image_dir)

    def image_file_find(self):
        
        options = QFileDialog.Options()  
        options |= QFileDialog.ShowDirsOnly
        self.image_file.append(QFileDialog.getOpenFileNames(self, "Open Image Data", filter="(*.jpg;*.png;*bmp;*tiff;)"))

        if self.image_file[0][0] == "":
            return super()

        for image_dir in self.image_file[0][0]:
            if '.jpg' or '.png' or '.bmp' or '.tiff' in image_dir:
                self.listWidget.addItem(image_dir)
                self.image_files.append(image_dir)
        self.image_file = []