class Board:
    def __init__(self, init_grid=None):
        self.empty_marker = "-"
        self.player_1_marker = "X"
        self.player_2_marker = "O"
        self.robot_marker = "R"
        self.player_number_to_marker = {
            1: self.player_1_marker,
            2: self.player_2_marker,
            "R": self.robot_marker
        }
        
        self.player_marker_to_number = {
            self.player_1_marker: "X",
            self.player_2_marker: "O",
            self.robot_marker: "R"
        }
        
        if not init_grid:
            self.grid = [[self.empty_marker for columns in range(3)] for rows in range(3)]
        else:
            self.grid = init_grid

    
    def make_move(self, place_coord, player_marker):
        row, column = place_coord
        self.grid[int(row)][int(column)] = player_marker
        
    
    def print_board(self, grid=None):
        if grid:
            grid = grid
        else:
            grid = self.grid
        print("")
        for row in range(len(self.grid)):
            print(grid[row])
    
    
    def get_valid_moves(self, state=True):
        if state:
            state = self.grid
        available_spaces = []
        for row in range(len(state)):
            for column in range(len(state[row])):
                if str(state[row][column]) == str(self.empty_marker):
                    available_spaces.append((str(row), str(column)))
        
        return available_spaces
    
        
    def check_victory(self):
        # check rows
        for row in self.grid:
            if row[0] == row[1] == row[2] != self.empty_marker:
                return True, self.player_marker_to_number[row[0]]

        # check columns
        for columns in range(len(self.grid)):
            column = [self.grid[0][columns], self.grid[1][columns], self.grid[2][columns]]
            if column[0] == column[1] == column[2] != self.empty_marker:
                return True, self.player_marker_to_number[column[0]]
        
        # check diagonals
        if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] != self.empty_marker:
            return True, self.player_marker_to_number[self.grid[0][0]]
        
        if self.grid[0][2] == self.grid[1][1] == self.grid[2][0] != self.empty_marker:
            return True, self.player_marker_to_number[self.grid[0][2]]

        return False, None
    
    
            
            
