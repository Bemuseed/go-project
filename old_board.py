class board:
    def __init__(self):
        self.grid = []
        self.stone_list = []
        for i in range(19):
            row = []
            srow = []
            for j in range(19):
                row += [None]
                srow += [-1]
            self.grid += [row]
            self.stone_list += [srow]
        self.group_list = []
        
        self.turn = "b"
        self.winner = ""
        self.g_over = False
        
        self.display_chars = {
            None: ".",
            "b": "X",
            "w": "O" }

    
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
    
    """Returns the group number of the given point on the grid"""
    def get_point_group(self, r, c):
        return self.stone_list[r][c]

    """Returns true if a given move is valid; otherwise, returns a string explaining why it is invalid"""
    def is_valid_move(self, row, col):
        if ((1 <= row <= 19) and (1 <= col <= 19)):
            if (self.grid[row-1][col-1] == None):
                return True
            else:
                return "Stones cannot be placed on other stones"
        else:
            return "Coords must be within the grid"

    """Returns the coords of the surrounding points of the given point in a list of four lists"""
    def get_neighbours(self, row, column):
        neighbours = [[row-1,column],
                     [row,column-1],
                     [row+1,column],
                     [row,column+1]]
        valid_neighbours = []
        for i in range(4):
            if ((0 <= neighbours[i][0] <= 18) and
                     (0 <= neighbours[i][1] <= 18)):
                valid_neighbours += [neighbours[i]]
        return valid_neighbours
    
    """Returns the total liberties of the given group in the group list"""
    def get_liberties(self, coord_list):
        empty_point_list = []
        for i in coord_list:
            neighbours = self.get_neighbours(i[0], i[1])
            for j in neighbours:
                if (self.grid[j[0]][j[1]] == None):
                    empty_point_list += [j]
        empty_point_list = self.remove_duplicates(empty_point_list)
        return len(empty_point_list)
    
    """Returns the total liberties of the given group in the group list"""
    def get_group_liberties(self, g_num):
        group = self.group_list[g_num]
        return self.get_liberties(group)
        
    """Updates the group numbers in the stone list so they match the coords in the group list"""
    def refresh_stone_list(self):
        for g in range(len(self.group_list)):
            for c in self.group_list[g]:
                self.stone_list[c[0]][c[1]] = g
    
    """Adds the stone at the given coords to the given group in the group list, and creates a stone list entry"""
    def add_to_group(self, r, c, g_num):
        self.group_list[g_num] += [[r, c]]
        self.stone_list[r][c] = g_num
        
    """Creates a new stone group, with a single stone at the given coords, and creates a stone list entry """
    def new_group(self, r, c):
        self.group_list += [[[r,c]]]
        self.stone_list[r][c] = len(self.group_list) - 1
    
    """Removes a group from the group list, and its members from the stone list and the grid"""
    def capture_group(self, g_num):
        for i in self.group_list[g_num]:
            self.stone_list[i[0]][i[1]] = -1
            self.grid[i[0]][i[1]] = None
        del self.group_list[g_num]
    
    """Combines two or more groups into one"""
    def converge_groups(self, g_nums):
        stone_coords = []
        g_nums.sort(reverse=True)
        for i in g_nums:
            for j in self.group_list[i]:
                stone_coords += [j]
            del self.group_list[i]
        self.group_list += [stone_coords]
        self.refresh_stone_list()
        
    """Updates the state of the grid after a stone has been placed"""
    def grid_refresh(self):
        captured_groups = []
        all_groups_checked = False
        current_index = 0
        while (not all_groups_checked):
            libs = self.get_group_liberties(current_index)
            if (libs == 0):
                self.capture_group(current_index)
            if (current_index == len(self.group_list) - 1):
                all_groups_checked = True
            current_index += 1
    
    """Updates the stone and group lists after a stone has been placed"""
    def update_groups(self, r, c):
        neighbours = self.get_neighbours(r, c)
        updated_groups = []
        groups_to_add = []
        for p in neighbours:
            x = p[0]
            y = p[1]
            value = self.grid[x][y]
            if (not (value == None)):
                group_num = self.get_point_group(x, y)
                if (not (group_num in updated_groups)):
                    if (value == self.turn):
                        updated_groups += [group_num]
                        groups_to_add += [group_num]
        if (updated_groups == []):
            self.new_group(r, c)
        else:
            self.add_to_group(r, c, groups_to_add[0])
            if len(groups_to_add) > 1:
                self.converge_groups(groups_to_add)  
    
    """Passes play onto the next player"""
    def next_turn(self):
        self.turn = self.other_player(self.turn)
        
    """Places a stone on the board based on a VALID pair of coords, refreshes group list and board and passes turn to next player"""
    def place_stone(self, move_row, move_column):
        self.grid[move_row][move_column] = self.turn
        self.update_groups(move_row, move_column)
        self.grid_refresh()
        print(self.group_list)
        self.next_turn()
    
    """Passes play onto the next player"""
    def pass_turn(self):
        self.next_turn()

