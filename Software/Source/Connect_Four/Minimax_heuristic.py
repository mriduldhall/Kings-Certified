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
            if score is not None:
                scores.append(score)
                lines_used += 1
                if (is_maximising and score == float('inf')) or (not is_maximising and score == float('-inf')):
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

    # def evaluate(self, state):
    #     current_board = Board(*self.game_setup_arguments, state)
    #     victory_status = current_board.check_victory()
    #     if victory_status[0] is True or len(current_board.get_valid_moves()) == 0:
    #         if victory_status[1] == self.maximising_marker:
    #             return 1
    #         elif victory_status[1] == self.minimising_marker:
    #             return -1
    #         return 0
    #     return None

    @staticmethod
    def deepcopy(state):
        return [list(column) for column in state]

    def next_best_move(self, is_maximising):
        best_moves = []
        child_nodes = self.storage_function.get_child_nodes_v2(self.current_depth, self.current_line)
        child_scores = [int(node[1]) for node in child_nodes]
        best_score = max(child_scores) if is_maximising else min(child_scores)
        for node in child_nodes:
            if int(node[1]) == best_score:
                best_moves.append(node)
        move = int(random.choice(best_moves)[0])
        return move


    def follow_move(self, column):
        child_nodes = self.storage_function.get_child_nodes_v2(self.current_depth, self.current_line)
        for i in range(len(child_nodes)):
            if int(child_nodes[i][0]) == column:
                if not child_nodes[i][2]:
                    print("Alpha beta error")
                    return 0
                self.current_depth += 1
                self.current_line = child_nodes[i][2]

    # Returns the number of streaks of length 2, 3, and 4 for the given player
    @staticmethod
    def sumOfFirstFourBits(x):
        return (0 if (x & 8) == 0 else 1) + (0 if (x & 4) == 0 else 1) + (0 if (x & 2) == 0 else 1) + (
            0 if (x & 1) == 0 else 1)

    # This will calculate the byte-index into the cumulative board
    @staticmethod
    def ix(row, col, dir):
        return row * 7 * 4 + col * 4 + dir

    @staticmethod
    def appendToStreak(curStreak, currentSpotState):
        if currentSpotState == -1:
            return 0
        elif curStreak == 0:
            if currentSpotState == 0:
                return 2
            else:
                return 3
        else:
            return (curStreak >> 4 << 4) | ((curStreak & 15) << 1) | currentSpotState

    def evaluate(self, connect4State) -> float:
        movableColumns = [0] * 7
        totalNumberOfFreeSpots = 0
        cumulativeBoardPlayer1 = [0] * 6 * 7 * 4
        cumulativeBoardPlayer2 = [0] * 6 * 7 * 4
        player1Score = 0
        player2Score = 0
        for row in range(6):
            for col in range(7):
                streakVectorPlayer1 = [
                    0 if col == 0 else
                    cumulativeBoardPlayer1[
                        self.ix(row, col - 1, 0)]
                    ,
                    0 if (row == 0 or col == 0) else cumulativeBoardPlayer1[
                        self.ix(row - 1, col - 1, 1)]
                    ,
                    0 if row == 0 else
                    cumulativeBoardPlayer1[
                        self.ix(row - 1, col, 2)]
                    ,
                    0 if (row == 0 or col == 6) else cumulativeBoardPlayer1[
                        self.ix(row - 1, col + 1, 3)]
                ]
                streakVectorPlayer2 = [
                    0 if col == 0 else
                    cumulativeBoardPlayer2[self.ix(row, col - 1, 0)]
                    ,
                    0 if (row == 0 or col == 0) else
                    cumulativeBoardPlayer2[self.ix(row - 1, col - 1, 1)]
                    ,
                    0 if row == 0 else
                    cumulativeBoardPlayer2[self.ix(row - 1, col, 2)]
                    ,
                    0 if (row == 0 or col == 6) else
                    cumulativeBoardPlayer2[self.ix(row - 1, col + 1, 3)]
                ]
                currentSpotState = connect4State[row][col]
                currentSpotState = -1 if currentSpotState == 2 else currentSpotState

                if currentSpotState == 0:
                    totalNumberOfFreeSpots += 1
                    movableColumns[col] = 1

                newStreakVectorPlayer1 = [
                    self.appendToStreak(streakVectorPlayer1[0], currentSpotState),
                    self.appendToStreak(streakVectorPlayer1[1], currentSpotState),
                    self.appendToStreak(streakVectorPlayer1[2], currentSpotState),
                    self.appendToStreak(streakVectorPlayer1[3], currentSpotState)
                ]
                newStreakVectorPlayer2 = [
                    self.appendToStreak(streakVectorPlayer2[0], -currentSpotState),
                    self.appendToStreak(streakVectorPlayer2[1], -currentSpotState),
                    self.appendToStreak(streakVectorPlayer2[2], -currentSpotState),
                    self.appendToStreak(streakVectorPlayer2[3], -currentSpotState)
                ]

                for i in range(4):
                    if (newStreakVectorPlayer1[i] >= 16):
                        player1Score += self.sumOfFirstFourBits(
                            newStreakVectorPlayer1[i]
                        )
                for i in range(4):
                    if (newStreakVectorPlayer2[i] >= 16):
                        player2Score += self.sumOfFirstFourBits(
                            newStreakVectorPlayer2[i]
                        )
                for i in range(4):
                    cumulativeBoardPlayer1[self.ix(row, col, i)] = newStreakVectorPlayer1[i]
                    cumulativeBoardPlayer2[self.ix(row, col, i)] = newStreakVectorPlayer2[i]


                if (31 in newStreakVectorPlayer1):
                    # Is End State
                    if self.maximising_marker == 1:
                        return float('inf')
                    else:
                        return float('')
                    # return {
                    #     'player1Score': float('inf'),
                    #     'player2Score': float('-inf'),
                    #     'winner': 'player1'  # For debugging
                    # }
                if (31 in newStreakVectorPlayer2):
                    # Is End State
                    if self.maximising_marker == 2:
                        return float('inf')
                    else:
                        return float('-inf')
                    # return {
                    #     'player1Score': float('-inf'),
                    #     'player2Score': float('inf'),
                    #     'winner': 'player2'  # For debugging
                    # }

        if totalNumberOfFreeSpots == 0:
            if self.maximising_marker == 1:
                return float(player1Score - player2Score)
            else:
                return float(player2Score - player1Score)
            # return {
            #     'player1Score': player1Score,
            #     'player2Score': player2Score,
            #     'winner': 'tie'  # For debugging
            # }
        # return {
        #     'player1Score': player1Score,
        #     'player2Score': player2Score,
        #     'winner': 'none'  # For debugging
        # }
        if self.maximising_marker == 1:
            return float(player1Score - player2Score)
        else:
            return float(player2Score - player1Score)


if __name__ == '__main__':
    a = Board(rows=6, columns=7, empty=0, player_1=1, player_2=2, robot=2)
    a.grid = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
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
