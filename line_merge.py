"""
   Copyright 2021 InfAI (CC SES)
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at
       http://www.apache.org/licenses/LICENSE-2.0
   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""


import os
import sys


class Config:
    def __init__(self):
        self.delimiter = os.getenv("delimiter")
        self.time_column = os.getenv("time_column")
        self.data_cache_path = sys.argv[1]
        self.input_file = sys.argv[2]
        self.output_file = sys.argv[3]
        self.first_line = sys.argv[4]


config = Config()


with open("{}/{}".format(config.data_cache_path, config.input_file), "r") as in_file:
    with open("{}/{}".format(config.data_cache_path, config.output_file), "w") as out_file:
        out_file.write(config.first_line + "\n")
        first_line = config.first_line.split(config.delimiter)
        time_col_num = first_line.index(config.time_column)
        current_timestamp = None
        for line in in_file:
            line = line.strip()
            line = line.split(config.delimiter)
            if line[time_col_num] != current_timestamp:
                try:
                    out_file.write(config.delimiter.join(merge_line) + "\n")
                except NameError:
                    pass
                merge_line = [str()] * len(first_line)
                merge_line[time_col_num] = line[time_col_num]
                current_timestamp = line[time_col_num]
            for pos in range(len(line)):
                if line[pos] and pos != time_col_num:
                    merge_line[pos] = line[pos]
        out_file.write(config.delimiter.join(merge_line) + "\n")
