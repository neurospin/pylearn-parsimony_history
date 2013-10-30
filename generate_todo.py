#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Use in terminal: ./generate_todo.py

Created on Thu Jul 11 14:27:20 2013

@author:  Tommy Löfstedt
@email:   tommy.loefstedt@cea.fr
@license: TBD
"""

import os
import re
import string

PATH = "./parsimony/"
OUTPUT = "./TODO"

RE_PY_FILE = re.compile(".*\.py$")
RE_TODO = re.compile("^[ \t]*#[ \t]*TODO:.*$")  # TODO: Allow code before TODO
RE_COMMENT = re.compile("^[ \t]*#.*$")


def write(f, string):
    f.write(string + os.linesep)
#    print string

with open(OUTPUT, "w+") as out:
    write(out, "# This file is automatically generated by generate_todo.py")
    write(out, "")
    for path, dirs, files in os.walk(PATH):
        for filename in files:
            first_in_file = True
            fullpath = os.path.join(path, filename)
            if RE_PY_FILE.match(filename):
                with open(fullpath, "r") as f:
                    match_next_comment = False
                    for i, line in enumerate(f):
                        if RE_TODO.match(line):
                            if first_in_file:
                                write(out, "%s:" % fullpath)
                                write(out, "-" * len(fullpath))
                                first_in_file = False
                            write(out, "%d: %s" % (i + 1, string.strip(line)))
                            match_next_comment = True
                        elif match_next_comment and RE_COMMENT.match(line):
                            write(out, "%d: %s" % (i + 1, string.strip(line)))
                        else:
                            if match_next_comment:
                                write(out, "")
                            match_next_comment = False
#            if not first_in_file:
#                write(out, "")