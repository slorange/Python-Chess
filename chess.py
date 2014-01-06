import kivy
kivy.require('1.0.9') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.core.image import Image
import math
from pprint import pprint
from Point import Point
import copy
import time


class UI(Widget):
    BOARD_SIZE = 500;
    LIGHT_COLOR = Color(0.4, 0.2, 0);
    DARK_COLOR = Color(1, 0.7, 0.3);
    VALID_COLOR = Color(0.8, 0.3, 0.8);
    WHITE_COLOR = Color(1, 1, 1);
    SQUARE_SIZE = BOARD_SIZE / 8;
    BASE_X = Window.center[0] - BOARD_SIZE/2
    BASE_X = Window.center[0] - BOARD_SIZE/2
    BASE_Y = Window.center[1] - BOARD_SIZE/2
    
    def __init__(self, **kwargs):
        super(UI, self).__init__(**kwargs)
        self.board = Board(self);
        
    def on_touch_down(self, touch):
        x = int((touch.x - UI.BASE_X) // UI.SQUARE_SIZE);
        y = int((touch.y - UI.BASE_Y) // UI.SQUARE_SIZE);
        self.board.on_touch_down(x, y);
    
    def draw_board(self, board, valid):
        #print("drawing board")
        square_size = UI.SQUARE_SIZE;
        base_x = UI.BASE_X;
        base_y = UI.BASE_Y;
        
        #board
        for x in range(0, 8):
            for y in range(0, 8):
                is_valid = Point(x,y) in valid
                main_color = UI.LIGHT_COLOR if (x+y) % 2 == 0 else UI.DARK_COLOR
                self.canvas.add(UI.VALID_COLOR) if is_valid else self.canvas.add(main_color)
                self.canvas.add(Rectangle(pos=(square_size * x + base_x, square_size * y + base_y), size=(square_size, square_size)))
                if is_valid:
                    self.canvas.add(main_color)
                    self.canvas.add(Rectangle(pos=(square_size * (x+0.125) + base_x, square_size * (y+0.125) + base_y), size=(square_size*3/4, square_size*3/4)))
        
        #pieces
        self.canvas.add(UI.WHITE_COLOR)
        base_x += square_size*1/8
        base_y += square_size*1/8
        piece_size = (square_size*3/4, square_size*3/4)
        for x in range (0,8):
            for y in range (0,8):
                if board[x][y] is not None:
                    texture = Image('images/'+str(board[x][y])+'.png').texture
                    self.canvas.add(Rectangle(texture=texture, pos=(square_size * x + base_x, square_size * y + base_y), size=piece_size))
        
                    
class Board(object):

    #test board is used by AI to try moves
    #some code isn't executed by test board to speed up AI
    def __init__(self, ui = None):
        self.board = [[None for i in range(8)] for j in range(8)]
        self.valid = [];
        self.ui = ui;
        if ui is not None:
            self.test = False;
            self.new_game();
        else:
            self.test = True;
   
    def on_touch_down(self, x, y):
        p = Point(x,y);
        if not self.on_board(x, y): return
        Piece = self.board[x][y]
        if Piece is not None and Piece.color == self.turn: #first click
            self.valid = Piece.get_valid_moves()
            Board.selected = Piece
            self.draw_board();
        elif p in self.valid: #second click
            b = self.move(Board.selected, p);
            Board.selected = None;
            self.valid = [];
            self.draw_board();
            if b:
                self.next_turn();
            else:
                pass
                # content = Button(text='OK')
                # popup = Popup(title='Cannot put king into check', content=content, auto_dismiss=False)
                # content.bind(on_press=popup.dismiss)
                # popup.open()
            
    def move(self, piece, loc):
        if not self.test: #implementing undo will get rid of this hack
            backup_board = [[copy.copy(self.board[i][j]) for j in range(8)] for i in range(8)]
            
        self.board[piece.X][piece.Y] = None;
        self.board[loc.X][loc.Y] = piece;
        piece.move(loc.X, loc.Y);
        
        if not self.test:
            #if king is in check, undo
            if self.is_in_check(piece.color):
                self.board = backup_board;
                return False;
        return True;
            
        
    def is_in_check(self, color):
        #get king's location
        kings_pieces = self.get_pieces(color);
        for piece in kings_pieces:
            if isinstance(piece, King):
                kings_location = Point(piece.X, piece.Y)
                
        enemy_pieces = self.get_pieces(Board.other_color(color));
        for piece in enemy_pieces:
            moves = piece.get_valid_moves();
            for move in moves:
                if move == kings_location:
                    print("King is in check at " +str(move))
                    return True;
        return False;
                
        
    def new_game(self):
        #pieces = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        self.board[0][0] = Rook('W', 'R', self, 0, 0);
        self.board[7][0] = Rook('W', 'R', self, 7, 0);
        self.board[1][0] = Knight('W', 'N', self, 1, 0);
        self.board[6][0] = Knight('W', 'N', self, 6, 0);
        self.board[2][0] = Bishop('W', 'B', self, 2, 0);
        self.board[5][0] = Bishop('W', 'B', self, 5, 0);
        self.board[3][0] = Queen('W', 'Q', self, 3, 0);
        self.board[4][0] = King('W', 'K', self, 4, 0);
        self.board[0][7] = Rook('B', 'R', self, 0, 7);
        self.board[7][7] = Rook('B', 'R', self, 7, 7);
        self.board[1][7] = Knight('B', 'N', self, 1, 7);
        self.board[6][7] = Knight('B', 'N', self, 6, 7);
        self.board[2][7] = Bishop('B', 'B', self, 2, 7);
        self.board[5][7] = Bishop('B', 'B', self, 5, 7);
        self.board[3][7] = Queen('B', 'Q', self, 3, 7);
        self.board[4][7] = King('B', 'K', self, 4, 7);
        for x in range (0,8):
            self.board[x][1] = Pawn('W', 'P', self, x, 1);
            self.board[x][6] = Pawn('B', 'P', self, x, 6);
        self.turn = 'W';
        #self.print_board();
        self.draw_board();
        print("Starting new game")
    
    def get_pieces(self, color):
        #TODO make player class and keep list of pieces
        rtn = [];
        for x in range (0,8):
            for y in range (0,8):
                if self.board[x][y] is not None:
                    if self.board[x][y].color == color:
                        rtn += [self.board[x][y]];
        return rtn;
    
    def next_turn(self):
        if(self.turn == 'W'):
            self.turn = 'B';
            AI_move = AI.make_move(self, 'B', 2);
            self.move(AI_move[0], AI_move[1]);
            self.draw_board();
            self.turn = 'W';
        else:
            self.turn = 'W';
    
    def on_board(self, x, y):
        return x >= 0 and x < 8 and y >= 0 and y < 8
    
    #deep copy
    def copy_board(self):
        test_board = Board();
        test_board.board = [[copy.copy(self.board[i][j]) for j in range(8)] for i in range(8)]
        for i in range(8):
            for j in range(8):
                if test_board.board[i][j] is not None:
                    test_board.board[i][j].board = test_board
        return test_board;
    
    def draw_board(self):
        if self.ui is None: return;
        #print("Drawing board")
        self.ui.draw_board(self.board, self.valid);
    
    def print_board(self):
        pprint(self.board)
        
    @staticmethod
    def other_color(color):
        return 'W' if color == 'B' else 'B'

        
class AI(object):
    
    @staticmethod
    def make_move(board, color, skill):
        mine = board.get_pieces(color);
        
        best_move = None;
        best_score = None;
        for piece in mine:
            moves = piece.get_valid_moves();
            for move in moves:
                test_board = board.copy_board();
                test_piece = test_board.board[piece.X][piece.Y];
                test_board.move(test_piece, move)
                if skill > 1:
                    AI_move = AI.make_move(test_board, Board.other_color(color), skill-1);
                    test_board.move(AI_move[0], AI_move[1]);
                score = AI.eval(test_board, color);
                if best_score is None or score > best_score:
                    best_score = score;
                    best_move = [piece, move];
        #print("best_score is: " + str(best_score))
        return best_move;
    
    @staticmethod
    def eval(board, color):
        mine = board.get_pieces(color);
        his = board.get_pieces(Board.other_color(color));
        score = 0;
        for piece in mine:
            #print(str(piece) + " " + str(len(piece.get_valid_moves())));
            score += len(piece.get_valid_moves());
            score += AI.value(piece);    
        for piece in his:
            score -= len(piece.get_valid_moves());
            score -= AI.value(piece);
        #board.print_board();
        #print(score);
        return score;
        
    @staticmethod
    def value(piece):
        if isinstance(piece, Pawn): return 100;
        if isinstance(piece, Bishop): return 350;
        if isinstance(piece, Knight): return 350;
        if isinstance(piece, Rook): return 500;
        if isinstance(piece, Queen): return 900;
        if isinstance(piece, King): return 10000000;
        print("error: unknown piece type: " + str(piece));
        return 0;
       
        
class Piece(object):
    def __init__(self, color, name, board, x, y):
        self.X = x;
        self.Y = y;
        self.board = board;
        self.color = color;
        self.name = name;
        self.moved = False;
        self.firstMove = False;
    def move(self,*args):
        if len(args) == 1:
            self.movepiece(args[0].X, args[0].Y)
        elif len(args) == 2:
            self.X = args[0];
            self.Y = args[1];
        self.firstMove = False if self.moved else True
        self.moved = True;
    @staticmethod
    def get_distance():
        return 8;
    @staticmethod
    def get_direction():
        return [];
    def get_valid_moves(self):
        moves = [];
        direction = self.get_direction();
        l = Point(self.X,self.Y);
        for i in direction:
            for j in range(1,self.get_distance()+1):
                p = i*j+l;
                if not self.board.on_board(p.X,p.Y): break;
                piece = self.board.board[p.X][p.Y];
                if piece is not None and piece.color == self.color: break;
                moves += [p];
                if piece is not None: break;
        return moves;
    def __repr__(self):
        return self.color+""+self.name

class Pawn(Piece):
    def get_distance(self):
        return 1 if self.moved else 2;
        
    def get_valid_moves(self):
        moves = [];
        dir = -1 if self.color == 'W' else 1
        i = Point(0,-dir)
        l = Point(self.X,self.Y);
        for j in range(1,self.get_distance()+1):
            p = i*j+l;
            if not self.board.on_board(p.X,p.Y): break;
            piece = self.board.board[p.X][p.Y];
            if piece is not None: break;
            moves += [p];
        sides = [Point(-1,-dir), Point(1,-dir)];
        for i in sides:
            p = i+l
            if not self.board.on_board(p.X,p.Y): continue;
            piece = self.board.board[p.X][p.Y];
            if piece is not None:
                if piece.color != self.color:
                    moves += [p];
            # else:
                # piece = self.board.board[p.X][p.Y - dir];
                # if piece is not None and piece.name == 'P' and piece.color != self.color and piece.firstMove == True:
                    # moves += [p];
        return moves;
        
class Bishop(Piece):
    @staticmethod
    def get_direction():
        return [Point(1,1),Point(1,-1),Point(-1,1),Point(-1,-1)]
class Knight(Piece):
    @staticmethod
    def get_distance():
        return 1;
    @staticmethod
    def get_direction():
        return [Point(1,2),Point(1,-2),Point(-1,2),Point(-1,-2), Point(2,1),Point(2,-1),Point(-2,1),Point(-2,-1)]
class Rook(Piece):
    @staticmethod
    def get_direction():
        return [Point(0,1),Point(0,-1),Point(-1,0),Point(1,0)]
class Queen(Piece):
    @staticmethod
    def get_direction():
        return Rook.get_direction() + Bishop.get_direction()
class King(Piece):
    @staticmethod
    def get_distance():
        return 1;
    @staticmethod
    def get_direction():
        return Queen.get_direction()

    

class ChessApp(App):
    def build(self):
        return UI()


if __name__ == '__main__':
    ChessApp().run()