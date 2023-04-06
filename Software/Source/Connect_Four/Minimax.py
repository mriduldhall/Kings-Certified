from Board import Board
from TreeStorageFunctions import TreeStorageFunction
from copy import deepcopy


class Minimax:
    def __init__(self, maximising_marker, minimising_marker, game_setup_arguments):
        self.maximising_marker = maximising_marker
        self.minimising_marker = minimising_marker
        self.game_setup_arguments = game_setup_arguments
        self.storage_function = TreeStorageFunction()

    def best_move(self, state):
        self.storage_function.max_depth = sum([row.count(self.game_setup_arguments[2]) for row in state])
        self.storage_function.initialise_files()
        current_board = Board(*self.game_setup_arguments, deepcopy(state))
        scores = []
        for column in current_board.get_valid_moves():
            current_board.make_move(column, self.maximising_marker)
            score, line_number = self.minimax(current_board.grid, False, str(column), str(column), 1)
            scores.append((column, score))
            current_board.grid = deepcopy(state)
        self.storage_function.close_files()
        return scores

    def minimax(self, state, is_maximising, previous_move, previous_moves, depth):
        if (score := self.evaluate(state)) is not None:
            line_number = self.storage_function.write_node(str(previous_move), str(score), depth)
            return score, line_number
        scores = []
        lines_used = 0
        line_number = 1
        for possible_state, column in self.possible_new_states(state, is_maximising):
            score, line_number = self.minimax(possible_state, not is_maximising, column, previous_moves + str(column), depth + 1)
            scores.append(score)
            lines_used += 1
        line_number = str(int(line_number) - lines_used + 1)
        if is_maximising:
            line_number = self.storage_function.write_node(str(previous_move), str(max(scores)), depth, line_number)
            return max(scores), line_number
        else:
            line_number = self.storage_function.write_node(str(previous_move), str(min(scores)), depth, line_number)
            return min(scores), line_number

    def possible_new_states(self, state, is_maximising):
        current_board = Board(*self.game_setup_arguments, deepcopy(state))
        player_marker = self.maximising_marker if is_maximising else self.minimising_marker
        possible_states = []
        columns = []
        for column in current_board.get_valid_moves():
            current_board.make_move(column, player_marker)
            possible_states.append(current_board.grid)
            columns.append(column)
            current_board.grid = deepcopy(state)
        return zip(possible_states, columns)

    def evaluate(self, state):
        current_board = Board(*self.game_setup_arguments, state)
        if current_board.check_victory()[0] is True or len(current_board.get_valid_moves()) == 0:
            if current_board.check_victory()[1] == self.maximising_marker:
                return 1
            elif current_board.check_victory()[1] == self.minimising_marker:
                return -1
            return 0
        return None

    def next_best_move(self, is_maximising):
        return 0

    def follow_move(self, column):
        pass


if __name__ == '__main__':
    a = Board(rows=6, columns=7, empty=0, player_1=1, player_2=2, robot='R')
    a.grid = [
        [0, 0, 0, 0, 0, 0, 0],
        [2, 0, 0, 1, 2, 1, 1],
        [1, 2, 1, 2, 1, 2, 2],
        [2, 2, 1, 2, 1, 2, 1],
        [1, 1, 2, 1, 1, 2, 2],
        [1, 2, 1, 2, 2, 1, 1],
    ]
    # a.grid = [
    #     [2, 1, 2, 2, 0, 0, 0],
    #     [2, 2, 1, 1, 2, 1, 1],
    #     [1, 2, 1, 2, 1, 2, 2],
    #     [2, 2, 1, 2, 1, 2, 1],
    #     [1, 1, 2, 1, 1, 2, 2],
    #     [1, 2, 1, 2, 2, 1, 1],
    # ]
    # a.grid = [
    #     [2, 1, 0, 2, 2, 2, 0],
    #     [2, 2, 1, 1, 2, 1, 1],
    #     [1, 2, 1, 2, 1, 2, 1],
    #     [2, 2, 1, 2, 1, 2, 1],
    #     [1, 1, 2, 1, 1, 2, 2],
    #     [1, 2, 1, 2, 2, 1, 1],
    # ]

    b = Minimax(1, 2, [6, 7, 0, 1, 2, "R"])
    moves = b.best_move(a.grid)
    print(moves)
