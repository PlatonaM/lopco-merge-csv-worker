#!/bin/sh

#   Copyright 2021 InfAI (CC SES)
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


# Environment variables:
#
# $DEP_INSTANCE
# $JOB_CALLBACK_URL
# $delimiter
# $time_column
# $time_format
# $_x_source_file


merge_file="$(cat /proc/sys/kernel/random/uuid | echo $(read s; echo ${s//-}))"
output_file="$(cat /proc/sys/kernel/random/uuid | echo $(read s; echo ${s//-}))"
data_cache="/data_cache"


echo "merging files ..."
if python -u file_merge.py "$data_cache" "$merge_file"; then
    head -5 "$data_cache/$merge_file"
    echo "adding unix timestamps ..."
    if python -u add_unix_time.py "$data_cache" "$merge_file" "${merge_file}_1"; then
        head -5 "$data_cache/${merge_file}_1"
        sed_string="s/[^$delimiter]//g"
        col_num=$(head -1 "$data_cache/${merge_file}_1" | sed $sed_string | wc -c)
        echo "sorting lines ..."
        if sort -n -t $delimiter -k $col_num "$data_cache/${merge_file}_1" > "$data_cache/${merge_file}_2"; then
            head -5 "$data_cache/${merge_file}_2"
            let col_num=col_num-1
            echo "removing unix timestamps ..."
            if cut -d ";" -f "1"-$col_num "$data_cache/${merge_file}_2" > "$data_cache/${merge_file}_3"; then
                head -5 "$data_cache/${merge_file}_3"
                first_line=$(head -n 1 "$data_cache/$merge_file")
                echo "merging lines ..."
                if python -u line_merge.py "$data_cache" "${merge_file}_3" "$output_file" "$first_line"; then
                    head -5 "$data_cache/$output_file"
                    echo "total number of lines written:" $(( $(wc -l < "$data_cache/$output_file") - 1 ))
                    if ! curl -s -S --header 'Content-Type: application/json' --data "{\""$DEP_INSTANCE"\": {\"output_csv\": \""$output_file"\"}}" -X POST "$JOB_CALLBACK_URL"; then
                        echo "callback failed"
                        rm "$data_cache/$output_file"
                    fi
                else
                    echo "merging lines failed"
                fi
            else
                echo "removing unix timestamps failed"
            fi
        else
            echo "sorting lines failed"
        fi
    else
        echo "adding unix timestamps failed"
    fi
else
    echo "merging files failed"
fi


if [ -f "$data_cache/$merge_file" ]; then
    rm "$data_cache/$merge_file"
fi
if [ -f "$data_cache/${merge_file}_1" ]; then
    rm "$data_cache/${merge_file}_1"
fi
if [ -f "$data_cache/${merge_file}_2" ]; then
    rm "$data_cache/${merge_file}_2"
fi
if [ -f "$data_cache/${merge_file}_3" ]; then
    rm "$data_cache/${merge_file}_3"
fi
