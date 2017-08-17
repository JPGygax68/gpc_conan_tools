#!python3

import os
import sys
import subprocess as sub


args = sys.argv[1:]
root_dir = ""
if args:
    root_dir = args[0]
if not root_dir:
    print("No directory specified, using .. (parent directory)")
    root_dir = ".."

def install_directory(dir):
    # TODO: the drawback of calling conan install twice is some work is done twice as well
    print("\nFor build_type = Release:")
    sub.run(["conan"] + "install -g cmake_multi -s build_type=Release -s compiler.runtime=MD --build=missing".split()  + [dir])
    print("\nFor build_type = Debug:")
    sub.run(["conan"] + "install -g cmake_multi -s build_type=Debug   -s compiler.runtime=MDd --build=missing".split() + [dir])
    print("")
    
install_directory(root_dir)
