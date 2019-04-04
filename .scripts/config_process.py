#!/usr/bin/env python3

# Preprocessor for i3 config files

import sys
import os

if len(sys.argv) < 4:
    print("Usage: PROG <defines> <infile> <outfile>")
    print("  where <defines> is a comma-separates list of strings.")
    exit(1)

infile = None
with open(sys.argv[2], 'r') as f:
    infile = f.read()

defines = sys.argv[1].split(',')

ctx = []
def included():
    global ctx
    keep = True
    for c in ctx:
        if c == "if-false":
            keep = False
    return keep
def process_line(line):
    global ctx
    line = "{}\n".format(line.rstrip())
    #print(line.rstrip())

    parsed = None
    def prefix(s):
        nonlocal line
        nonlocal parsed
        if line.startswith(s):
            parsed = line[len(s):].strip()
            return True
        else:
            parsed = None
            return False

    if prefix("# PP END"):
        ctx.pop()
        return "# EVAL PP END\n"
    elif not included():
        return "# SKIP " + line
    elif prefix("# PP"):
        line = parsed
        eval_res = ""
        extra_lines = ""
        if prefix("IF DEFINED"):
            def_list = parsed.split(",")
            if all(map(lambda x: x.strip() in defines, def_list)):
                ctx.append("if-true")
            else:
                ctx.append("if-false")
            eval_res = " = " + ctx[-1]
        elif prefix("INCLUDE"):
            parsed = os.path.expanduser(parsed)
            if os.path.isfile(parsed):
                eval_res = " ok"
                with open(parsed, "r") as f:
                    extra_lines = f.read().rstrip() + "\n"
            else:
                eval_res = " not found"
            pass
        else:
            return "# UNKNOWN PP {}\n".format(line)
        return "# EVAL PP {}{}\n{}".format(line, eval_res, extra_lines)
    else:
        return line

infile_pp = ""
infile_pp += "#########################################\n"
infile_pp += "# AUTGENERATED, DO NOT EDIT MANUALLY\n"
infile_pp += "#########################################\n"
infile_pp += "\n"
for line in infile.splitlines():
    infile_pp += process_line(line)

with open(sys.argv[3], 'w') as f:
    f.write(infile_pp)
