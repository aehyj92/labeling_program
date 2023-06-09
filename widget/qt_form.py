from PyQt5 import QtCore, QtWidgets


class Ui_Load(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Load Image File")
        Dialog.resize(465, 376)
        Dialog.setStyleSheet('font-family: Arial')
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(100, 320, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.toolButton = QtWidgets.QToolButton(Dialog)
        self.toolButton.setGeometry(QtCore.QRect(230, 10, 21, 21))
        self.toolButton.setObjectName("toolButton")
        self.textEdit_4 = QtWidgets.QTextEdit(Dialog)
        self.textEdit_4.setGeometry(QtCore.QRect(40, 40, 381, 21))
        self.textEdit_4.setObjectName("textEdit_4")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(40, 10, 180, 21))
        self.label_3.setObjectName("label_3")
        self.listWidget = QtWidgets.QListWidget(Dialog)
        self.listWidget.setGeometry(QtCore.QRect(20, 100, 421, 201))
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(40, 70, 171, 23))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.toolButton.setText(_translate("Dialog", "..."))
        self.textEdit_4.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Gulim\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Put in Dataset\'s Directory</p></body></html>"))
        self.label_3.setText(_translate("Dialog", "Put in Dataset\'s Directory"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("Dialog", "Image Set"))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.pushButton.setText(_translate("Dialog", "Image File Select"))


class Ui_LeftForm(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(281, 778)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(0, 10, 281, 31))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 0, 271, 31))
        self.label.setObjectName("label")

        
        
        
        self.listWidget = QtWidgets.QListWidget(Form)
        self.listWidget.setGeometry(QtCore.QRect(10, 50, 261, 341))
        self.listWidget.setObjectName("listView")
        self.line = QtWidgets.QFrame(Form)
        self.line.setGeometry(QtCore.QRect(0, 400, 281, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(10, 420, 101, 21))
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(70, 450, 201, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.listWidget_2 = QtWidgets.QListWidget(Form)
        self.listWidget_2.setGeometry(QtCore.QRect(10, 550, 261, 121))
        self.listWidget_2.setObjectName("listView_2")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(200, 480, 71, 23))
        self.pushButton.setObjectName("pushButton")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(10, 450, 51, 21))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(10, 480, 51, 21))
        self.label_4.setObjectName("label_4")
        self.listWidget_3 = QtWidgets.QListWidget(Form)
        self.listWidget_3.setGeometry(QtCore.QRect(70, 480, 121, 21))
        self.listWidget_3.setObjectName("listView_3")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(10, 520, 81, 21))
        self.label_5.setObjectName("label_5")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(160, 510, 31, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setStyleSheet('background-color: rgb(255, 0, 0)')
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(200, 510, 31, 31))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setStyleSheet('background-color: rgb(0, 255, 0)')
        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(240, 510, 31, 31))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.setStyleSheet('background-color: rgb(0, 0, 255)')
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(10, 700, 101, 21))
        self.label_6.setObjectName("label_6")
        


###########

