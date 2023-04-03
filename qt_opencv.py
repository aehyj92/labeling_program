import cv2 as cv
import numpy as np
from PyQt5.QtGui import QImage, QBitmap, QPolygonF
from PyQt5.QtCore import QPointF


class OpenCVImage():
    def __init__(self, image, connectivity=4, tolerance=35):

        self._image = image
        self._origin = image
     
        height, width ,channel = self._image.shape[:3]
        self._mask = np.zeros((height, width,channel), dtype=np.uint8)
        self._flood_mask = np.zeros((height + 2, width + 2), dtype=np.uint8)
        self.connectivity = connectivity
        self.tolerance = None
        self.set_tolerance(tolerance)
        self._flood_fill_flags = (
                self.connectivity | cv.FLOODFILL_FIXED_RANGE | cv.FLOODFILL_MASK_ONLY | 255 << 8
        )  

    def reset_image(self):
        self._image = self._origin

    def reset_mask(self):
        height, width = self._image.shape[:2]
        self._mask = np.zeros((height, width), dtype=np.uint8)

    def backup_mask(self):
        return self._mask.copy()

    def restore_mask(self, mask):
        assert self._mask.shape == mask.shape, "Shape mismatch between masks"
        self._mask = mask.copy()

    def set_tolerance(self, value):
        self.tolerance = (value,) * 3

    def set_connectivity(self, value):
        self.connectivity = value

    def set_mask(self, x, y, option='or'):
        self._flood_mask[:] = 0
        cv.floodFill(
            self._image,
            self._flood_mask,
            (x, y),
            0,
            self.tolerance,
            self.tolerance,
            self._flood_fill_flags,
        )
        flood_mask = self._flood_mask[1:-1, 1:-1].copy()

        if option == 'and':
            self._mask = cv.bitwise_and(self._mask, flood_mask)
        elif option == 'or':
            self._mask = cv.bitwise_or(self._mask, flood_mask)
        elif option == 'sub':
            self._mask = cv.bitwise_and(self._mask, cv.bitwise_not(flood_mask))
        else:
            self._mask = flood_mask

    def get_image(self):
        # image = self._image  
 
        image = cv.cvtColor(self._image, cv.COLOR_BGR2RGB)
        # print(self._image.shape)
       
        height, width,channel = image.shape[:3]
        # print(height,width,channel)
        # print(QImage(image, width, height, QImage.Format_RGB888))
        return QImage(image, width, height,width*channel, QImage.Format_RGB888)

    def get_mask(self):
        # print('None')
        
        mask = cv.bitwise_not(self._mask)

        # print('hi1')        
        mask = cv.cvtColor(mask, cv.COLOR_BGR2RGB)
        # print(self._mask.shape)

        
        height, width, channel = self._image.shape[:3]
        mono = QImage(mask, width, height,width*channel, QImage.Format_RGB888)

        
        bitmap = QBitmap(width, height).fromImage(mono)
        return bitmap

    def get_polygon(self):
        contours, hierarchy = cv.findContours(self._mask, cv.RETR_CCOMP, cv.CHAIN_APPROX_NONE)
        if len(contours) < 1:
            return None

        
        

        key = np.array([cv.contourArea(contour) for contour in contours])
        index = np.argmax(key)
        x = contours[index][:, 0][:, 0].tolist()
        y = contours[index][:, 0][:, 1].tolist()

        
        if hierarchy[0][index][2] != -1:
            
            x.extend(contours[hierarchy[0][index][2]][:, 0][:, 0].tolist())
            y.extend(contours[hierarchy[0][index][2]][:, 0][:, 1].tolist())

        elif hierarchy[0][index][3] != -1:
            
            x = contours[hierarchy[0][index][2]][:, 0][:, 0].tolist() + x
            y = contours[hierarchy[0][index][2]][:, 0][:, 1].tolist() + y

        
        polygon = QPolygonF()
        for idx in range(len(x)):
            polygon.append(QPointF(x[idx], y[idx]))

        return polygon

    def paint_mask(self, x, y, width):
        m_height, m_width = self._mask.shape[:2]
        assert x >= 0 and x < m_width \
               and y >= 0 and y < m_height, "Invalid paint position"
        cv.circle(self._mask, center=(x, y), radius=int(width / 2), color=255, thickness=-1)

    def erase_mask(self, x, y, width):
        m_height, m_width = self._mask.shape[:2]
        assert x >= 0 and x < m_width \
               and y >= 0 and y < m_height, "Invalid erase position"
        cv.circle(self._mask, center=(x, y), radius=int(width / 2), color=0, thickness=-1)

    def grayscale(self):
        
        self._image = cv.cvtColor(self._image, cv.COLOR_BGR2GRAY)

        
        self._image = cv.equalizeHist(self._image)
        print('hi2')  
    def crack_detector_opening(self, opening_kernel_size):
        
        SUBTRACTION_THRESHOLD_VALUE = 20
        MEDIAN_FILTER_SIZE = 39
        MORPHOLOGICAL_OPENING_KERNEL_SIZE = opening_kernel_size

        
        image = self._image
        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        
        gray = image.copy()
        image = cv.medianBlur(image, MEDIAN_FILTER_SIZE)

        
        image = cv.subtract(image, gray)

        
        if opening_kernel_size > 0:
            opening_kernel = np.ones((MORPHOLOGICAL_OPENING_KERNEL_SIZE, MORPHOLOGICAL_OPENING_KERNEL_SIZE), np.uint8)
            image = cv.morphologyEx(image, cv.MORPH_OPEN, opening_kernel)

        
        image = image + image * (image > SUBTRACTION_THRESHOLD_VALUE)

        self._image = image

    def crack_detector(self, opening_kernel_size, closing_kernel_size):
        """ 이미지 전처리를 통해서 균열을 찾는다.

            논문 "INTELIGENT CRACK DETECTING ALGORITHM ON THE CONCRETE
                CRACK IMAGE USING NEURAL NETWORK, Hyeong-Gyeong Moon and Jung-Hoon Kim" 참조
        """
        
        GAUSSIAN_FILTER_SIZE = 5
        GAUSSIAN_FILTER_SIG = 0.5
        MORPHOLOGICAL_CLOSING_KERNEL_SIZE = closing_kernel_size

        
        self.crack_detector_opening(opening_kernel_size)
        print('hi3')  
        
        image = self._image
        image = cv.GaussianBlur(image, (GAUSSIAN_FILTER_SIZE, GAUSSIAN_FILTER_SIZE),
                                GAUSSIAN_FILTER_SIG)

        
        _, image = cv.threshold(image, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

        
        closing_kernel = np.ones((MORPHOLOGICAL_CLOSING_KERNEL_SIZE, MORPHOLOGICAL_CLOSING_KERNEL_SIZE), np.uint8)
        image = cv.morphologyEx(image, cv.MORPH_CLOSE, closing_kernel)

        self._image = image

    def edge_detector(self, canny_min, canny_max):
        MEDIAN_FILTER_SIZE = 5

        
        image = self._image
        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        
        image = cv.equalizeHist(image)

        
        image = cv.medianBlur(image, MEDIAN_FILTER_SIZE)

        print('hi4')          
        image = cv.Canny(image, canny_min, canny_max)

        self._image = image
