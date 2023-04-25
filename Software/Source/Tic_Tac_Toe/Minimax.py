from Board import Board
from TreeStorageFunctions import TreeStorageFunction


class Minimax:
    def __init__(self, initial_state, maximising_marker, minimising_marker):
        self.initial_state = initial_state 
        self.maximising_marker = maximising_marker  # player who is to play next
        self.minimising_marker = minimising_marker  # opponent
        # self.game_setup_arguments = game_setup_arguments
        self.is_maximising = False
        self.storage_function = TreeStorageFunction()

    @staticmethod
    def deepcopy(state):
        return [list(row) for row in state]

    def evaluate(self, state):
        current_board = Board(state)
        victory_status = current_board.check_victory()
        # print(victory_status)
        if victory_status[0] is True or len(current_board.get_valid_moves()) == 0:
            if victory_status[1] == self.maximising_marker:
                return 1
            elif victory_status[1] == self.minimising_marker:
                return -1
            return 0 
        return None

    def possible_new_states(self, state, is_maximising):
        current_board = Board(state)
        player_marker = self.maximising_marker if is_maximising else self.minimising_marker
        possible_states = []
        positions = []
        for position in current_board.get_valid_moves():
            current_board.make_move(position, player_marker)
            possible_states.append(current_board.grid)
            positions.append(position)
            current_board.grid = self.deepcopy(state)
        
        return zip(possible_states, positions)
    
    def minimax(self, state, is_maximising, previous_move, previous_moves, depth):
        score = self.evaluate(state)
        if score is not None:
            line_number = self.storage_function.write_node(str(previous_move), str(score), depth)
            return score, line_number

        scores = []
        lines_used = 0
        line_number = 1

        for possible_state, position in self.possible_new_states(state, is_maximising):
            score, line_number = self.minimax(possible_state, not is_maximising, position, previous_moves + str(position), depth + 1)
            if score is not None:
                scores.append(score)
                lines_used += 1
                if (is_maximising and score == 1) or (not is_maximising and score == -1):
                    break

        line_number = str(int(line_number) - lines_used + 1)
        
        if is_maximising:
            if scores:
                line_number = self.storage_function.write_node(str(previous_move), str(max(scores)), depth, line_number)
                return max(scores), line_number
            return None, None

        else:
            if scores:
                line_number = self.storage_function.write_node(str(previous_move), str(min(scores)), depth, line_number)
                return min(scores), line_number
            return None, None

    def best_move(self, state):
        self.storage_function.max_depth = sum([row.count("-") for row in state])
        self.storage_function.initialise_files()
        current_board = Board(self.deepcopy(state))
        scores = []

        for position in current_board.get_valid_moves():
            current_board.make_move(position, self.maximising_marker)
            score, line_number = self.minimax(current_board.grid, self.is_maximising, str(position), str(position), 1)
            scores.append([position, score])
            current_board.grid = self.deepcopy(state)

        self.storage_function.close_files()
        
        return scores

    def next_logical_move(self, state, is_maximising):
        moves = self.best_move(state)
        best_pos = moves[0]
        worst_pos = moves[0]
        # print(f"Moves: {moves}")
        # print(f"Best position: {best_pos}")
        # print(f"Worst position: {worst_pos}")
        
        # print(best_pos, worst_pos)
        for move in moves:
            # print(f"Move:{move}")
            if int(move[1]) > int(best_pos[1]):
                best_pos = move
            elif int(move[1]) < int(worst_pos[1]):
                worst_pos = move
        if is_maximising:
            return best_pos[0]
        else:
            return worst_pos[0]


if __name__ == "__main__":
    a = Board()
    
    a.grid = [
        ["X", "-", "O"],
        ["X", "-", "O"],
        ["-", "-", "X"]
    ]
    
    b = Minimax(a.grid, "X", "O")
    # this means that first marker is the one whose choice will be taken?
    
    # print(b.evaluate(a.grid))
    # print(b.minimax(a.grid, True))
    # print(b.best_move(a.grid))
    a.grid = [
        ["X", "-", "-"],
        ["-", "O", "-"],
        ["X", "-", "-"]
    ]
    # for grid in b.possible_new_states(a.grid, True):
    #     a.print_board(grid)
        
    print(b.next_logical_move(a.grid, False))
    # the boolean here for is_maximising is used in conjunction with the initialising of minimax and if this is true then the first item entered into the
