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
import uuid


class Config:
    def __init__(self):
        self.delimiter = os.getenv("delimiter")
        self.time_column = os.getenv("time_column")
        self.data_cache_path = sys.argv[1]
        self.output_file = sys.argv[2]
        self.source_file_field = "source_file"
        self.inputs = list()
        for key, value in os.environ.items():
            if self.source_file_field in key:
                self.inputs.append(value)


config = Config()


def merge_files(file_1_name, file_2_name, out_file_name=uuid.uuid4().hex):
    out_file = open("{}/{}".format(config.data_cache_path, out_file_name), "w")
    file_1 = open("{}/{}".format(config.data_cache_path, file_1_name), "r")
    file_2 = open("{}/{}".format(config.data_cache_path, file_2_name), "r")
    first_line_1 = file_1.readline().strip()
    first_line_2 = file_2.readline().strip()
    first_line_2 = first_line_2.split(config.delimiter)
    time_col_2 = first_line_2.index(config.time_column)
    first_line_2.remove(config.time_column)
    new_first_line = first_line_1 + config.delimiter + config.delimiter.join(first_line_2)
    out_file.write(new_first_line + "\n")
    new_first_line = new_first_line.split(config.delimiter)
    time_col_new = new_first_line.index(config.time_column)
    right_padding = config.delimiter * len(first_line_2)
    left_padding = str()
    for num in range(len(first_line_1.split(config.delimiter))):
        if num == time_col_new:
            left_padding += "{}" + config.delimiter
        else:
            left_padding += config.delimiter
    for line in file_1:
        out_file.write(line.strip() + right_padding + "\n")
    for line in file_2:
        line = line.strip().split(config.delimiter)
        timestamp = line[time_col_2]
        line.remove(timestamp)
        out_file.write(left_padding.format(timestamp) + config.delimiter.join(line) + "\n")
    file_1.close()
    file_2.close()
    out_file.close()
    return out_file_name


input_files = list()
output_files = list()

for file in config.inputs:
    if len(input_files) < 2:
        input_files.append(file)
    else:
        output_files.append(merge_files(*input_files))
        input_files.clear()
        input_files.append(output_files[-1])
        input_files.append(file)
merge_files(*input_files, config.output_file)

print("merged {} files:".format(len(config.inputs)))

for file in output_files:
    os.remove("{}/{}".format(config.data_cache_path, file))



