import board


class GoGame:
    
    def __init__(self):
        self.b = board.Board()
        
    def is_a_number(self, string):
        try:
            int(string)
            return True
        except ValueError:
            return False
    
    def alpha_to_column_number(self, alpha):
        order_in_alphabet = ord(alpha) - (ord('a') - 1)
        if ord(alpha) >= ord('i'):
            order_in_alphabet -= 1
        return order_in_alphabet
    
    def is_valid_coord(self, move_string):
        alpha = move_string[0].lower()
        if ord('a') <= ord(alpha) <= ord('t') and alpha != 'i':
            if self.is_a_number(move_string[1:]):
                return True
    
    def is_pass(self, move_string):
        move_string = move_string.lower()
        if move_string == "p" or move_string == "pass":
            return True
        else:
            return False
    
    def get_valid_move(self):
        valid_coord = False
        row, col = 0, 0
        pass_move = False
        while not valid_coord:
            move = input("Enter move: ")
            valid_coord = self.is_valid_coord(move)
            if not valid_coord:
                if self.is_pass(move):
                    valid_coord = True
                    pass_move = True
                else:
                    print("Invalid coordinate.")
            else:
                col = self.alpha_to_column_number(move[0].lower())
                row = int(move[1:])
        return board.Coord(row-1, col-1), pass_move
    
    def perform_legal_move(self):
        move_complete = False
        coordinate = board.Coord(1, 1)
        print("\nIt is " + self.b.turn + "'s turn.\n")
        while not move_complete:
            coordinate, pass_move = self.get_valid_move()
            legal, reason = self.b.is_legal_move(coordinate)
            if legal:
                self.b.make_move(coordinate)
                move_complete = True
            elif pass_move:
                self.b.pass_turn()
                move_complete = True
            else:
                print(reason)
        return coordinate
    
    def play(self):
        while self.b.g_over is not True:
            print(self.b.as_string())
            coord = self.perform_legal_move()

g = GoGame()
g.play()