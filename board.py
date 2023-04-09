from PyQt6.QtWidgets import QGraphicsScene
from PyQt6.QtCore import pyqtSignal


class ChessBoard(QGraphicsScene):
    pieceMoved = pyqtSignal(object)
