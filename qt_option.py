import PyQt5
from PyQt5.QtWidgets import QGraphicsView 
from PyQt5.QtGui import QColor,QCursor,QPixmap,QImage
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt

class EditMode:
    _MODE_COUNT = 6
    
    def __init__(self):
        # self.scene = QGraphicsScene()  #1103
        
        # super().__init__()
        # self.setScene(self.scene) #1103
        self.set_default()

    def set_default(self):
        
        self.set_mode(0)

        
        self.DRAW_PEN_COLOR = QColor(0, 0, 0)
        self.DRAW_PEN_COLOR_WARNNING = QColor(255, 0, 0)
        self.DRAW_PEN_COLOR_SELECT = QColor(0, 255, 255)
        self.DRAW_PEN_WIDTH = 3
        self.DRAW_PEN_WIDTH_SELECT = 6
        self.DRAW_BRUSH_COLOR = QColor(0, 0, 255, 80)

        self.DRAW_MASK_COLOR = QColor(255, 255, 0, 100)
        self.DRAW_MASK_TOLERANCE = 10
        self.DRAW_MASK_TOLERANCE_MIN = 1
        self.DRAW_MASK_TOLERANCE_MAX = 100

        self.DRAW_PAINT_WIDTH = 30
        self.DRAW_PAINT_WIDTH_MIN = 1
        self.DRAW_PAINT_WIDTH_MAX = 100
        self.DRAW_PAINT_MODE = True

        self.POLYGON_CURRENT_ATTRIBUTE = {"name" : "none"}
        self.POLYGON_BRUSH_COLOR = {}

        self.IMAGE_ADJUST_MODE = 0
        self.IMAGE_ADJUST_OPENING_SIZE = 3
        self.IMAGE_ADJUST_CLOSING_SIZE = 7
        self.IMAGE_ADJUST_CANNY_MIN = 50
        self.IMAGE_ADJUST_CANNY_MAX = 100

        
        self.POLYGON_END_THRESHOLD = 2000

        
        self.SCROLLBAR_VIEW = True

    def set_mode(self, mode):
        assert mode < self._MODE_COUNT, "Invalid edit mode"
        self.CURRENT = mode
        self.VIEW_DRAG_MODE = QGraphicsView.NoDrag 

        if mode == 0:
            
            self.VIEW_DRAG_MODE = QGraphicsView.ScrollHandDrag
            pass

        elif mode == 1:
            # aa=cv.imread('./icon/polygon.png')
            # x,y,z=cv.imread('./icon/polygon.png').shape[:3]
            # poly_cursor=QCursor(QPixmap(QImage(aa,x,y,x*z,QImage.Format_RGB888)),0,0)
            # poly_cursor1=QCursor(QPixmap('./icon/polygon.png'),0,0)
            # print(QPixmap('./icon/polygon.png'))
            # print(QPixmap(QImage(aa,x,y,x*z,QImage.Format_RGB888)))
            # print(poly_cursor)
            # print(poly_cursor1)
            # self.setCursor(self,QCursor(PyQt5.QtCore.Qt.CrossCursor))
            # bb=QWidget.setCursor(self,poly_cursor1)
            # print(aa)
            # print(bb)
            # image_item = QGraphicsPixmapItem(QPixmap('./icon/polygon.png'))
            # self.scene.addItem(image_item)

            
            pass
        elif mode == 5: # 221024_jh 
            # 5. Draw Mode : draw point

            pass