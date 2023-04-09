from PyQt6.QtWidgets import QGraphicsRectItem
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen

class ChessTile(QGraphicsRectItem):
    def __init__(self, x, y, w, h, color) -> None:
        super().__init__(0, 0, w, h)
        
        self.setPos(x, y)
        self.setBrush(color)

        pen = QPen(Qt.GlobalColor.black)
        pen.setStyle(Qt.PenStyle.NoPen)
        self.setPen(pen)