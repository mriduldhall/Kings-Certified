from pathlib import Path
from os import fsync
from linecache import getline
from itertools import islice
from itertools import count as ct


class TreeStorageFunction:
    def __init__(self, max_depth=0, directory_name='TreeFiles', flush_interval=1000000, seperator=','):
        self.max_depth = max_depth
        self.directory_name = directory_name
        # self.directory_name = 'C:/Users/aryab/OneDrive - King\'s College London/King\'s Certificate/King Certified/Trees/Connect 3'
        # self.directory_name = 'M:/KCLMS Server/Connect-3/TreeFiles'
        self.files = []
        self.files_line_count = []
        self.append_count = 0
        self.flush_interval = flush_interval
        self.seperator = seperator

    def initialise_files(self):
        Path(self.directory_name).mkdir(parents=True, exist_ok=True)
        for file_number in range(self.max_depth):
            self.files.append(open(self.directory_name + "/" + str(file_number + 1) + ".txt", "w"))
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
        line_contents = getline((self.directory_name + "/" + str(depth) + ".txt"), line)
        return (line_contents.strip()).split(self.seperator)

    def get_child_nodes_v1(self, depth, start_line, end_line):
        nodes = []
        for current_line in range(start_line, end_line + 1):
            nodes.append(self.read_node(depth, current_line))
        print("Nodes", nodes)
        return nodes

    def get_child_nodes_v2(self, depth, start_line):
        nodes = []
        counter = 0
        while len(nodes) <= 5:
            line_contents = self.read_node(depth, int(start_line) + counter)
            if nodes:
                if line_contents[0] <= nodes[-1][0]:
                    return nodes
            nodes.append(line_contents)
            counter += 1
        print("Nodes", nodes)
        return nodes

    def get_child_nodes_v3(self, depth, start_line, end_line):
        nodes = []
        with open((self.directory_name + "/" + str(depth) + ".txt"), 'r') as file_in:
            line_generator = islice(file_in, start_line - 1, end_line - 1)
            for line in line_generator:
                nodes.append((line.rstrip('\n')).split(self.seperator))
        return nodes

    def get_next_linevalue(self, depth, start_line, end_of_file):
        with open((self.directory_name + "/" + str(depth) + ".txt"), 'r') as file_in:
            counter = 0
            lines_to_skip = start_line
            for _ in range(lines_to_skip):
                counter += 1
                next(file_in)
            while counter < end_of_file:
                counter += 1
                line = str(next(file_in))
                node = (line.rstrip('\n')).split(self.seperator)
                if node[2]:
                    file_in.close()
                    return int(node[2])
        return None
