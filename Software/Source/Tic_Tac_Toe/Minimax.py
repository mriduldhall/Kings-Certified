from Board import Board
from TreeStorageFunctions import TreeStorageFunction
from random import choice

class Minimax:
    def __init__(self, initial_state, maximising_marker, minimising_marker):
        self.initial_state = initial_state 
        self.maximising_marker = maximising_marker  # player who is to play next
        self.minimising_marker = minimising_marker  # opponent
        # self.game_setup_arguments = game_setup_arguments
        self.is_maximising = False
        self.storage_function = TreeStorageFunction()
        self.current_line = 1
        self.final_line = 9
        self.current_depth = 1

    @staticmethod
    def deepcopy(state):
        return [list(row) for row in state]

    def evaluate(self, state):
        current_board = Board(self.deepcopy(state))
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
        current_board = Board(self.deepcopy(state))
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
            scores.append(score)
            lines_used += 1
            
        line_number = str(int(line_number) - lines_used + 1)
        
        if is_maximising:
            line_number = self.storage_function.write_node(str(previous_move), str(max(scores)), depth, line_number)
            return max(scores), line_number
        
        else:
            line_number = self.storage_function.write_node(str(previous_move), str(min(scores)), depth, line_number)
            return min(scores), line_number

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


    def next_best_move(self, is_maximising):
        child_nodes = self.storage_function.get_layer(self.current_depth, self.current_line, self.final_line)
        best_moves = []
        child_scores = [int(node[1]) for node in child_nodes]
        best_score = max(child_scores) if is_maximising else min(child_scores)
        # print("Child nodes: ", child_nodes)
        # print("Child Scores:", child_scores)
        # print("Best score:", best_score)
        for node in child_nodes:
            if str(node[1]) == str(best_score):
                best_moves.append(node)
        # print("Best moves", best_moves)
        return best_moves
    
    def follow_move(self, move):
        # print("Depth b4:", self.current_depth)
        # print("Lines b4:", self.current_line, self.final_line)
        child_nodes = self.storage_function.get_layer(self.current_depth, self.current_line, self.final_line)
        # print("Child nodes from follow:", child_nodes)
        for count in range(len(child_nodes)-1):
            if move == child_nodes[count][0]:
                # print("Count:", count)
                self.current_depth += 1
                self.current_line = int(child_nodes[count][2])
                self.final_line = int(child_nodes[count+1][2])
               
        # print("Depth after:", self.current_depth)
        # print("Lines after:", self.current_line, self.final_line)
    
    
    
if __name__ == "__main__":
    a = Board()
    # a.grid = [
    #     ["X", "-", "O"],
    #     ["X", "-", "O"],
    #     ["-", "-", "X"]
    # ]
    
    b = Minimax(a.grid, "O", "X")
    # this means that first marker is the one whose choice will be taken?
    print(b.best_move(a.grid))
    
    # print(b.storage_function.get_layer(1, b.current_line, b.final_line))
    # print(b.next_best_move(True))