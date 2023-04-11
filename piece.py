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
                self.moved = False
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
        self.new_rank = round(self.new_xpos/(self.size/8))
        self.new_file = round(self.new_ypos/(self.size/8))

        # Move the piece back when it's out of the board
        if self.new_rank < 0 or self.new_rank > 7 or self.new_file < 0 or self.new_file > 7:
            self.rollback()
            return
        
        # Calculate number of square until the end of the board
        self.left = self.rank
        self.right = 7 - self.rank
        self.up = self.file
        self.down = 7 - self.file

        self.UL = min(self.up, self.left)
        self.UR = min(self.up, self.right)
        self.DL = min(self.down, self.left)
        self.DR = min(self.down, self.right)


        # Check if piece moved
        self.rank_gap = self.new_rank - self.rank
        self.file_gap = self.new_file - self.file

        if self.new_rank != self.rank or self.new_file != self.file:
            self.valid = self.validateMove()
            if not self.valid:
                return


            self.prev_rank = self.rank
            self.prev_file = self.file
            self.prev_pos.append((self.prev_rank, self.prev_file))
            self.rank = self.new_rank
            self.file = self.new_file

            self.scene().pieceMoved.emit(self)
            self.setPos(QPointF(self.rank*self.size/8, self.file*self.size/8))

        self.rollback()

    def validateMove(self):
        # legal moves
        self.take = True
        self.scene().checkLegal.emit(self)

        if not self.take:
            self.rollback()
            return False

        match self.type:
            # TODO: implement pawn's legal moves
            case "pawn":
                pass
            case "knight":
                if (abs(self.file_gap) != 1 or abs(self.rank_gap) != 2) and (abs(self.rank_gap) != 1 or abs(self.file_gap) != 2):
                    self.rollback()
                    return False
            # TODO: not let pieces jump above others
            case "bishop":
                if abs(self.file_gap) != abs(self.rank_gap):
                    self.rollback()
                    return False
                
                if not self.validBishopMove():
                    self.rollback()
                    return False
                
            case "rook":
                if self.new_file != self.file and self.new_rank != self.rank:
                    self.rollback()
                    return False
                
                if not self.validRookMove():
                    self.rollback()
                    return False
                
            case "queen":
                if (self.new_file != self.file and self.new_rank != self.rank) and (abs(self.file_gap) != abs(self.rank_gap)):
                    self.rollback()
                    return False

                if not self.validRookMove() or not self.validBishopMove():
                    self.rollback()
                    return False
        
            case "king":
                if abs(self.file_gap) > 1 or abs(self.rank_gap) > 1:
                    self.rollback()
                    return False
        return True
    
    def validRookMove(self):
        # print(f"rank gap: {self.rank_gap}, file gap: {self.file_gap}")
        if self.file_gap < 0:
            if abs(self.file_gap) > self.up:
                return False
        if self.file_gap > 0:
            if abs(self.file_gap) > self.down:
                return False
        if self.rank_gap < 0:
            if abs(self.rank_gap) > self.left:
                return False
        if self.rank_gap > 0:
            if abs(self.rank_gap) > self.right:
                return False
        return True
    
    def validBishopMove(self):
        if self.file_gap < 0 and self.rank_gap < 0:
            if abs(self.file_gap) > self.UL:
                return False
        if self.file_gap < 0 and self.rank_gap > 0:
            if abs(self.file_gap) > self.UR:
                return False
        if self.file_gap > 0 and self.rank_gap < 0:
            if abs(self.file_gap) > self.DL:
                return False
        if self.file_gap > 0 and self.rank_gap > 0:
            if abs(self.file_gap) > self.DR:
                return False
        return True

    def rollback(self):
        """
        Bring the piece back to its original position
        """
        self.prev_rank = self.rank
        self.prev_file = self.file
        self.setPos(QPointF(self.prev_rank*self.size/8, self.prev_file*self.size/8))
