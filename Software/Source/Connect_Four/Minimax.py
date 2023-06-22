from Board import Board
from random import choice
from time import process_time as time


class Minimax:
    def __init__(self, maximising_marker, minimising_marker, game_setup_arguments, max_depth=6):
        self.maximising_marker = maximising_marker
        self.minimising_marker = minimising_marker
        self.game_setup_arguments = game_setup_arguments
        self.max_depth = max_depth

    def best_move(self, state, is_maximising):
        current_board = Board(*self.game_setup_arguments, self.deepcopy(state))
        scores = []
        for column in current_board.get_valid_moves():
            current_board.make_move(column, self.maximising_marker)
            score = self.minimax(current_board.grid, not is_maximising, 1)
            scores.append((column, score))
            current_board.grid = self.deepcopy(state)
        return scores

    def minimax(self, state, is_maximising, depth):
        score = self.evaluate(state)
        if (depth >= self.max_depth) or (score == float('inf')) or (score == float('-inf')):
            return score
        scores = []
        lines_used = 0
        for possible_state, column in self.possible_new_states(state, is_maximising):
            score = self.minimax(possible_state, not is_maximising, depth + 1)
            if score is not None:
                scores.append(score)
                lines_used += 1
                if (is_maximising and score == float('inf')) or (not is_maximising and score == float('-inf')):
                    break
        if is_maximising:
            if scores:
                return max(scores)
            return None
        else:
            if scores:
                return min(scores)
            return None

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

    @staticmethod
    def deepcopy(state):
        return [list(column) for column in state]

    @staticmethod
    def sum_of_first_four_bits(x):
        return (
            0 if (x & 8) == 0 else 1
        ) + (
            0 if (x & 4) == 0 else 1
        ) + (
            0 if (x & 2) == 0 else 1
        ) + (
            0 if (x & 1) == 0 else 1
        )

    @staticmethod
    def ix(row, col, dir):
        return row * 7 * 4 + col * 4 + dir

    @staticmethod
    def append_to_streak(current_streak, current_spot_state):
        if current_spot_state == -1:
            return 0
        elif current_streak == 0:
            if current_spot_state == 0:
                return 2
            return 3
        return (current_streak >> 4 << 4) | ((current_streak & 15) << 1) | current_spot_state

    def evaluate(self, connect_four_state: list[list[int]]) -> float:
        movable_columns = [0] * 7
        total_number_of_free_spots = 0
        cumulative_board_player_one = [0] * 6 * 7 * 4
        cumulative_board_player_two = [0] * 6 * 7 * 4
        player_one_score = 0
        player_two_score = 0
        for row in range(6):
            for col in range(7):
                streak_vector_player_one = [
                    0 if col == 0 else
                    cumulative_board_player_one[
                        self.ix(row, col - 1, 0)
                    ],
                    0 if (row == 0 or col == 0) else
                    cumulative_board_player_one[
                        self.ix(row - 1, col - 1, 1)
                    ],
                    0 if row == 0 else
                    cumulative_board_player_one[
                        self.ix(row - 1, col, 2)
                    ],
                    0 if (row == 0 or col == 6) else
                    cumulative_board_player_one[
                        self.ix(row - 1, col + 1, 3)
                    ]
                ]
                streak_vector_player_two = [
                    0 if col == 0 else
                    cumulative_board_player_two[
                        self.ix(row, col - 1, 0)
                    ],
                    0 if (row == 0 or col == 0) else
                    cumulative_board_player_two[
                        self.ix(row - 1, col - 1, 1)
                    ],
                    0 if row == 0 else
                    cumulative_board_player_two[
                        self.ix(row - 1, col, 2)
                    ],
                    0 if (row == 0 or col == 6) else
                    cumulative_board_player_two[
                        self.ix(row - 1, col + 1, 3)
                    ]
                ]
                current_spot_state = connect_four_state[row][col]
                current_spot_state = -1 if current_spot_state == 2 else current_spot_state

                if current_spot_state == 0:
                    total_number_of_free_spots += 1
                    movable_columns[col] = 1

                new_streak_vector_player_one = [
                    self.append_to_streak(streak_vector_player_one[0], current_spot_state),
                    self.append_to_streak(streak_vector_player_one[1], current_spot_state),
                    self.append_to_streak(streak_vector_player_one[2], current_spot_state),
                    self.append_to_streak(streak_vector_player_one[3], current_spot_state)
                ]
                new_streak_vector_player_two = [
                    self.append_to_streak(streak_vector_player_two[0], -current_spot_state),
                    self.append_to_streak(streak_vector_player_two[1], -current_spot_state),
                    self.append_to_streak(streak_vector_player_two[2], -current_spot_state),
                    self.append_to_streak(streak_vector_player_two[3], -current_spot_state)
                ]

                for i in range(4):
                    if new_streak_vector_player_one[i] >= 16:
                        player_one_score += self.sum_of_first_four_bits(
                            new_streak_vector_player_one[i]
                        )
                    if new_streak_vector_player_two[i] >= 16:
                        player_two_score += self.sum_of_first_four_bits(
                            new_streak_vector_player_two[i]
                        )
                for i in range(4):
                    cumulative_board_player_one[self.ix(row, col, i)] = new_streak_vector_player_one[i]
                    cumulative_board_player_two[self.ix(row, col, i)] = new_streak_vector_player_two[i]

                if 31 in new_streak_vector_player_one:
                    return float('inf') if self.maximising_marker == 1 else float('-inf')
                if 31 in new_streak_vector_player_two:
                    return float('inf') if self.maximising_marker == 2 else float('-inf')

        if total_number_of_free_spots == 0:
            if self.maximising_marker == 1:
                return float(player_one_score - player_two_score)
            return float(player_two_score - player_one_score)
        if self.maximising_marker == 1:
            return float(player_one_score - player_two_score)
        return float(player_two_score - player_one_score)

    def convert_state(self, state):
        state = self.deepcopy(state)
        for column_index in range(len(state)):
            for row_index in range(len(state[column_index])):
                if state[column_index][row_index] == "R":
                    state[column_index][row_index] = 2
        return state

    def next_best_move(self, state, is_maximising=True, update_depth=True):
        state = self.convert_state(state)
        start_time = time()
        moves = self.best_move(state, is_maximising)
        if update_depth:
            end_time = time()
            duration = end_time - start_time
            print("DURATION", duration)
            if duration < 7:
                self.max_depth += 2
            elif duration < 15:
                self.max_depth += 1
            print("DEPTH", self.max_depth)
        columns, scores = zip(*moves)
        best_score = max(scores)
        if scores.count(best_score) > 1:
            best_score_index = []
            for index in range(len(scores)):
                if scores[index] == best_score:
                    best_score_index.append(index)
        else:
            best_score_index = [scores.index(best_score)]
        best_columns = []
        for index in best_score_index:
            best_columns.append(columns[index])
        best_move = choice(best_columns)
        return best_move


if __name__ == '__main__':
    a = Board(rows=6, columns=7, empty=0, player_1=1, player_2=2, robot=2)
    # a.grid = [
    #     [0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0],
    # ]
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

    b = Minimax(1, 2, [6, 7, 0, 1, 2, "R"], 6)
    best, info = b.next_best_move(a.grid)
    print(best)
