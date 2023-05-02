from pathlib import Path
from os import fsync
from linecache import getline


class TreeStorageFunction:
    def __init__(self, max_depth=0, directory_name='TreeFiles', flush_interval=1000000, seperator=','):
        self.max_depth = max_depth
        self.directory_name = directory_name
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

    def write_node(self, value, score, depth, line='-1'):
        self.files[depth - 1].write(value + self.seperator + score + self.seperator + line + '\n')
        self.files_line_count[depth - 1] += 1
        self.append_count += 1
        if self.append_count >= self.flush_interval:
            self.refresh_files()
        return str(self.files_line_count[depth - 1])

    def read_node(self, depth, line):
        line_contents = getline((self.directory_name + "/" + str(depth) + ".txt"), line)
        if line_contents[11] == "-":
            line_contents = (line_contents[2], line_contents[7]), line_contents[11:13], line_contents[14:].strip()
        else:
            line_contents = (line_contents[2], line_contents[7]), line_contents[11:12], line_contents[13:].strip()
        return line_contents

    def coord_value(self, coord):
        row, column = coord
        return int(row) * 3 + int(column)

    def get_layer(self, depth, line_start, line_end):
        with open("TreeFiles/" + str(depth) + '.txt', "r") as file_in:
            lines = [line.rstrip() for line in file_in]
        file_in.close()
        
        layer = []
        for actual_line in range(line_start-1, line_end-1):
            line = lines[actual_line]
            if line[11] == "-":
                layer.append([(line[2], line[7]), line[11:13], line[14:]])
            else:
                layer.append([(line[2], line[7]), line[11:12], line[13:]])

        return layer
