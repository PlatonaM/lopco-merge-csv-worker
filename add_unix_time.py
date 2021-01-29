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


import datetime
import time
import os
import sys


class Config:
    def __init__(self):
        self.delimiter = os.getenv("delimiter")
        self.time_column = os.getenv("time_column")
        self.time_format = os.getenv("time_format")
        self.data_cache_path = sys.argv[1]
        self.input_file = sys.argv[2]
        self.output_file = sys.argv[3]


config = Config()


with open("{}/{}".format(config.data_cache_path, config.input_file), "r") as in_file:
    with open("{}/{}".format(config.data_cache_path, config.output_file), "w") as out_file:
        first_line = in_file.readline().strip()
        first_line = first_line.split(config.delimiter)
        time_col_num = first_line.index(config.time_column)
        for line in in_file:
            line = line.strip()
            line = line.split(config.delimiter)
            line.append("{}\n".format(time.mktime(datetime.datetime.strptime(line[time_col_num], config.time_format).timetuple())))
            out_file.write(config.delimiter.join(line))
