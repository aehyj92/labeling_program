from numpy import arange
from widget.qt_leftside import global_item
import qt_option
import os
import json
import test
import pandas as pd
from PyQt5.QtWidgets import *

from pysys import dataset
from widget import qt_load, qt_image, qt_central, qt_merge

from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QDesktopWidget, QFileDialog
from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtCore import Qt
from widget import qt_leftside
from widget import qt_form
from PyQt5.QtWidgets import QWidget

from PyQt5.QtWidgets import QWidget, QColorDialog
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtCore import Qt
from widget import qt_form
from PyQt5 import QtCore, QtWidgets

class ToolWindow(QMainWindow,QWidget,qt_form.Ui_LeftForm):
    def __init__(self):
        super().__init__()
        self.dataset = None

        self.json_data = {}
        self.json_path = []

        
        self.mode = qt_option.EditMode()

        
        self.central_widget = qt_central.CentralWidget(self.mode)
        self.setCentralWidget(self.central_widget)
        self.image_widget = self.central_widget.image_widget
        self.leftside_widget = self.central_widget.leftside_widget
        # self.tmp3=self.leftside_widget.setupUi(self)
        # self.tmp=qt_leftside.LeftSideWidget(self.mode,self)
        # self.tmp2=qt_form.Ui_LeftForm()
        self.listWidget = QtWidgets.QListWidget()



        
        self._create_action()

        
        self._create_menu()

        
        self._create_toolbar()

        
        self._connect()

        
        self.statusBar().showMessage('Ready')

        
        self.setWindowTitle('Quick Point Annotation Tool')

        
        self.setWindowIcon(QIcon("./icon/icon.png"))

        
        self.resize(1280, 780)

        
        self.show()
        self._center()

        
        self.activateWindow()

    def load_data(self, dataset):
        if dataset.image_count < 1:
            return
        self.dataset = dataset
        self.image_widget.load_data(dataset)
        self.leftside_widget.load_filelist(dataset)
        self.dataset.import_json_dict(self.json_data)

    def load_json(self):
        '''
        json파일을 load 하면 check box에 checked 기능 추가 
        '''

        
        self.json_data.clear()

        
        options = QFileDialog.Options()  
        options |= QFileDialog.ShowDirsOnly

        json_file_dirs = QFileDialog.getOpenFileNames(self,
                         "Open Json File", filter = "json(*.json)")
        json_file_dirs = json_file_dirs[0]

        for dir in json_file_dirs:
            
            if not os.path.exists(dir):
                return super()

        
        if len(json_file_dirs) < 1:
            return super()

        
        elif len(json_file_dirs) == 1:
            self.json_path = json_file_dirs

        for json_file_dir in json_file_dirs:
            with open(json_file_dir, 'r') as LD_json:
                loaded_json_file = json.load(LD_json)

            
            self.json_data.update(loaded_json_file)
        ################
        try:
            for i,j in zip(self.dataset.image_dirs,arange(len(self.dataset.image_dirs))):
                x=str(os.path.basename(i))
                if list(self.json_data[f'{x}']["regions"].values()):
                    if list(self.json_data[f'{x}']["regions"].values())[0]['shape_attributes']['name']=='polygon' or 'point':
                        load_item=global_item[-1][j]
                        
                        load_item.setCheckState(Qt.Checked)
                        self.listWidget.addItem(load_item)    
                    # elif list(self.json_data[f'{x}']["regions"].values())[0]['shape_attributes']['name']=='point':
                    #     load_item=global_item[-1][j]
                        
                    #     load_item.setCheckState(Qt.Checked)
                    #     self.listWidget.addItem(load_item)                          
        except:
            print('json file is empty')
        #################
        if self.dataset is not None:
            self.dataset.reset()
            self.dataset.import_json_dict(self.json_data)

            
            self.image_widget.redraw()

            

    def save_csv(self, path = ""):
        if self.dataset is None:
            return

        image_list = self.dataset.out_metadata_to_csv()
        csv_data = pd.DataFrame(image_list)
        csv_data.columns = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']

        CSV_DIR = path
        if path == "":
            CSV_DIR = os.getcwd()
            csv_data.to_csv(CSV_DIR + '/new_csv.csv', index=None, na_rep='NaN', encoding='utf-8')
        else:
            csv_data.to_csv(CSV_DIR, index=None, na_rep='NaN', encoding='utf-8')

    def save_new_csv(self):
        if self.dataset is None:
            return

        path = QFileDialog.getSaveFileName(self, 'Save csv File', filter="csv(*.csv)")
        path = path[0]

        if path:
            self.save_csv(path)
        else:
            return super()

    def save_json(self, path = ""):
        if self.dataset is None:
            return

        if path == "" and (len(self.json_path) != 1 or \
           not os.path.exists(self.json_path[0])):
            self.save_new_json()
            return
        elif path == "":
            path = self.json_path[0]

        dict_info = self.dataset.out_metadata_to_dict()
        JSON_DIR = path

        if os.path.exists(JSON_DIR) is True: 
            json_annotation = json.load(open(JSON_DIR))
            json_annotation.update(dict_info)
            dict_info = json_annotation

        with open(JSON_DIR, 'w') as outfile:
            json.dump(dict_info, outfile, indent = '\t')

        self.json_path.clear()
        self.json_path = [path]

    def save_new_json(self):
        if self.dataset is None:
            return

        path = QFileDialog.getSaveFileName(self, 'Save Json File', filter = "json(*.json)")
        path = path[0]

        if path:
            self.save_json(path)
        else:
            return super()

    def cancel_json(self):
        if len(self.json_data) > 0:
            self.dataset.cancel_json_dict()
            for i in self.json_data:
                self.json_data[i]['regions'] = []
            super()
        else:
            return super()

    # def calibration(self):
    #     print('calibration')

    def merge_json(self):
        merge_win = qt_merge.MergeDialog()
        merge_win.showModal()

    def closeEvent(self, QCloseEvent):
        re = QMessageBox.question(self, "종료 확인", "\0\0\0\0\0\0\0종료 하시겠습니까?\n (저장하지 않은 정보는 유실됩니다.)",
                    QMessageBox.Yes|QMessageBox.No)

        if re == QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()  





    def _create_action(self):
        self.action = {}
     
        exitAction = QAction(QIcon('./icon/exit.png'), 'Save/Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.save_new_json)  
        exitAction.triggered.connect(qApp.quit)
        self.action['exit'] = exitAction

        loadAction = QAction(QIcon('./icon/load.png'),'Load', self)
        loadAction.setShortcut('Ctrl+L')
        loadAction.setStatusTip('Load Image File')
        loadAction.triggered.connect(self._action_load_image)
        self.action['load'] = loadAction

        selectMode0 = QAction(QIcon('./icon/hand.png'), 'Select/Search', self)
        selectMode0.setShortcut('1')
        selectMode0.setStatusTip('Select/Search')
        selectMode0.triggered.connect(lambda x: [self.mode.set_mode(0), self.image_widget.view.refresh()])
        self.action['mode0'] = selectMode0

        selectMode1 = QAction(QIcon('./icon/polygon.png'), 'Draw Polygon', self)
        selectMode1.setShortcut('2')
        selectMode1.setStatusTip('Draw Polygon')
        selectMode1.triggered.connect(lambda x: [self.mode.set_mode(1), self.image_widget.view.refresh()])
        self.action['mode1'] = selectMode1

        selectMode2 = QAction(QIcon('./icon/paint.png'), 'Draw Point', self)
        selectMode2.setShortcut('3')
        selectMode2.setStatusTip('Draw Point')
        selectMode2.triggered.connect(lambda x: [self.mode.set_mode(5), self.image_widget.view.refresh()])
        self.action['mode2'] = selectMode2

        
        
        
        
        

        
        
        
        
        

        nextImage = QAction(QIcon('./icon/next.png'), 'Next', self)
        nextImage.setShortcut('E')
        nextImage.setStatusTip('Select Next Image')
        nextImage.triggered.connect(lambda x: self.image_widget.next_image())
        self.action['next'] = nextImage

        prevImage = QAction(QIcon('./icon/prev.png'), 'Prev', self)
        prevImage.setShortcut('W')
        prevImage.setStatusTip('Select Previous Image')
        prevImage.triggered.connect(lambda x: self.image_widget.prev_image())
        self.action['prev'] = prevImage

        importJson = QAction(QIcon('./icon/import_json.png'), '&Import JSON..', self)
        importJson.setShortcut('Ctrl+J')
        importJson.setStatusTip('Import JSON File')
        importJson.triggered.connect(self.load_json)
        self.action['import'] = importJson

        saveJson = QAction(QIcon('./icon/save.png'), '&Save', self)
        saveJson.setShortcut('Ctrl+S')
        saveJson.setStatusTip('Save JSON File')
        saveJson.triggered.connect(lambda x: self.save_json())
        self.action['saveJSON'] = saveJson

        saveNewJson = QAction(QIcon('./icon/saveas.png'), '&Save As..', self)
        saveNewJson.setShortcut('Ctrl+Shift+S')
        saveNewJson.setStatusTip('Save New JSON File')
        saveNewJson.triggered.connect(self.save_new_json)
        self.action['saveAs'] = saveNewJson

        # mergeJson = QAction(QIcon('./icon/merge_json.png'), '&Merge Json', self)
        # mergeJson.setShortcut('Ctrl+M')
        # mergeJson.setStatusTip('Merge Json File')
        # mergeJson.triggered.connect(self.merge_json)
        # self.action['merge'] = mergeJson

        # cancelJson = QAction(QIcon('./icon/cancel_json.png'), '&Cancel JSON', self)
        # cancelJson.setStatusTip('cancel')
        # cancelJson.triggered.connect(self.cancel_json)
        # self.action['cancel'] = cancelJson

        # calibration = QAction(QIcon('./icon/calibration.png'), '&Image Calibration', self)
        # calibration.setStatusTip('Create New Calibrate Image')
        # calibration.triggered.connect(self.calibration)
        # self.action['calibration'] = calibration

        
        
        
        
        

        
        
        
        

        
        
        
        

    def _create_menu(self):
        
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)

        
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(self.action['load'])
        filemenu.addAction(self.action['saveJSON'])
        filemenu.addAction(self.action['saveAs'])
        
        
        filemenu.addAction(self.action['import'])
        # filemenu.addAction(self.action['cancel'])
        filemenu.addAction(self.action['exit'])

        
        editmenu = menubar.addMenu('&Edit')
        editmenu.addAction(self.action['mode0'])
        editmenu.addAction(self.action['mode1'])
        editmenu.addAction(self.action['mode2'])       
        
        editmenu.addAction(self.action['prev'])
        editmenu.addAction(self.action['next'])
        

        
        
        
        

    def _create_toolbar(self):
        
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(self.action['saveJSON'])
        self.toolbar.addAction(self.action['saveAs'])
        self.toolbar.addAction(self.action['prev'])
        self.toolbar.addAction(self.action['next'])
        self.toolbar.addAction(self.action['exit'])
        self.toolbar.addAction(self.action['mode0'])
        self.toolbar.addAction(self.action['mode1'])
        self.toolbar.addAction(self.action['mode2'])
        
        

    def _connect(self):
        
        
        R, G, B = 'RED', 'GREEN', 'BLUE'
        self.leftside_widget.pushButton.clicked.connect(self.leftside_widget.color_select)
        self.leftside_widget.pushButton_2.clicked.connect(lambda: self.leftside_widget.fast_color(R))
        self.leftside_widget.pushButton_3.clicked.connect(lambda: self.leftside_widget.fast_color(G))
        self.leftside_widget.pushButton_4.clicked.connect(lambda: self.leftside_widget.fast_color(B))
        self.leftside_widget.pushButton_5.clicked.connect(self.leftside_widget.add_attr_list)
        self.leftside_widget.pushButton_6.clicked.connect(self.leftside_widget.del_attr_list)
        self.leftside_widget.listWidget_2.clicked.connect(self.leftside_widget.select_attr_list)
        self.leftside_widget.listWidget.itemDoubleClicked.connect(lambda: self.leftside_widget.select_image(self.image_widget))

        
        
        

        
        
        

    def _center(self):
        
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _action_load_image(self):
        load_win = qt_load.LoadDialog()

        
        r = load_win.showModal()

        if r:
            text = load_win.image_files
            LD_image = text

            image_data = dataset.DirectDataset(LD_image)
            self.load_data(image_data)
        else:
            
            return super()

    
    
    