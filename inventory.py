#!/usr/bin/env python
import sys, json
from splitstream import splitfile

# use stdin to parse
if not sys.stdin.isatty():
    input_stream = sys.stdin
else:
    message = 'Expecting json to be piped in.'
    raise IndexError(message)

has_output_file = True
try:
    output_filename = sys.argv[1]
except IndexError:
    has_output_file = False
    #message = 'Need a filename to save output to.'
    #raise IndexError(message)

json_inv = {}
for jsonstr in splitfile(sys.stdin, format="json"):
    json_inv = json.loads(jsonstr.decode('utf-8'))

inventory_str = ""

# Create [allservers]
inventory_str += "[allservers]\n"
for k in json_inv.keys():
    if isinstance(json_inv[k]["value"], list):
        for v in json_inv[k]["value"]:
            inventory_str += v + "\n"
    else:
        inventory_str += json_inv[k]["value"] + "\n"
inventory_str += "\n"

# Create sections for each Key
for k in json_inv.keys():
    inventory_str += "[" + k + "]\n"
    if isinstance(json_inv[k]["value"], list):
        for v in json_inv[k]["value"]:
            inventory_str += v + "\n"
    else:
        inventory_str += json_inv[k]["value"] + "\n"
    inventory_str += "\n"

if has_output_file:
    with open(output_filename, "w") as f:
        f.write(inventory_str)
else:
    print(inventory_str)