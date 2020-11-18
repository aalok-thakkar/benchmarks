import sys
import os
import csv

MAXB = 3
MAXV = 7

benchmark_name = sys.argv[1]
rules_small_dl_path = benchmark_name + "/rules.small.dl"
inputs = []
rels = {}
outputs = []
types = {}

with open(rules_small_dl_path, 'r') as rules_file:
    for line in rules_file.readlines():
        if line[:2] == "//":
            continue
        elif ".decl" in line:
            line = line[6:]
            if line[-1] == '\n':
                line = line[:-1]
            # print(line)
            relname = line[:line.find("(")].strip()
            # print(relname)
            args = [ x[x.find(":")+1:].strip() for x in line[line.find("(")+1 : line.find(")")].split(',') ]
            # print(args)
            rels[relname] = args
        elif ".input" in line:
            if line[-1] == '\n':
                line = line[:-1]
            relname = line.split()[1].strip()
            inputs.append(relname)
        elif ".output" in line:
            if line[-1] == '\n':
                line = line[:-1]
            relname = line.split()[1].strip()
            outputs.append(relname)

s = ""
for i in inputs:
    s += "#modeb(" + str(MAXB) + ", " + i + "(" + ",".join(["var(" + t + ")" for t in rels[i]]) + "), (positive)).\n"

for o in outputs:
    s += "#modeh(" + o + "(" + ",".join(["var(" + t + ")" for t in rels[o]]) + ")).\n"

s += "#maxv(" + str(MAXV) + ").\n"

f = open(benchmark_name + "/modes.txt", "a")
f.write(s)
f.close()