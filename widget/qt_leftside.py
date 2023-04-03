global_item=[]
global_base_name=[]
global_file_name=[]
from widget.qt_image import global_current

import os
import numpy as np 

from PyQt5.QtWidgets import QWidget, QColorDialog
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtCore import Qt
from numpy import arange
from widget import qt_form

from PyQt5 import QtWidgets

class LeftSideWidget(QWidget, qt_form.Ui_LeftForm):
    def __init__(self, mode, parent):
        super().__init__()
        self.mode = mode
        self.parent = parent
        self.item_ =[]
        self.base_name=[]
        self.top = 0
        self.attr_dict = dict()

        self.add_color = ""
        ##
        self.listWidget = QtWidgets.QListWidget()
        ##
        
    # def check_filelist(self): 
    #         for i,j in zip(global_base_name,arange(len(global_base_name))):
    #             # print(global_base_name)
    #             # print(i)
    #             # print(j)
    #             # print(global_file_name)
    #             # print(i)
    #             if i == global_file_name[0]:                    
    #                 global_item[-1][j].setCheckState(Qt.Checked)  
    #                 self.listWidget.addItem(global_item[-1][j])  
                    
    def check_filelist_1(self):
            # print(global_current)
            global_item[-1][global_current[-1]].setCheckState(Qt.Checked)  
            self.listWidget.addItem(global_item[-1][global_current[-1]])



    def load_filelist(self, dataset):
        for i,j in zip(dataset.image_dirs,arange(len(dataset.image_dirs))):
            
            self.item_.append(QListWidgetItem(str(os.path.basename(i))))
            global_item.append(self.item_)
            global_base_name.append(str(os.path.basename(i)))
            self.item_[j].setCheckState(Qt.Unchecked)   
            self.listWidget.addItem(self.item_[j]) 
        
    # def load_filelist(self, dataset):
    #     for i,j in zip(dataset.image_dirs,arange(len(dataset.image_dirs))):
            
    #         self.item_.append(QListWidgetItem(str(os.path.basename(i))))
    #         global_item.append(self.item_)
    #         # self.base_name.append(str(os.path.basename(i)))
    #         self.item_[j].setCheckState(Qt.Unchecked)   
    #         print(self.item_[j]) 
    #         print(global_item[j]) 
    #         # global_item.append(QListWidgetItem(str(os.path.basename(i))))
    #         # global_item.append(str(os.path.basename(i)))
    #         # global_item.append(self.item_)
    #         # global_item.append(str(os.path.basename(i)))
    #         # global_item.setCheckState(Qt.Unchecked)
    #         self.listWidget.addItem(self.item_[j]) 
            # print(type(global_item[1]),global_item[1]) 
        #     print(self.item_[j])
        # print(self.item_)
        # for i,j in zip(dataset.image_dirs,arange(len(dataset.image_dirs))):
        #     self.item.append(QListWidgetItem(str(os.path.basename(i))))
        #     self.base_name.append(str(os.path.basename(i)))
        #     self.item[j].setCheckState(Qt.Unchecked)    
        #     self.listWidget.addItem(self.item[j])  
        # print(self.item,i,j)

            # self.listWidget.addItem(str(os.path.basename(i)))

    def select_image(self, image_widget):
        image_file = self.listWidget.currentItem().text()
        global_file_name.append(image_file)####################
        image_count = self.listWidget.count()
        # print(image_count)
        for i in range(image_count):
            if image_file == self.listWidget.item(i).text():
                image_widget.select_image(i)
                break

    def select_image_list(self, image_id):
        if not image_id < self.listWidget.count():
            return
        self.listWidget.setCurrentRow(image_id)

    def color_select(self):
        
        color = QColorDialog.getColor()

        if color.isValid():
            self.listWidget_3.clear()
            self.listWidget_3.addItem(color.name())
            self.add_color = str(color.name())
   

    def select_attr_list(self):
        
        attr = self.listWidget_2.currentItem().text()
        attr_index = self.listWidget_2.count()
        for i in range(attr_index):
            if str(self.attr_dict[i]) == attr:
                self.mode.POLYGON_CURRENT_ATTRIBUTE['name'] = str(self.attr_dict[i]['name'])

    def del_attr_list(self):
        
        attr = self.listWidget_2.currentItem()
        flag = 0

        for index in range(self.listWidget_2.count()):  
            if attr == self.listWidget_2.item(index):
                self.listWidget_2.takeItem(flag).text()
                del self.mode.POLYGON_BRUSH_COLOR[str(self.attr_dict[flag]['name'])]
                del self.attr_dict[flag]
                if flag != len(self.attr_dict):
                    for i in range(len(self.attr_dict) - flag):
                        self.attr_dict[flag + i] = self.attr_dict[flag + i + 1]
                    del self.attr_dict[len(self.attr_dict) - 1]
                self.top -= 1
                break
            flag += 1
        self.parent.image_widget.redraw()

    def add_attr_list(self):
        
        
        name_dupl = []
        name = self.lineEdit.text()

        for i in range(self.listWidget_2.count()):
            name_dupl.append(self.listWidget_2.item(i).text())
            if name in name_dupl[i]:
                return super()

        if self.add_color is not "":
            self.attr_dict[self.top] = {'name': name, 'color': self.add_color}
            self.listWidget_2.addItem(str(self.attr_dict[self.top]))

            
            self.listWidget_2.setCurrentRow(self.top)
            self.select_attr_list()

            
            color = QColor(self.attr_dict[self.top]['color'])
            color.setAlpha(200)
            self.mode.POLYGON_BRUSH_COLOR[str(self.attr_dict[self.top]['name'])] = color
            self.parent.image_widget.redraw()

            self.top += 1

    def fast_color(self, color):
        
        self.listWidget_3.clear()
        self.listWidget_3.addItem(str(color))
        self.add_color = color

    
    
    
    

    
    
    
    

    
    
    
    

    
    
    
    

    
    
    
    

    
    
    