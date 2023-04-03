from PyQt5.QtWidgets import QGraphicsEllipseItem


class EllipseItem(QGraphicsEllipseItem):
    def __init__(self, parent, ellipse, attribute, id = -1):
        super().__init__(ellipse)
        self.parent = parent
        self.point = ellipse
        self.attribute = attribute
        self.id = id
        self.name= 'Elli'
        print('ellipse:',self.point)
        print('ellipse id:',self.id)
        print('x:',self.point.x())

        self.text_item = None

        self.setAcceptHoverEvents(True)

    def mouseDoubleClickEvent(self, e):
        self.parent.callback_polygon_double_click(self)

    def hoverEnterEvent(self, e):
        self.parent.callback_polygon_hover_enter(self)

    def hoverMoveEvent(self, e):
        self.parent.callback_polygon_hover_move(self)

    def hoverLeaveEvent(self, e):
        self.parent.callback_polygon_hover_leave(self)