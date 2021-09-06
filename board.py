class coord:
    def __init__(self, r, c):
        self.row = r
        self.column = c
        
        int_type = type(3)
        assert type(r) == int_type
        assert type(c) == int_type

class board:
    def __init__(self):
        
        self.grid = []
        for i in range(19):
            row = []
            for j in range(19):
                row += [None]
            self.grid += [row]
        
        self.turn = "b"
        self.winner = ""
        self.g_over = False
        
        self.display_chars = {
            None: ".",
            "b": "X",
            "w": "O" }

    """Returns the value at the intersection on the grid specificied by the given coordinate"""
    def get_contents(self, coord):
        r = coord.row
        c = coord.column
        return self.grid[r][c]
    
    """Sets the value at the intersection at the given coordinate to the given value"""
    def set_contents(self, coord, value):
        r = coord.row
        c = coord.column
        self.grid[r][c] = value
        
    """If a number has one digit, inserts a space in front of it"""
    def double_digit_fill_left(self, number)->str:
        if (int(number) >= 10):
            return str(number)
        elif (int(number) >= 100):
            raise RuntimeError()
        else:
            return " " + str(number)
    
    """If a number has one digit, appends a space after it"""
    def double_digit_fill_right(self, number)->str:
        if (int(number) >= 10):
            return str(number)
        elif (int(number) >= 100):
            raise RuntimeError()
        else:
            return str(number) + " "
    
    
    """Outputs an ASCII representation of the grid to the console"""
    def print_grid(self):
        output = "   A B C D E F G H J K L M N O P Q R S T   \n"
        for i in range(19, 0, -1):
            output += self.double_digit_fill_right(i) + " "
            for c in self.grid[i-1]:
                output += self.display_chars[c] + " "
            output += self.double_digit_fill_left(i) + "\n"
        output += "   A B C D E F G H J K L M N O P Q R S T   \n"
        print(output)
    
    """Removes duplicate entries from a list"""
    def remove_duplicates(self, lst):
        unique_lst = []
        for i in lst:
            if (not (i in unique_lst)):
                unique_lst += [i]
        return unique_lst
    
    """Returns the character for the other player"""
    def other_player(self, player):
        if (player == "b"):
            return "w"
        else:
            return "b"

    """Returns true if a given move is valid; otherwise, returns a string explaining why it is invalid"""
    def is_valid_move(self, coord):
        if ((1 <= coord.row <= 19) and (1 <= coord.row <= 19)):
            if (self.get_contents(coord) == None):
                return True
            else:
                return "Stones cannot be placed on other stones"
        else:
            return "Coords must be within the grid"

    """Returns the coords of the surrounding points of the given point in a list of four lists"""
    def get_neighbours(self, crd):
        r = crd.row
        c = crd.column
        
        neighbours = [coord(r-1, c),
                     coord(r, c-1),
                     coord(r+1, c),
                     coord(r, c+1)]
        valid_neighbours = []
        for i in range(4):
            if ((0 <= neighbours[i].row <= 18) and
                     (0 <= neighbours[i].row <= 18)):
                valid_neighbours += [neighbours[i]]
        return valid_neighbours
    
    """Returns a list of coordinates of stones with strict connection to the given stone"""
    def get_chain(self, coord):
        chain = [coord]
        current = coord
        to_check = []
        colour = self.get_contents(coord)
        
        done = False
        while (not done):
            neighbours = self.get_neighbours(current)
            for i in neighbours:
                print(self.get_contents(i))
                if (self.get_contents(i) == colour):
                    if (not (i in chain)):
                        to_check += [i]
                        chain += [i]
            if (to_check == []):
                done = True
            else:
                current = to_check[0]
                del to_check[0]
        return chain
    
    """Returns the total liberties of the given list of stones"""
    def get_liberties(self, coord_list):
        empty_point_list = []
        colour = self.get_contents(coord_list[0])
        for i in coord_list:
            
            if (self.get_contents(i) != colour):
                raise RuntimeError()
                
            neighbours = self.get_neighbours(i)
            for j in neighbours:
                if (self.get_contents(j) == None):
                    empty_point_list += [j]
        empty_point_list = self.remove_duplicates(empty_point_list)
        return len(empty_point_list)
    
    """Removes the given list of stones from the board"""
    def capture(self, chain):
        for stone in chain:
            self.set_contents(stone, None)
    
    """Adds a stone to the board at the given coords, and makes any necessary captures"""
    def place_stone(self, coord, colour):
        self.set_contents(coord, colour)
        neighbours = self.get_neighbours(coord)
        for i in neighbours:
            if (self.get_contents(i) != None):
                chain = self.get_chain(i)
                print(chain)
                libs = self.get_liberties(chain)
                if (libs == 0):
                    self.capture(chain)
    
    """Passes play onto the next player"""
    def next_turn(self):
        self.turn = self.other_player(self.turn)
        
    """Enacts the given valid move and passes play to the next player"""
    def make_move(self, move_coord):
        self.place_stone(move_coord, self.turn)
        self.next_turn()
    
    """Passes play onto the next player"""
    def pass_turn(self):
        self.next_turn()

