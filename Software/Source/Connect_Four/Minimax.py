from Board import Board
from copy import deepcopy
from bigtree import Node, print_tree, tree_to_dict, dict_to_tree
from pickle import dump, load
from operator import attrgetter


class Minimax:
    def __init__(self, maximising_marker, minimising_marker, game_setup_arguments):
        self.maximising_marker = maximising_marker
        self.minimising_marker = minimising_marker
        self.game_setup_arguments = game_setup_arguments
        self.tree = None
        self.current_node = None

    def best_move(self, state):
        current_board = Board(*self.game_setup_arguments, deepcopy(state))
        scores = []
        for column in current_board.get_valid_moves():
            current_board.make_move(column, self.maximising_marker)
            score = self.minimax(current_board.grid, False)
            scores.append((score, column))
            current_board.grid = deepcopy(state)
        return scores

    def minimax(self, state, is_maximising):
        if (score := self.evaluate(state)) is not None:
            return score
        return (max if is_maximising else min)(
            self.minimax(possible_state, not is_maximising)
            for possible_state, column in self.possible_new_states(deepcopy(state), is_maximising)
        )

    def best_move_tree(self, state):
        current_board = Board(*self.game_setup_arguments, deepcopy(state))
        scores = []
        nodes = []
        for column in current_board.get_valid_moves():
            current_board.make_move(column, self.maximising_marker)
            score, child_node = self.minimax_tree(current_board.grid, False, str(column))
            nodes.append(child_node)
            scores.append((score, column))
            current_board.grid = deepcopy(state)
        root_node = Node(name=str(" "), children=nodes, score=1)
        self.tree = root_node
        return scores

    def minimax_tree(self, state, is_maximising, previous_moves):
        if (score := self.evaluate(state)) is not None:
            node = Node(name=str(previous_moves), score=str(score))
            return score, node
        scores = []
        nodes = []
        for possible_state, column in self.possible_new_states(deepcopy(state), is_maximising): #tupple
            score, child_node = self.minimax_tree(possible_state, not is_maximising, previous_moves + str(column))
            nodes.append(child_node)
            scores.append(score)
        if is_maximising:
            node = Node(name=str(previous_moves), score=str(max(scores)), children=nodes)
            return max(scores), node
        else:
            node = Node(name=str(previous_moves), score=str(min(scores)), children=nodes)
            return min(scores), node

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
        current_board = Board(*self.game_setup_arguments, deepcopy(state))
        if current_board.check_victory()[0] is True or len(current_board.get_valid_moves()) == 0:
            if current_board.check_victory()[1] == self.maximising_marker:
                return 1
            elif current_board.check_victory()[1] == self.minimising_marker:
                return -1
            return 0
        return None

    def store_tree(self, file_name="minimax_tree.txt"):
        tree = tree_to_dict(self.tree, name_key="name", parent_key="parent", attr_dict={"score": "score"})
        with open(file_name, "wb") as file:
            dump(tree, file)

    def load_tree(self, file_name="minimax_tree.txt"):
        with open(file_name, "rb") as file:
            tree = load(file)
        self.tree = dict_to_tree(tree)
        self.current_node = self.tree

    def next_best_move(self, is_maximising):
        child_nodes = self.current_node.children
        best_move = max(child_nodes, key=attrgetter('score')) if is_maximising else min(child_nodes, key=attrgetter('score'))
        return int(best_move.name[-1])

    def follow_move(self, column):
        for node in self.current_node.children:
            if column == int(node.name[-1]):
                self.current_node = node


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
    b = Minimax(1, 2, [6, 7, 0, 1, 2, "R"])
    moves = b.best_move_tree(a.grid)
    print(moves)
    print("Best move:", max(moves))
    b.store_tree()
    print_tree(b.tree, attr_list=["score"])
