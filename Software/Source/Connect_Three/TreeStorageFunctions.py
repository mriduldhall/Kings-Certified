from pathlib import Path
from os import fsync
from linecache import getline
from itertools import islice
from itertools import count as ct


class TreeStorageFunction:
    def __init__(self, player_begin, directory_name="TreeFiles", max_depth=0, flush_interval=1000000, seperator=','):
        self.max_depth = max_depth
        self.directory_name = directory_name
        self.files = []
        self.files_line_count = []
        self.append_count = 0
        self.flush_interval = flush_interval
        self.seperator = seperator
        self.player_begin = player_begin #True if robot starts

    def initialise_files(self):
        directory_addon = "Player1" if self.player_begin else "Player2"
        directory_name = self.directory_name + directory_addon
        Path(directory_name).mkdir(parents=True, exist_ok=True)
        for file_number in range(self.max_depth):
            self.files.append(open(directory_name + "/" + str(file_number + 1) + ".txt", "w"))
            self.files_line_count.append(0)

    def refresh_files(self):
        self.append_count = 0
        for file in self.files:
            file.flush()
            fsync(file.fileno())

    def close_files(self):
        for file in self.files:
            file.close()

    def write_node(self, value, score, depth, line=''):
        self.files[depth - 1].write(value + self.seperator + score + self.seperator + line + '\n')
        self.files_line_count[depth - 1] += 1
        self.append_count += 1
        if self.append_count >= self.flush_interval:
            self.refresh_files()
        return str(self.files_line_count[depth - 1])

    def read_node(self, depth, line):
        directory_addon = "Player1" if self.player_begin else "Player2"
        directory_name = self.directory_name + directory_addon
        line_contents = getline((directory_name + "/" + str(depth) + ".txt"), line)
        return (line_contents.strip()).split(self.seperator)

    def get_child_nodes(self, depth, start_line, end_line):
        directory_addon = "Player1" if self.player_begin else "Player2"
        directory_name = self.directory_name + directory_addon
        nodes = []
        with open((directory_name + "/" + str(depth) + ".txt"), 'r') as file_in:
            line_generator = islice(file_in, start_line - 1, end_line - 1)
            for line in line_generator:
                nodes.append((line.rstrip('\n')).split(self.seperator))
        return nodes

    def get_next_linevalue(self, depth, start_line, end_of_file):
        directory_addon = "Player1" if self.player_begin else "Player2"
        directory_name = self.directory_name + directory_addon
        with open((directory_name + "/" + str(depth) + ".txt"), 'r') as file_in:
            counter = 0
            lines_to_skip = start_line
            for _ in range(lines_to_skip):
                counter += 1
                next(file_in)
            while counter < end_of_file:
                print("EOF:", end_of_file)
                counter += 1
                line = str(next(file_in))
                print("line:", line)
                node = (line.rstrip('\n')).split(self.seperator)
                if node[2]:
                    file_in.close()
                    return int(node[2])
        return None
