global_current=[0]

from statistics import mode
from qt_polygon import PolygonItem
from qt_ellipse import EllipseItem
from qt_opencv import OpenCVImage

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView, QGraphicsEllipseItem
from PyQt5.QtGui import QPixmap, QBrush, QPen, QPolygonF, QColor, QFont
from PyQt5.QtCore import Qt, QLineF, QPointF, QRectF, QSizeF

import os
from PyQt5.QtWidgets import QListWidgetItem
from widget.qt_leftside import global_item
from widget import qt_leftside
from widget import qt_form



class ImageWidget(QWidget):
    def __init__(self, mode, parent):
        super().__init__()
        self.mode = mode
        self.parent = parent
        self.dataset = None
        self.image = None
        self.view = None
        self.pixmap = None
        self.image_count = 0
        self.current = 0 

        
        self.view = ImageView(mode)

        
        vbox = QVBoxLayout()
        vbox.addWidget(self.view)
        self.setLayout(vbox)

        
        self._update()

    def load_data(self, dataset):
        self.image_count = dataset.image_count

        if self.image_count > 0:
            self.dataset = dataset
            self.current = 0
            self._image_select(self.current)
        else:
            self.dataset = None
            print("No image to import")

    def select_image(self, index):
        self.current = index if index < self.image_count else 0
        global_current.append(self.current)
        if self.dataset is not None:
            self._image_select(self.current)

    def next_image(self):
        self.current = self.current + 1 if self.current < self.image_count - 1 else 0
        global_current.append(self.current)
        if self.dataset is not None:
            self._image_select(self.current)

    def prev_image(self):
        self.current = self.current - 1 if self.current > 0 else self.image_count - 1
        global_current.append(self.current)
        if self.dataset is not None:
            self._image_select(self.current)

    def redraw(self, backup_mask=False):
        print(backup_mask)
        if self.view.image is None:
            return

        
        if backup_mask:
            mask = self.view.image.backup_mask()

        
        self.view.reset()

        
        self._image_select(self.current)

        
        if backup_mask:
            self.view.image.restore_mask(mask)

        
        self.view.refresh()

    def _update(self):
        if self.dataset is None:
            return

        
        self._image_adjust(self.image)
        print('updated_metadata:',self.metadata)
        
        self.view.load_image(self.image, self.metadata)

    def _image_select(self, image_id):
        image, self.metadata = self.dataset.load_image(image_id)
        self.parent.leftside_widget.select_image_list(image_id)
        self.image = OpenCVImage(image)
        self._update()

    def _image_adjust(self, image):
        assert image is not None, "Image is None"
        image.reset_image()
        if self.mode.IMAGE_ADJUST_MODE == 0:
            
            pass

        elif self.mode.IMAGE_ADJUST_MODE == 1:
            
            image.grayscale()

        elif self.mode.IMAGE_ADJUST_MODE == 2:
            
            image.crack_detector_opening(self.mode.IMAGE_ADJUST_OPENING_SIZE)

        elif self.mode.IMAGE_ADJUST_MODE == 3:
            
            image.crack_detector(self.mode.IMAGE_ADJUST_OPENING_SIZE,
                                         self.mode.IMAGE_ADJUST_CLOSING_SIZE)

        elif self.mode.IMAGE_ADJUST_MODE == 4:
            
            image.edge_detector(self.mode.IMAGE_ADJUST_CANNY_MIN,
                                        self.mode.IMAGE_ADJUST_CANNY_MAX)

