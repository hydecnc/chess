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


        self.setPos(x, y)
        self.setScale(size/8/IMAGE_SIZE)
        self.setTransformationMode(Qt.TransformationMode.SmoothTransformation)
        self.setAcceptHoverEvents(True)
    
        # Get the initial position of the piece
        self.rank = round(self.x()/(self.size/8))
        self.file = round(self.y()/(self.size/8))
        self.prev_rank = round(self.x()/(self.size/8))
        self.prev_file = round(self.y()/(self.size/8))
        self.prev_pos = [(self.prev_file, self.prev_rank)]
        self.new_xpos = self.x()
        self.new_ypos = self.y()
    

    # TODO: diplay attacking squares with red color when the piece is released
    def display_attaking_squares(self):
        pass

    def hoverEnterEvent(self, event):
        self.setCursor(QCursor(Qt.CursorShape.OpenHandCursor))
    
    def hoverLeaveEvent(self, event):
        pass
    
    def mousePressEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        orig_cursor_position = event.lastScenePos()
        updated_cursor_position = event.scenePos()

        orig_position = self.scenePos()
        
        self.new_xpos = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
        self.new_ypos = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()

        self.setPos(QPointF(self.new_xpos, self.new_ypos))

    def mouseReleaseEvent(self, event):
        # print(self.prev_rank*self.size/8, self.prev_file*self.size/8)

        self.new_rank = round(self.new_xpos/(self.size/8))
        self.new_file = round(self.new_ypos/(self.size/8))
        # print(f"xpos: {xpos}, ypos: {ypos}")
        
        # print(f"og: ({self.xpos}, {self.ypos}) vs. new: {(new_xpos, new_ypos)}")
        if self.new_rank != self.rank or self.new_file != self.file:
            self.prev_rank = self.rank
            self.prev_file = self.file
            self.prev_pos.append((self.prev_rank, self.prev_file))
            self.rank = self.new_rank
            self.file = self.new_file    
            self.rollback()
            self.scene().pieceMoved.emit(self)
            # print(f"{self.color} moved to {(self.rank, self.file)} from {(self.prev_rank, self.prev_file)}")

        self.setPos(QPointF(self.rank*self.size/8, self.file*self.size/8))
        # self.setPos(QPointF(self.prev_rank*self.size/8, self.prev_file*self.size/8))
    
    def rollback(self):
        print(self.prev_file, self.prev_rank)
        # print("rollback")
