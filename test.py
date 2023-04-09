import sys

from PyQt6.QtWidgets import QApplication, QGraphicsPixmapItem, QGraphicsView, QGraphicsItem, QGraphicsRectItem, QGraphicsScene
from PyQt6.QtCore import QPointF, Qt, QUrl, QObject, pyqtSignal
from PyQt6.QtGui import QPixmap, QCursor, QPalette, QColor
from PyQt6.QtMultimedia import QSoundEffect

class View(QGraphicsView):
    def __init__(self) -> None:
        super().__init__()
        self.scene = Scene()
        self.setScene(self.scene)
        self.scene.pieceMoved.connect(self.hi)

        self.scene.addItem(ChessPiece())
    
    def hi(self, item):
        print("hi")
        print(item)

class Scene(QGraphicsScene):
    pieceMoved = pyqtSignal(object)

class ChessPiece(QGraphicsPixmapItem):
    def __init__(self) -> None:
        super().__init__(QPixmap(f"images/white/rook.png"))
        self.setAcceptHoverEvents(True)
        # print("sd")
        self.setPos(100, 100)

    def hoverEnterEvent(self, event):
        self.setCursor(QCursor(Qt.CursorShape.OpenHandCursor))

    def mouseMoveEvent(self, event):
        orig_cursor_position = event.lastScenePos()
        updated_cursor_position = event.scenePos()

        orig_position = self.scenePos()
        
        self.new_xpos = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
        self.new_ypos = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()
        
        self.setPos(QPointF(self.new_xpos, self.new_ypos))
    
    def mouseReleaseEvent(self, event):
        print("H")
        self.scene.pieceMoved.emit(self)
    
    # def move(self):
    #     self.setPos(500, 500)


app = QApplication(sys.argv)
view = View()
view.show()

app.exec()
