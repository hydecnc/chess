from PyQt6.QtWidgets import QGraphicsPixmapItem, QWidget, QGraphicsItem
from PyQt6.QtCore import QPointF, Qt, QUrl, QObject
from PyQt6.QtGui import QPixmap, QCursor, QPalette, QColor
from PyQt6.QtMultimedia import QSoundEffect

IMAGE_SIZE = 334

class ChessPiece(QGraphicsPixmapItem):
    def __init__(self, type, x, y, size) -> None:
        self.size = size
        self.color = "white" if type.islower() else "black"
        self.type = ""
        match type.lower():
            case 'p':
                self.type = "pawn"
            case 'n':
                self.type = "knight"
            case 'b':
                self.type = "bishop"
            case 'r':
                self.type = "rook"
            case 'q':
                self.type = "queen"
            case 'k':
                self.type = "king"
        super().__init__(QPixmap(f"images/{self.color}/{self.type}.png"))


        # self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        # self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)
        # print(f"Added {self.type}")
        
        # self._signal = Signal()


        self.setPos(x, y)
        self.setScale(size/8/IMAGE_SIZE)
        self.setTransformationMode(Qt.TransformationMode.SmoothTransformation)
        self.setAcceptHoverEvents(True)
    
        # Get the initial position of the piece
        self.prev_rank = round(self.x()/(self.size/8))
        self.prev_file = round(self.y()/(self.size/8))
        self.new_rank = self.x()
        self.new_file = self.y()
    


        # print(f"{self.type} added at ({self.xpos}, {self.ypos})")

    # def itemChange(self, change, value):
    #     pass
    #     if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
    #         print(value)
    
    # TODO: diplay attacking squares with red color when the piece is released
    def display_attaking_squares(self):
        pass

    def hoverEnterEvent(self, event):
        # piece.instance().setOverrideCursor(Qt.CursorShape.OpenHandCursor)
        self.setCursor(QCursor(Qt.CursorShape.OpenHandCursor))
    
    def hoverLeaveEvent(self, event):
        pass
    
    def mousePressEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        orig_cursor_position = event.lastScenePos()
        updated_cursor_position = event.scenePos()

        orig_position = self.scenePos()
        
        self.new_rank = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
        self.new_file = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()
        
        self.setPos(QPointF(self.new_rank, self.new_file))

    def mouseReleaseEvent(self, event):

        self.rank = round(self.new_rank/(self.size/8))
        self.file = round(self.new_file/(self.size/8))
        # print(f"xpos: {xpos}, ypos: {ypos}")
        
        # print(f"og: ({self.xpos}, {self.ypos}) vs. new: {(new_xpos, new_ypos)}")
        if self.rank != self.prev_rank or self.file != self.prev_file:
            self.scene().pieceMoved.emit(self)
            self.prev_rank = self.rank
            self.prev_file = self.file

        self.setPos(QPointF(self.rank*self.size/8, self.file*self.size/8))

        # print(self.pos().x(), self.pos().y())

        # sound = QSoundEffect()
        # sound.setSource(QUrl.fromLocalFile("media/ficha-de-ajedrez-34722.mp3"))
        # sound.setLoopCount(-2)
        # sound.play()
    

# class AhChessPiece(QWidget):
#     def __init__(self, type, x, y, size) -> None:
#         super().__init__()
#         self.piece = ChessPiece(type, x, y, size)
        
#         self.setAutoFillBackground(True)

#         palette = self.palette()
#         palette.setColor(QPalette.ColorRole.Window, QColor('red'))
#         self.setPalette(palette)

#     def mouseReleaseEvent(self, event):
#         print("AhChessPiece Clicked")
#         self.piece.mouseMoveEvent()
