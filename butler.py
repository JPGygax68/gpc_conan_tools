#!python3

import os
import sys
import pathlib as pl
import subprocess as sub


print("Butler V0.00")

have_conanfile   = pl.Path('conanfile.txt').is_file()
have_conanrecipe = pl.Path('conanfile.py' ).is_file()

def get_requirements(info):
    """Extracts the list of dependencies from the output of "conan info ." (supplied as a string)."""
    reqs = []
    branch = []
    last_indent = -1
    for line in [_.rstrip() for _ in info.split("\n")]:
        data = line.lstrip()
        indent = len(line) - len(data)
        if indent > last_indent:
            branch.append((data, indent))
            last_indent = indent
        elif indent == last_indent:
            branch[-1] = (data, indent)
        elif indent < last_indent:
            while True:
                branch.pop()
                if indent >= branch[-1][1]: 
                    last_indent = indent
                    break
        parent = [_[0] for _ in branch[:-1]]
        if parent == ["PROJECT", "Requires:"]:
            yield data
    
if have_conanfile and have_conanrecipe:
    print("CAUTION! This directory has both a conanfile and a conan recipe, aborting for safety")
    sys.exit()
if have_conanfile:
    print("conanfile found")
if have_conanrecipe:
    print("conan recipe found, querying list of dependencies")
    cp = sub.run("conan info .", stdout=sub.PIPE, stderr=sub.PIPE)
    if cp.returncode == 0:
        print("Requirements:")
        for _ in get_requirements(cp.stdout.decode()):
            print(_)
    else:
        print("error!")
        print(cp.stdout.decode(), cp.stderr.decode())