class ImageView(QGraphicsView,qt_form.Ui_LeftForm):
    def __init__(self, mode):     
        self.mode = mode

        self.leftside_widget = qt_leftside.LeftSideWidget(self.mode, self)   
              
        self.scene = QGraphicsScene()
        super().__init__(self.scene)
        self.setScene(self.scene)

        
        
        
        self.items = []
        self.obj = {} 
        self._object_reset()

        self.rect_p0 = None
        self.rect_p1 = None
        self.select = []

        
        self.image = None
        self.pixmap = None
        self.image_item = None
        self.metadata = None

        
        self._zoom = 0
        self.KEY_SHIFT = False
        self.KEY_ALT = False
        self.KEY_CTRL = False
        self.KEY_MOUSE_LEFT = False

        
        self.last_mask = None
        self.last_polygon = None

        
        self.setDragMode(self.mode.VIEW_DRAG_MODE)
        self.setMouseTracking(True)

        
        if not self.mode.SCROLLBAR_VIEW:
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def load_image(self, image, metadata):
        self.reset()
        self.image = image
         # Qimage 를 가져온다.
        image = self.image.get_image()
         # pixmap data 생성
        pixmap = QPixmap(image)

        self.pixmap = pixmap
        self.image_item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(self.image_item)

        self._load_metadata(metadata)

    def refresh(self):
        """ 현재 작업중인 임시 정보를 모두 삭제하고, 현재 설정값을 재설정한다.

        """
        # Object 초기화
        self._object_reset()

        # Mode 설정
        self.setDragMode(self.mode.VIEW_DRAG_MODE)

        # Data Reset
        self.rect_p0 = None
        self.rect_p1 = None
        self.select.clear()

        # Key 초기화
        self.KEY_SHIFT = False
        self.KEY_ALT = False
        self.KEY_MOUSE_LEFT = False

        
        self._mask_draw()

        # update
        self._update()

    def reset(self):
        """ 이미지 정보를 포함하여 모든 정보를 삭제한다.

        """
        # Scene 에 표시되는 물체들을 제거한다.
        self._delete_items(self.items)
        self.scene.removeItem(self.image_item)

        # backup 초기화
        self.last_mask = None
        self.last_polygon = None

        # image 정보 초기화
        self.image = None
        self.pixmap = None
        self.image_item = None
        self.metadata = None

        # refresh
        self.refresh()

    def restore(self):
        print('restore')
        if self.last_mask is not None and self.image is not None:
            self.image.restore_mask(self.last_mask)
            if self.last_polygon is not None:
                self._polygon_delete(self.last_polygon)
            print('1')

            self.last_mask = None
            self.last_polygon = None
            self._mask_draw()

    def callback_selected(self, e, item):
        """ Image Item 객체가 선택되었을 때, View 에 직접 호출 할 수 있는 함수

            Image Item 객체의 event 함수에서 호출된다.
        """
        pass

    def callback_polygon_double_click(self, polygon_item):
        if self.KEY_CTRL and self.mode.CURRENT == 0:
            
            
            if polygon_item.text_item is not None:
                self.items.remove(polygon_item.text_item)
                self.scene.removeItem(polygon_item.text_item)

            
            self.items.remove(polygon_item)
            self.scene.removeItem(polygon_item)
        elif self.KEY_CTRL:
            self._polygon_delete(polygon_item)
            print('pdel_activated')

    def callback_polygon_hover_enter(self, polygon_item):
        if self.mode.CURRENT == 0:
            self.setDragMode(QGraphicsView.NoDrag)

    def callback_polygon_hover_move(self, polygon_item):
        if self.mode.CURRENT == 0:
            self.setDragMode(QGraphicsView.NoDrag)

    def callback_polygon_hover_leave(self, polygon_item):
        if self.mode.CURRENT == 0:
            self.setDragMode(self.mode.VIEW_DRAG_MODE)

    def _load_metadata(self, metadata):
        """ Image Annotation 을 읽어와 View 에 출력한다.
        """
        self.metadata = metadata
        polygons = metadata.out_polygons_to_list()
        points = metadata.out_point_to_list()
        if metadata.polygon_count >0:
            for polygon in polygons:
                # attribute 참조
                # region = reg["region"]
                # polygon = [region, all_points_x, all_points_y, id]
                [attribute, x, y, id] = polygon
                assert len(x) == len(y), "Invalid polygon information in metadata"
                qpol = QPolygonF()
                for idx in range(len(x)):
                    # qpoint=QPointF(x[idx], y[idx])
                    qpol.append(QPointF(x[idx], y[idx]))
                # if len(x) <2 : 
                #     for point in points:
                #         [attribute, x, y, id] =points
                #         self._point_draw((x,y), attribute, id)
                #     # self._point_draw(points, attribute, id)
                    
                # else :
                self._polygon_draw(qpol, attribute, id)
            if metadata.point_count >0:
                print('load_metadata_check:',metadata.point_count)
                qpoints=[]
                for point in points:
                    [attribute, x, y, id] =point
                    qpoint=QPointF(x[0],y[0])
                    self._point_draw(qpoint, attribute, id)
                        # self._point_draw(points, attribute, id) 
        elif metadata.point_count >0:
            print('load_metadata_check:',metadata.point_count)
            qpoints=[]
            for point in points:
                [attribute, x, y, id] =point
                qpoint=QPointF(x[0],y[0])
                self._point_draw(qpoint, attribute, id)
                    # self._point_draw(points, attribute, id)               
            



    def _update(self):
        pass

    def _delete_items(self, items):
        for item in items:
            self.scene.removeItem(item)
        items.clear()

    def _object_reset(self):
        """ Object 를 초기화한다.

            obj Dictionary 에는 view 그리기에 필요한 임시값들이 저장되어있다.
        """
        
        if 'polygon' not in self.obj:
            self.obj['polygon'] = []
        else:
            self.obj['polygon'].clear()

        
        if 'lines' not in self.obj:
            self.obj['lines'] = []
        else:
            self._delete_items(self.obj['lines'])
            self.obj['lines'].clear()

        
        if 'mask' in self.obj and self.obj['mask'] is not None:
            self.scene.removeItem(self.obj['mask'])
        self.obj['mask'] = None

        
        if 'paint' in self.obj and self.obj['paint'] is not None:
            self.scene.removeItem(self.obj['paint'])
        self.obj['paint'] = None
        
        if 'point' not in self.obj:
            self.obj['point'] = []
        else:
            self.obj['point'].clear()


    # def _point_check(self, polygon_list):
    #     """ polygon 의 시작 위치와 종료 위치를 이용하여 생성 조건을 반환한다.

    #     """
    #     if polygon_list is None or len(polygon_list) < 3:
    #         return False

        
    #     dx = polygon_list[-1].x() - polygon_list[0].x()
    #     dy = polygon_list[-1].y() - polygon_list[0].y()
    #     d = dx * dx + dy * dy

    #     if d < self.mode.POLYGON_END_THRESHOLD:
            
    #         del (polygon_list[-1])
    #         polygon_list.append(polygon_list[0])
    #         return True
    #     else:
    #         return False

    def _polygon_check(self, polygon_list):
        """ polygon 의 시작 위치와 종료 위치를 이용하여 생성 조건을 반환한다.

        """
        if polygon_list is None or len(polygon_list) < 3:
            return False

        
        dx = polygon_list[-1].x() - polygon_list[0].x()
        dy = polygon_list[-1].y() - polygon_list[0].y()
        d = dx * dx + dy * dy

        if d < self.mode.POLYGON_END_THRESHOLD:
            
            del (polygon_list[-1])
            polygon_list.append(polygon_list[0])
            return True
        else:
            return False



    def _polygon_draw(self, polygon, attribute, id=-1):
        """ polygon 을 그린다.
        setPen(QPen(self.brush_color, self.brush_size, Qt.SolidLine, Qt.RoundCap))
            polygon 객체를 인수로 받아서 scene 에 추가한다.
        """
        
        attribute = attribute.copy()

        pen = QPen(self.mode.DRAW_PEN_COLOR, 3)
        if attribute['name'] in self.mode.POLYGON_BRUSH_COLOR:
            # if self.mode.CURRENT == 5: ## point 일때 pen 변경 221101 aehyj92
                # pen= QPen(self.mode.POLYGON_BRUSH_COLOR[attribute['name']],20)
            brush = QBrush(self.mode.POLYGON_BRUSH_COLOR[attribute['name']])
        #     else :   
        #         brush = QBrush(self.mode.POLYGON_BRUSH_COLOR[attribute['name']])
        # elif self.mode.CURRENT == 5:  ## point 일때 pen 변경
        #     pen = QPen(QColor(230, 0, 0),20)
        #     brush = QBrush(self.mode.DRAW_BRUSH_COLOR)
            
        else:
            brush = QBrush(self.mode.DRAW_BRUSH_COLOR)

        
        polygon_item = PolygonItem(self, polygon, attribute, id)
        polygon_item.setPen(pen)
        polygon_item.setBrush(brush)

        
        self.items.append(polygon_item)
        self.scene.addItem(polygon_item)

        
        self._polygon_location(polygon_item)

        return polygon_item

