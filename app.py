import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget
from PyQt6.QtCore import QSize

from chess import Chess

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.setMinimumSize(QSize(1000, 800))

        layout = QHBoxLayout()

        chess = Chess()
        layout.addWidget(chess)
        
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

app = QApplication(sys.argv)

# view = ChessBoard()
# view.setRenderHint(QPainter.RenderHint.Antialiasing)
# view.show()

test = MainWindow()
test.show()

app.exec()
