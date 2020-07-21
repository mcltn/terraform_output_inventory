#!/usr/bin/env python
import sys, json
from splitstream import splitfile

# use stdin to parse
if not sys.stdin.isatty():
    input_stream = sys.stdin
else:
    message = 'Expecting json to be piped in.'
    raise IndexError(message)

try:
    output_filename = sys.argv[1]
except IndexError:
    message = 'Need a filename to save output to.'
    raise IndexError(message)

json_inv = {}
for jsonstr in splitfile(sys.stdin, format="json"):
    json_inv = json.loads(jsonstr.decode('utf-8'))

with open(output_filename, "w") as f:
    # Create [allservers]
    f.write("[allservers]\n")
    for k in json_inv.keys():
        for v in json_inv[k]["value"]:
            f.write(v + "\n")
    f.write("\n")

    # Create sections for each Key
    for k in json_inv.keys():
        f.write("[" + k + "]\n")
        for v in json_inv[k]["value"]:
            f.write(v + "\n")
        f.write("\n")