##point draw 221026jh
    def _point_draw(self,point,attribute, id=-1):
        """ point 를 찍는다. 
            point 객체를 인수로 받아서 scene 에 추가한다.
        """
       
        attribute = attribute.copy() #221024 aehyj92
        pen = QPen(QColor(230, 0, 0,200),20)
        if attribute['name'] in self.mode.POLYGON_BRUSH_COLOR:
            brush = QBrush(self.mode.POLYGON_BRUSH_COLOR[attribute['name']])
            pen= QPen(self.mode.POLYGON_BRUSH_COLOR[attribute['name']],20)
        else:
            brush = QBrush(self.mode.DRAW_BRUSH_COLOR)
            pen = QPen(QColor(230, 0, 0,200),20)
        #221101 aehyj92
        print('point_draw,point',point)
        point_item =  QRectF(point,QSizeF(3,3))
        point=QPolygonF([QPointF(point)])  
        point_item_elli = EllipseItem(self,point_item,attribute,id)
        # point_item_info = PolygonItem(self, point, attribute, id)
        
        point_item_elli.setPen(pen)
        point_item_elli.setBrush(brush)       
        
        # point_item_info.setPen(pen)
        # point_item_info.setBrush(brush)
      
        self.items.append(point_item_elli)
        self.scene.addItem(point_item_elli)
        # self.scene.addEllipse(point_item,pen,brush)
        self._polygon_location(point_item_elli)
        
        return point_item_elli       
 
 
        # attribute = attribute.copy()
        # print('hi')
        # pen = QPen(self.mode.DRAW_PEN_COLOR,10)
        # print('hi2')
        # if attribute['name'] in self.mode.POLYGON_BRUSH_COLOR:
        #     brush = QBrush(self.mode.POLYGON_BRUSH_COLOR[attribute['name']])
        # else:
        #     print('hi3')
        #     brush = QBrush(self.mode.DRAW_BRUSH_COLOR)
        # #221101 aehyj92
        # point_item =  PolygonItem(self, point, attribute, id)
        # print('hi4')
        # point_item.setPen(pen)
        # point_item.setBrush(brush)

        
        # self.items.append(point_item)
        # self.scene.addItem(point_item)
        # # self._polygon_location(point_item)
        
    def _polygon_location(self, polygon_item):
        ## Elli 일때 좌표반환 추가
        
        name = polygon_item.name
        attribute = polygon_item.attribute
        if name =='Poly':
            polygon = polygon_item.polygon
        elif name =='Elli' :
            point = polygon_item.point
                   
        text_locate, compare_list_y = [], []
        if name =='Poly':
            for i in range(len(polygon) - 1):
                compare_list_y.append(polygon[i].toPoint().y())
            print(compare_list_y)
            if compare_list_y :
                top_of_polygon_y = min(compare_list_y)
                index = compare_list_y.index(top_of_polygon_y)  
                text_locate.append(polygon[index].toPoint().x())
                text_locate.append(polygon[index].toPoint().y())
                text_locate[0] = text_locate[0] - 5
                text_locate[1] = text_locate[1] - 5
            else :
                pass
                
        elif name =='Elli' :
            text_locate.append(point.x())
            text_locate.append(point.y())
            print(text_locate)
            text_locate[0] = text_locate[0] - 5
            text_locate[1] = text_locate[1] - 5


        
        if 'name' not in attribute:
            attribute['name'] = 'none'
        item = self.scene.addText(attribute['name'], QFont('Arial', 10))
        self.items.append(item)
        polygon_item.text_item = item
        # if compare_list_y :
        item.setPos(text_locate[0], text_locate[1])
        

    def _polygon_add_info(self, polygon_item):
        """ polygon 을 metadata 에 추가한다.
            polygon이 그려진 file을 check 한다.

        """
        ## Elli 일때 좌표반환 추가
        region_attribute = polygon_item.attribute
    
        name = polygon_item.name
        if name =='Poly':
            polygon = polygon_item.polygon
        elif name =='Elli' :
            point = polygon_item.point 
 
       
        name = polygon_item.name
        xs = []
        ys = []
        if name =='Poly':
            for point in polygon:
                xs.append(int(point.x()))
                ys.append(int(point.y()))
            polygon_item.id = self.metadata.add_polygon(region_attribute, xs, ys)
        elif name =='Elli':
                xs.append(int(point.x()))
                ys.append(int(point.y()))   
                polygon_item.id = self.metadata.add_point(region_attribute, xs, ys) 
       
        print('add_info:',xs,ys)
        # polygon_item.id = self.metadata.add_polygon(region_attribute, xs, ys)
        ## 0823 file check
        # self.leftside_widget.check_filelist()
        self.leftside_widget.check_filelist_1()
 

    def _polygon_delete(self, polygon_item):
        
        print('polygon_delete/','item_id:',polygon_item.id)
        self.metadata.delete_polygon(polygon_item.id)
        self.metadata.delete_point(polygon_item.id)    

        if polygon_item.text_item is not None:
            print('itemis')
            self.items.remove(polygon_item.text_item)
            self.scene.removeItem(polygon_item.text_item)

        self.items.remove(polygon_item)
        self.scene.removeItem(polygon_item)
        
        
    def _point_delete(self, polygon_item):
        
        print('point_delete/','item_id:',polygon_item.id)
        self.metadata.delete_point(polygon_item.id)

        if polygon_item.text_item is not None:
            print('itemis')
            self.items.remove(polygon_item.text_item)
            self.scene.removeItem(polygon_item.text_item)

        self.items.remove(polygon_item)
        self.scene.removeItem(polygon_item)

    def _mask_draw(self):
        if self.image is None:
            return

        
        bitmap = self.image.get_mask()

        
        pixmap = QPixmap(self.pixmap)
        pixmap.fill(self.mode.DRAW_MASK_COLOR)

        
        pixmap.setMask(bitmap)

        
        if self.obj['mask'] is not None:
            self.scene.removeItem(self.obj['mask'])
        self.obj['mask'] = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(self.obj['mask'])

    def _mask_reset(self):
        
        if self.image is not None:
            self.image.reset_mask()

    def _paint_draw_sign(self, x, y):
        
        brush = QBrush(self.mode.DRAW_MASK_COLOR) if self.mode.DRAW_PAINT_MODE else QBrush(QColor(255, 255, 255, 50))
        pen = QPen(QColor(0, 0, 0), 3)

        
        width = self.mode.DRAW_PAINT_WIDTH
        if self.obj['paint'] is not None:
            self.scene.removeItem(self.obj['paint'])
        self.obj['paint'] = QGraphicsEllipseItem(int(x - width / 2), int(y - width / 2),
                                                 width, width)
        self.obj['paint'].setBrush(brush)
        self.obj['paint'].setPen(pen)
        self.scene.addItem(self.obj['paint'])

    def _draw_sequence_press(self, pos, out_of_range):
        """ view 에 item 들을 그린다.

            mode 로 view 에 그리는 방법을 다르게 설정 할 수 있다.
            press, move, release sequence 함수들은 서로 의존적이다.
            mousePressEvent 에서 호출된다.
        """
        if out_of_range:
            return

        last_pos = self.rect_p0
        self.rect_p0 = pos

        
        if self.mode.CURRENT == 1:
            
            polygon_list = self.obj['polygon']
            polygon_list.append(pos)

            
            if self._polygon_check(polygon_list):
                
                polygon = QPolygonF([QPointF(point) for point in polygon_list])

                
                polygon_item = self._polygon_draw(polygon, self.mode.POLYGON_CURRENT_ATTRIBUTE)

                
                self._polygon_add_info(polygon_item)

                
                polygon_list.clear()

                
                self._delete_items(self.obj['lines'])

                
                self.rect_p0 = None
                self.rect_p1 = None

            elif self.rect_p1 != None:
                
                pen = QPen(self.mode.DRAW_PEN_COLOR, self.mode.DRAW_PEN_WIDTH) if not out_of_range \
                    else QPen(self.mode.DRAW_PEN_COLOR_WARNNING, self.mode.DRAW_PEN_WIDTH)

                line = QLineF(self.rect_p0.x(), self.rect_p0.y(),
                              last_pos.x(), last_pos.y())
                self.obj['lines'].insert(0, self.scene.addLine(line, pen))

        
        elif self.mode.CURRENT == 2:
            
            if self.KEY_SHIFT and self.KEY_ALT:
                option = 'and'
            elif self.KEY_SHIFT:
                option = 'or'
            elif self.KEY_SHIFT:
                option = 'sub'
            else:
                option = 'select'

            
            self.image.set_tolerance(self.mode.DRAW_MASK_TOLERANCE)
            self.image.set_mask(int(pos.x()), int(pos.y()), option=option)

            
            self._mask_draw()

        
        elif self.mode.CURRENT == 3:
            
            if self.mode.DRAW_PAINT_MODE:
                self.image.paint_mask(int(pos.x()), int(pos.y()), self.mode.DRAW_PAINT_WIDTH)
            else:
                self.image.erase_mask(int(pos.x()), int(pos.y()), self.mode.DRAW_PAINT_WIDTH)
            self._mask_draw()
            self._paint_draw_sign(int(pos.x()), int(pos.y()))
            
        elif self.mode.CURRENT == 5 :  # 221024 aehyj92
            # point_list = self.obj['point']  # 221101 aehyj92  
            # point = QPolygonF([QPointF(pos)])        
            # point_item = self._point_draw(point, self.mode.POLYGON_CURRENT_ATTRIBUTE)

            point_list = self.obj['point']  # 221101 aehyj92 
            point_list.append(pos) 
            print('ellip_pos:',pos)
            # point = pos  
            # point_info =  QPolygonF([QPointF(pos)])  
            point_item = self._point_draw(pos, self.mode.POLYGON_CURRENT_ATTRIBUTE)     
            # point_item_info = self._polygon_draw(point_info, self.mode.POLYGON_CURRENT_ATTRIBUTE)
            self._polygon_add_info(point_item)
            
            # list clear & scene의 anno 삭제 221102 aehyj92  
            point_list.clear()
            self._delete_items(self.obj['point'])
            self.rect_p0 = None
            self.rect_p1 = None
            self._paint_draw_sign(int(pos.x()+5), int(pos.y()+5))

    def _draw_sequence_move(self, pos, out_of_range):
        """ view 에 item 들을 그린다.

            mouseMoveEvent 에서 호출된다.
        """

        
        if self.mode.CURRENT == 1:
            if self.rect_p0 is None:
                return
            else:
                self.rect_p1 = pos

            
            pen = QPen(self.mode.DRAW_PEN_COLOR, self.mode.DRAW_PEN_WIDTH) if not out_of_range \
                else QPen(self.mode.DRAW_PEN_COLOR_WARNNING, self.mode.DRAW_PEN_WIDTH)

            
            if len(self.obj['lines']) > 0:
                self.scene.removeItem(self.obj['lines'][-1])
                del (self.obj['lines'][-1])

            
            line = QLineF(self.rect_p0.x(), self.rect_p0.y(),
                          self.rect_p1.x(), self.rect_p1.y())
            self.obj['lines'].append(self.scene.addLine(line, pen))

        elif self.mode.CURRENT == 3 and not out_of_range:
            
            if self.KEY_MOUSE_LEFT:
                if self.mode.DRAW_PAINT_MODE:
                    self.image.paint_mask(int(pos.x()), int(pos.y()), self.mode.DRAW_PAINT_WIDTH)
                else:
                    self.image.erase_mask(int(pos.x()), int(pos.y()), self.mode.DRAW_PAINT_WIDTH)

                self._mask_draw()
            self._paint_draw_sign(int(pos.x()), int(pos.y()))
            
        elif self.mode.CURRENT == 5 : 
            self._paint_draw_sign(int(pos.x()+5), int(pos.y()+5))

    def _mouse_check(self, e):
        """ 현재 좌표와 좌표가 이미지 위에 위치하는지 여부를 반환한다.

            Image 가 할당된 이후에 호출될 수 있어야 한다.
            QMouseEvent 가 주어져야한다.
        """
        assert self.image_item is not None, "No image to check"

        
        pos = self.mapToScene(e.pos())

        
        pos = self.image_item.mapFromScene(pos)

        
        rect = self.image_item.boundingRect()

        
        return pos, not rect.contains(pos)

    def keyPressEvent(self, e):
        super().keyPressEvent(e)
        if self.image is None:
            return

        if e.key() == Qt.Key_Escape:
            self.last_mask = self.image.backup_mask()
            self._mask_reset()
            self.refresh()
        if e.key() == Qt.Key_Shift:
            self.KEY_SHIFT = True
            self.mode.DRAW_PAINT_MODE = not self.mode.DRAW_PAINT_MODE
        if e.key() == Qt.Key_Alt:
            self.KEY_ALT = True
        if e.key() == Qt.Key_Control:
            self.KEY_CTRL = True
        if e.key() == Qt.Key_Space and self.image is not None:
            
            self.last_mask = self.image.backup_mask()
            polygon = self.image.get_polygon()
            if polygon is not None:
                polygon_item = self._polygon_draw(polygon, self.mode.POLYGON_CURRENT_ATTRIBUTE)
                self._polygon_add_info(polygon_item)
                self.last_polygon = polygon_item

                self._mask_reset()
                self.refresh()

    def keyReleaseEvent(self, e):
        if e.key() == Qt.Key_Shift:
            self.KEY_SHIFT = False
        if e.key() == Qt.Key_Alt:
            self.KEY_ALT = False
        if e.key() == Qt.Key_Control:
            self.KEY_CTRL = False

    def showEvent(self, e):
        
        self._update()
        super().showEvent(e)

    def wheelEvent(self, e):
        if self.KEY_CTRL:
            if self.mode.CURRENT == 3:
                pos, out_of_range = self._mouse_check(e)
                if not out_of_range:
                    
                    self._paint_draw_sign(int(pos.x()), int(pos.y()))
            return

        
        if e.angleDelta().y() > 0 and self._zoom < 10:
            self.scale(1.25, 1.25)
            self._zoom += 1
        elif e.angleDelta().y() < 0 and self._zoom > -10:
            self.scale(0.8, 0.8)
            self._zoom -= 1

    def mousePressEvent(self, e):
        
        super().mousePressEvent(e)

        if self.KEY_CTRL:
            return

        
        if self.image_item is not None:
            pos, out_of_range = self._mouse_check(e)
        else:
            return

        
        if self.mode.CURRENT not in [0, 2, 3]:
            self._mask_reset()
            self._mask_draw()

        
        if e.button() == Qt.LeftButton:
            self.KEY_MOUSE_LEFT = True

            
            self._draw_sequence_press(pos, out_of_range)

    def mouseMoveEvent(self, e):
        super().mouseMoveEvent(e)

        
        if self.image_item is not None:
            
            pos, out_of_range = self._mouse_check(e)

            
            self._draw_sequence_move(pos, out_of_range)

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)

        
        if self.image_item is not None:
            pos, out_of_range = self._mouse_check(e)
        else:
            return

        
        if e.button() == Qt.LeftButton:
            self.KEY_MOUSE_LEFT = False