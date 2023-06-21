from Board import Board
from TreeStorageFunctions import TreeStorageFunction
import random
import cProfile

class Minimax:
    def __init__(self, maximising_marker, minimising_marker, game_setup_arguments, player_begin):
        self.maximising_marker = maximising_marker
        self.minimising_marker = minimising_marker
        self.game_setup_arguments = game_setup_arguments
        self.storage_function = TreeStorageFunction(player_begin)
        self.current_line = 1
        self.last_line = 0
        self.current_depth = 1
        self.files_line_count = []
        self.player_begin = player_begin #when generating tree, this is manually updated (changed bt True to False)

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
        directory_addon = "Player1" if self.player_begin else "Player2"
        directory_name = self.storage_function.directory_name + directory_addon
        with open((directory_name + "/0.txt"), 'w') as file:
            file.write(str(self.storage_function.files_line_count))
        return scores

    def minimax(self, state, is_maximising, previous_move, previous_moves, depth):
        if (score := self.evaluate(state)) is not None:
            line_number = self.storage_function.write_node(str(previous_move), str(score), depth)
            return score, line_number
        scores = []
        lines_used = 0
        line_number = 1
        for possible_state, column in self.possible_new_states(state, is_maximising):
            score, line_number = self.minimax(possible_state, not is_maximising, column, previous_moves + str(column),
                                              depth + 1)
            if self.player_begin:
                if depth%2 != 0:
                    if score is not None:
                        scores.append(score)
                        lines_used += 1
                        if (is_maximising and score == 1) or (not is_maximising and score == -1):
                            break
                else:
                    scores.append(score)
                    lines_used += 1
            elif not self.player_begin:
                if depth%2 == 0:
                    if score is not None:
                        scores.append(score)
                        lines_used += 1
                        if (is_maximising and score == 1) or (not is_maximising and score == -1):
                            break
                else:
                    scores.append(score)
                    lines_used += 1
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
        if self.current_depth == 1:
            self.last_line = int(self.files_line_count[0]) + 1
        child_nodes = self.storage_function.get_child_nodes(self.current_depth, self.current_line, self.last_line)
        best_moves = []
        child_scores = [int(node[1]) for node in child_nodes]
        best_score = max(child_scores) if is_maximising else min(child_scores)
        for node in child_nodes:
            if str(node[1]) == str(best_score):
                best_moves.append(node)
        move = int(random.choice(best_moves)[0])
        return move

    
    def follow_move(self, column):
        if self.current_depth == 1:
            self.last_line = int(self.files_line_count[0]) + 1
        child_nodes = self.storage_function.get_child_nodes(self.current_depth, self.current_line, self.last_line)
        for i in range(len(child_nodes)):
            if int(child_nodes[i][0]) == column:
                if not child_nodes[i][2]:
                    return 0
                if (self.current_line + i) == int(self.files_line_count[self.current_depth-1]):
                    self.last_line = int(self.files_line_count[self.current_depth]) + 1
                else:
                    self.last_line = self.storage_function.get_next_linevalue(self.current_depth, self.current_line + i, int(self.files_line_count[self.current_depth-1]))
                    if not self.last_line:
                        self.last_line = int(self.files_line_count[self.current_depth]) + 1
                self.current_depth += 1
                self.current_line = int(child_nodes[i][2])


    def update_file_line_count(self):
        directory_addon = "Player1" if self.player_begin else "Player2"
        directory_name = self.storage_function.directory_name + directory_addon
        with open((directory_name + "/0.txt"), 'r') as file:
            files_line_count = file.read()
            files_line_count = list(map(str.strip, files_line_count.strip('][').replace('"', '').split(',')))
            self.files_line_count = files_line_count

if __name__ == '__main__':
    a = Board(rows=4, columns=5, empty=0, player_1=1, player_2=2, robot='R')
    # a.grid = [
    #     [0, 0, 0, 0, 0],
    #     [2, 0, 0, 1, 2],
    #     [1, 2, 0, 2, 1],
    #     [2, 2, 1, 2, 1]
    # ]

    a.grid = [
        [2, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [2, 0, 0, 0, 0],
        [1, 0, 0, 0, 0]
    ]

    b = Minimax(1, 2, [4, 5, 0, 1, 2, "R"], True)
    # moves = b.best_move(a.grid)
    cProfile.run('b.best_move(a.grid)')
    # print(moves)
