# this file contains all tools (classes, methodes and others) to define a chinese chess board

# regularities:
# piece.side == 1 if red, 2 if black
# piece.name is one of 'T_R', 'T_B', 'S_R', 'S_B', 'V_R', 'V_B', 'X', 'P', 'M', 'C_R', 'C_B'
# positioning: row is from 1 to 10 upside down, and column is from 1 to 9 from left to right


class Position:
    # constructor
    def __init__(self, x, y):
        if x < 1 or x > 10 or y < 1 or y > 9:
            print('quan co nam ngoai ban co')
            assert False
        self.x = x
        self.y = y


class Move:
    # constructor
    def __init__(self, old_pos, new_pos):
        self.old_pos = old_pos
        self.new_pos = new_pos


class Piece:
    # constructor: initialize a piece
    def __init__(self, board, position, side, is_dead=False):
        self.board = board
        self.position = position
        self.side = side
        self.is_dead = is_dead
    # methods

    def set_killed(self):
        self.is_dead = True

    # check if the move is valid, pass it to be inherited by subclasses
    def is_valid_move(self, new_position):
        pass

    def update_piece(self, new_position):
        self.position = new_position


# TODO Ma
# TODO Phao


# Piece Si
class PieceSi(Piece):
    # constructor
    def __init__(self, board, position, side, is_dead=False):
        super(PieceSi, self).__init__(board, position, side, is_dead)
        self.name = 'Si    '
    # methods


# TODO Tinh


# Piece Tot
class PieceTot(Piece):
    # constructor
    def __init__(self, board, position, side, is_dead=False):
        super(PieceTot, self).__init__(board, position, side, is_dead)
        self.name = 'Tot   '
    # methods


# Piece Tuong
class PieceTuong(Piece):
    # constructor
    def __init__(self, board, position, side, is_dead=False):
        super(PieceTuong, self).__init__(board, position, side, is_dead)
        self.name = 'Tuong '

    def available_new_pos(self):
        res = []
        changes = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        for change in changes:
            new_pos = Position(self.position.x + change[0], self.position.y + change[1])
            if new_pos is not None:
                res.append(new_pos)
        return res

    # methods
    # check valid move
    def is_valid_move(self, new_position):
        if self.side == 1:  # red Tuong
            if not new_position.x in [8, 9, 10] or not new_position.y in [4, 5, 6]:
                print('Tuong khong nam trong cung tuong')
                assert False
            piece = self.board.get_piece(new_position)
            new_positions = self.available_new_pos()
            if not new_position in new_positions:
                print('Vi tri moi khong dung')
                assert False
            if piece.side == self.side:
                print('Khong the tu an quan cua minh')
                assert False
            return True
        # if self.side == 2:  # black Tuong
        else:
            if not new_position.x in [1, 2, 3] or not new_position.y in [4, 5, 6]:
                print('Tuong khong nam trong cung tuong')
                assert False
            piece = self.board.get_piece(new_position)
            new_positions = self.available_new_pos()
            if not new_position in new_positions:
                print('Vi tri moi khong dung')
                assert False
            if piece.side == self.side:
                print('Khong the tu an quan cua minh')
                assert False
            return True


# TODO Piece Xe


class Board:
    # constructor: initialize an empty board
    def __init__(self):
        self.pieces = []
        self.n_r = 0  # number of red pieces
        self.n_b = 0  # number of black pieces
        self.next_to_move = 0  #

    # get a piece from a board
    def get_piece(self, position):
        for piece in self.pieces:
            if piece.position.x == position.x and piece.position.y == position.y:
                return piece
        return None

    def add_piece(self, piece):
        assert not piece.is_dead  # if piece is dead -> stop
        assert self.get_piece(piece.position) is None  # if there is another piece at this position -> stop
        self.pieces.append(piece)
        if piece.side == 1:
            self.n_r += 1
        elif piece.side == 2:
            self.n_b += 1



    # initialize a board with the initial state of a chinese chess board
    def gen_start_board(self):
        self.next_to_move = 1  # red player to move
        self.pieces = []
        self.n_r = 0  # number of red pieces
        self.n_b = 0  # number of black pieces
        self.add_piece(PieceTuong(self, Position(10, 5), 1))
        self.add_piece(PieceTot(self, Position(7, 5), 1))
        self.add_piece(PieceSi(self, Position(10, 4), 1))
        self.add_piece(PieceSi(self, Position(10, 6), 1))
        self.add_piece(PieceTuong(self, Position(1, 5), 2))
        self.add_piece(PieceTot(self, Position(4, 5), 2))
        self.n_r = 4
        self.n_b = 2
        # TODO add more pieces

    # check if a new move is valid
    def is_valid_move(self, move):
        piece = self.get_piece(move.old_pos)
        if piece is None:
            return False
        elif not piece.side == self.next_to_move:
            return False
        else:
            return piece.is_valid_move(move.new_pos)

    # update state
    def update_board(self, move):
        assert self.is_valid_move(move)
        self.next_to_move = 3 - self.next_to_move  # make alternative move
        piece = self.get_piece(move.old_pos)
        target = self.get_piece(move.new_pos)
        if target is not None:
            target.set_killed()
            if target.side == 1:
                self.n_r -= 1
            else:
                self.n_b -= 1
        piece.update_piece(move.new_pos)

    # display board
    def display_board(self):
        for row in range(1, 10 + 1):
            cur_row = ''
            for col in range(1, 9 + 1):
                piece = self.get_piece(Position(row, col))
                if piece is None:
                    cur_row += 'XXXX  '
                else:
                    cur_row += piece.name
            print(cur_row)

    # gen board from a list 2d
    def gen_board_from_state(self, list_2d):
        self.pieces = []
        self.n_r = 0
        self.n_b = 0
        n_row = len(list_2d)
        n_col = len(list_2d[0])
        for row in range(0, n_row):
            for col in range(0, n_col):
                if not list_2d[row][col] == 0:
                    position = Position(row + 1, col + 1)
                    if list_2d[row][col] in range(1, 8):
                        side = 1
                    else:
                        side = 2
                    # TODO add more cases for all types of pieces
                    if list_2d[row][col] in [3, 10]:
                        self.add_piece(PieceSi(self, position, side))
                    elif list_2d[row][col] in [5, 12]:
                        self.add_piece(PieceTot(self, position, side))
                    elif list_2d[row][col] in [6, 13]:
                        self.add_piece(PieceTuong(self, position, side))