##########        
        
        
        
        # self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        # self.lineEdit_2.setGeometry(QtCore.QRect(227, 740, 40, 30))
        # self.lineEdit_2.setObjectName("lineEdit_2")
        self.line_2 = QtWidgets.QFrame(Form)
        self.line_2.setGeometry(QtCore.QRect(0, 680, 281, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.pushButton_5 = QtWidgets.QPushButton(Form)
        self.pushButton_5.setGeometry(QtCore.QRect(185, 420, 85, 23))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(Form)
        self.pushButton_6.setGeometry(QtCore.QRect(100, 420, 80, 23))
        self.pushButton_6.setObjectName("pushButton_5")

        self.line_3 = QtWidgets.QFrame(Form)
        self.line_3.setGeometry(QtCore.QRect(0, 775, 281, 16))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")

        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(10, 790, 101, 21))
        self.label_7.setObjectName("label_7")

        
        
        
        
        

        # self.lineEdit_3 = QtWidgets.QLineEdit(Form)
        # self.lineEdit_3.setGeometry(QtCore.QRect(227, 820, 40, 30))
        # self.lineEdit_3.setObjectName("lineEdit_3")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        Form.setStyleSheet('font-family: Arial')
        self.label.setText(_translate("Form", "File List"))
        self.label_2.setText(_translate("Form", "Attribute"))
        self.lineEdit.setText(_translate("Form", "Default"))
        self.pushButton.setText(_translate("Form", "Select"))
        self.label_3.setText(_translate("Form", "Name"))
        self.label_4.setText(_translate("Form", "Color"))
        self.label_5.setText(_translate("Form", "Attribute List"))
        self.pushButton_2.setText(_translate("Form", "R"))
        self.pushButton_3.setText(_translate("Form", "G"))
        self.pushButton_4.setText(_translate("Form", "B"))
        
        self.pushButton_5.setText(_translate("Form", "Add"))
        self.pushButton_6.setText(_translate("Form", "Delete"))
        

class Ui_MergeJson(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Merge Json")
        Dialog.resize(324, 285)
        Dialog.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget = QtWidgets.QWidget(Dialog)
        self.centralwidget.setObjectName("centralwidget")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 40, 161, 21))
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(210, 210, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(30, 40, 81, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber.setGeometry(QtCore.QRect(30, 10, 131, 21))
        self.lcdNumber.setDigitCount(11)
        self.lcdNumber.setObjectName("lcdNumber")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(30, 70, 261, 131))
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(120, 40, 81, 23))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(210, 40, 81, 23))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(30, 210, 81, 23))

        self.pushButton_6.setObjectName("pushButton_6")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        Dialog.setStyleSheet('font-family: Arial')
        self.pushButton.setText(_translate("Dialog", "Help"))
        self.pushButton_3.setText(_translate("Dialog", "JSON File"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("Dialog", "JSON File List"))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.pushButton_4.setText(_translate("Dialog", "JSON DIR"))
        self.pushButton_5.setText(_translate("Dialog", "MERGE"))
        self.pushButton_6.setText(_translate("Dialog", "MERGE Opt"))

class Ui_MergeJsonDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Merge Json")
        Dialog.resize(510, 212)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(410, 30, 81, 241))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.textEdit_4 = QtWidgets.QTextEdit(Dialog)
        self.textEdit_4.setGeometry(QtCore.QRect(20, 70, 381, 21))
        self.textEdit_4.setObjectName("textEdit_4")
        self.textEdit_3 = QtWidgets.QTextEdit(Dialog)
        self.textEdit_3.setGeometry(QtCore.QRect(20, 150, 381, 21))
        self.textEdit_3.setObjectName("textEdit_3")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(20, 40, 251, 21))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(20, 120, 251, 21))
        self.label_4.setObjectName("label_4")
        self.toolButton = QtWidgets.QToolButton(Dialog)
        self.toolButton.setGeometry(QtCore.QRect(180, 40, 21, 21))
        self.toolButton.setObjectName("toolButton")
        self.action = QtWidgets.QAction(Dialog)
        self.action.setObjectName("action")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        Dialog.setStyleSheet('font-family: Arial')
        self.textEdit_4.setHtml(_translate("Dialog",
                                           "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                           "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                           "p, li { white-space: pre-wrap; }\n"
                                           "</style></head><body style=\" font-family:\'Gulim\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                           "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Put in Dataset\'s Directory</p></body></html>"))
        self.textEdit_3.setHtml(_translate("Dialog",
                                           "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                           "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                           "p, li { white-space: pre-wrap; }\n"
                                           "</style></head><body style=\" font-family:\'Gulim\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                           "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">new_via_style_json</p></body></html>"))
        self.label_3.setText(_translate("Dialog", "New JSON File\'s Location"))
        self.label_4.setText(_translate("Dialog", "Please Set new JSON File\'s Name"))
        self.toolButton.setText(_translate("Dialog", "..."))