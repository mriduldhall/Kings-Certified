from Board import Board
from TreeStorageFunctions import TreeStorageFunction
import random


class Minimax:
    def __init__(self, maximising_marker, minimising_marker, game_setup_arguments):
        self.maximising_marker = maximising_marker
        self.minimising_marker = minimising_marker
        self.game_setup_arguments = game_setup_arguments
        self.storage_function = TreeStorageFunction()
        self.current_line = 1
        self.current_depth = 1

    def best_move(self, state):
        self.storage_function.max_depth = sum([row.count(self.game_setup_arguments[2]) for row in state])
        self.storage_function.initialise_files()
        current_board = Board(*self.game_setup_arguments, self.deepcopy(state))
        scores = []
        for column in current_board.get_valid_moves():
            current_board.make_move(column, self.maximising_marker)
            score, line_number = self.minimax(current_board.grid, False, str(column), str(column), 1)
            scores.append((column, score))
            current_board.grid = self.deepcopy(state)
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
        current_board = Board(*self.game_setup_arguments, self.deepcopy(state))
        player_marker = self.maximising_marker if is_maximising else self.minimising_marker
        possible_states = []
        columns = []
        for column in current_board.get_valid_moves():
            current_board.make_move(column, player_marker)
            possible_states.append(current_board.grid)
            columns.append(column)
            current_board.grid = self.deepcopy(state)
        return zip(possible_states, columns)

    def evaluate(self, state):
        current_board = Board(*self.game_setup_arguments, state)
        victory_status = current_board.check_victory()
        if victory_status[0] is True or len(current_board.get_valid_moves()) == 0:
            if victory_status[1] == self.maximising_marker:
                return 1
            elif victory_status[1] == self.minimising_marker:
                return -1
            return 0
        return None

    @staticmethod
    def deepcopy(state):
        return [list(column) for column in state]

    def next_best_move(self, is_maximising):
        best_moves = []
        child_nodes = self.storage_function.get_child_nodes_v2(self.current_depth, self.current_line)
        child_scores = [int(node[1]) for node in child_nodes]
        best_score = max(child_scores) if is_maximising else min(child_scores)
        print(best_score)
        for node in child_nodes:
            if int(node[1]) == best_score:
                best_moves.append(node)
        move = int(random.choice(best_moves)[0])
        print(move)
        return move


    def follow_move(self, column):
        child_nodes = self.storage_function.get_child_nodes_v2(self.current_depth, self.current_line)
        for i in range(len(child_nodes)):
            if int(child_nodes[i][0]) == column:
                if not child_nodes[i][2]:
                    print("Not in tree.")
                    return 0
                self.current_depth += 1
                self.current_line = child_nodes[i][2]



if __name__ == '__main__':
    a = Board(rows=4, columns=5, empty=0, player_1=1, player_2=2, robot='R')
    # a.grid = [
    #     [0, 0, 0, 0, 0],
    #     [2, 0, 0, 1, 2],
    #     [1, 2, 1, 2, 1],
    #     [2, 2, 1, 2, 1]
    # ]

    a.grid = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [1, 2, 1, 1, 2]
    ]

    b = Minimax(1, 2, [4, 5, 0, 1, 2, "R"])
    moves = b.best_move(a.grid)
    print(moves)