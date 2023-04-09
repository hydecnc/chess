import sys

from PyQt6.QtWidgets import QApplication, QGraphicsView, QMainWindow, QHBoxLayout, QWidget, QPushButton
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QColor

from piece import ChessPiece
from tiles import ChessTile
from board import ChessBoard


class Chess(QGraphicsView):
    def __init__(self) -> None:
        super().__init__()
        self.setMinimumSize(QSize(800, 800))
        self.scene = ChessBoard()
        self.setScene(self.scene)

        self.scene.pieceMoved.connect(self.handlePieceMoved)

        self.colors = {
            'black': QColor(118, 150, 86),
            'white': QColor(238, 238, 210),
        }
        
        # print(self.size().width()/8, self.size().height()/8)

        # Define the width and height
        self.WIDTH = self.contentsRect().width()
        self.HEIGHT = self.contentsRect().height()
        self.setSceneRect(0, 0, self.WIDTH, self.HEIGHT)

        self.tiles = [[0 for i in range(8)] for j in range(8)]
        self.board = [[0 for i in range(8)] for j in range(8)]

        # Generate Board
        pos = {'x': 0, 'y':0}
        for file in range(8):
            for rank in range(8):
                color = self.colors['white'] if (file + rank) % 2 == 0 else self.colors['black']
                tile = ChessTile(pos['x'], pos['y'], self.WIDTH/8, self.HEIGHT/8, color=color)

                self.tiles[file][rank] = tile
                self.scene.addItem(tile)

                pos['x'] += self.WIDTH/8
            pos['x'] = 0
            pos['y'] += self.HEIGHT/8
        
        # Place the pieces
        self.piece_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
        fen = self.piece_fen.split('/')
        # print(fen)

        pos = {'x': 0, 'y':0}
        for file in range(8):
            for rank in range(8):
                # print(file, rank)
                if fen[file][rank].isdigit():
                    pos['x'] += int(fen[file][rank]) * (self.WIDTH/8)
                    rank += int(fen[file][rank])

                    if rank >= 8:
                        break
                else:
                    piece = ChessPiece(fen[file][rank], pos['x'], pos['y'], self.WIDTH)
                    # piece.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
                    
                    self.board[file][rank] = piece
                    self.scene.addItem(piece)
                    pos['x'] += self.WIDTH/8
            pos['x'] = 0
            pos['y'] += self.HEIGHT/8
        # print(self.board)
    
    def handlePieceMoved(self, piece):
        # print(f"From {(piece.prev_rank, piece.prev_ypos)} to {(piece.xpos, piece.ypos)}")
        if isinstance(self.board[piece.file][piece.rank], ChessPiece):
            # self.board[piece.ypos][piece.xpos].piece.removeItem()
            self.scene.removeItem(self.board[piece.file][piece.rank])
            self.board[piece.file][piece.rank] = 0
        self.board[piece.prev_file][piece.prev_rank], self.board[piece.file][piece.rank] = self.board[piece.file][piece.rank], self.board[piece.prev_file][piece.prev_rank]
        self.print_board()
    
    def print_board(self):
        for file in range(8):
            for rank in range(8):
                if type(self.board[file][rank]) == type(1):
                    print("None", end=" ")
                else:
                    print(self.board[file][rank].type, end=" ")
            print()
    
    def check_overlapping(self):
        for file in range(8):
            for rank in range(8):
                if not self.board[file][rank] == 0:
                    if not (file, rank) == self.board[file][rank].pos():
                        print(f"{self.board[file][rank]} Sussy")

    def update_board(self, fen):   
        pass
    

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.setMinimumSize(QSize(1000, 800))

        layout = QHBoxLayout()
        # layout.addWidget(AhChessPiece('r', 0, 0, 800))

        chess = Chess()
        layout.addWidget(chess)

        # layout.addWidget(QPushButton("HI"))
        # print(chess_board.board)
        
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
