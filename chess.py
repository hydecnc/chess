from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtCore import QSize, QPointF
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
        self.scene.checkLegal.connect(self.legalSquares)

        self.colors = {
            'black': QColor(118, 150, 86),
            'white': QColor(238, 238, 210),
        }
        self.turn = "white"
        self.moves = []
        
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
        print(fen)

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
        
        for file in range(8):
            for rank in range(8):
                if isinstance(self.board[file][rank], ChessPiece):
                    if self.board[file][rank].color != self.turn:
                        self.board[file][rank].setEnabled(False)
                    else:
                        self.board[file][rank].setEnabled(True)

    def change_turn(self, cur):
        self.turn = "black" if cur == "white" else "white"
        for file in range(8):
            for rank in range(8):
                if isinstance(self.board[file][rank], ChessPiece):
                    if self.board[file][rank].color != self.turn:
                        self.board[file][rank].setEnabled(False)
                    else:
                        self.board[file][rank].setEnabled(True)

    
    
    def handlePieceMoved(self, piece):
        move = self.board[piece.prev_file][piece.prev_rank].symbol if self.board[piece.prev_file][piece.prev_rank].type != "pawn" else ""

        if isinstance(self.board[piece.file][piece.rank], ChessPiece):
            self.scene.removeItem(self.board[piece.file][piece.rank])
            self.board[piece.file][piece.rank] = 0
            move += 'x' if self.board[piece.prev_file][piece.prev_rank].type != "pawn" else f"{self.board[piece.prev_file][piece.prev_rank].coord()[0]}x"
        move += ''.join(piece.coord())
            
        self.change_turn(piece.color)
        self.board[piece.prev_file][piece.prev_rank], self.board[piece.file][piece.rank] = self.board[piece.file][piece.rank], self.board[piece.prev_file][piece.prev_rank]
        self.moves.append(move)
    
    def legalSquares(self, piece):
        if isinstance(self.board[piece.new_file][piece.new_rank], ChessPiece):
            if self.board[piece.new_file][piece.new_rank].color != piece.color:
                piece.take = True
            else:
                piece.take = False
        
        # Rook
        if piece.up != 0:
            for i in range(piece.up):
                if isinstance(self.board[piece.file - i - 1][piece.rank], ChessPiece):
                    piece.up = i + 1
                    break
        if piece.down != 0:
            for i in range(piece.down):
                if isinstance(self.board[piece.file + i + 1][piece.rank], ChessPiece):
                    piece.down = i + 1
                    break
        if piece.left != 0:        
            for i in range(piece.left):
                if isinstance(self.board[piece.file][piece.rank - i - 1], ChessPiece):
                    piece.left = i + 1
                    break
        if piece.right != 0:        
            for i in range(piece.right):
                if isinstance(self.board[piece.file][piece.rank + i + 1], ChessPiece):
                    piece.right = i + 1
                    break

        # Bishop
        if piece.UL != 0:
            for i in range(piece.UL):
                if isinstance(self.board[piece.file - i - 1][piece.rank - i - 1], ChessPiece):
                    piece.UL = i + 1
                    break
        if piece.UR != 0:
            for i in range(piece.UR):
                if isinstance(self.board[piece.file - i - 1][piece.rank + i + 1], ChessPiece):
                    piece.UR = i + 1
                    break
        if piece.DL != 0:
            for i in range(piece.DL):
                if isinstance(self.board[piece.file + i + 1][piece.rank - i - 1], ChessPiece):
                    piece.DL = i + 1
                    break
        if piece.DR != 0:
            for i in range(piece.DR):
                if isinstance(self.board[piece.file + i + 1][piece.rank + i + 1], ChessPiece):
                    piece.DR = i + 1
                    break
            
    def print_board(self):
        for file in range(8):
            for rank in range(8):
                if type(self.board[file][rank]) == type(1):
                    print("None", end=" ")
                else:
                    print(self.board[file][rank].type, end=" ")
            print()

    def generate_fen(self):
        fen = ""
        for file in range(7, -1, -1):
            count = 0
            for rank in range(8):
                if isinstance(self.board[file][rank], ChessPiece):
                    fen += str(count) if count > 0 else ''
                    count = 0
                    fen += self.board[file][rank].symbol
                else:
                    count += 1

            fen += str(count) if count > 0 else ''
            fen += '/'
        return fen[:len(fen)-1]