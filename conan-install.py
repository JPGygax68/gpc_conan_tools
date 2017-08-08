#!python3

# DEPRECATED
# This script was supposed to do "conan install" on nested project directories.
# Since Conan does not work well with that pattern (at the time of writing: 2017-08-08),
# I decided to scrap this approach, with the intent of beginning work on a script, or
# collection of scripts, that handles more of the boilerplate work than just Conan.

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
    
# DEPRECATED:
# Crawling all the nest directories seemed like a good idea at the time, but Conan does not
# cooperate well with nested project directories.
if False:
    for root, dirs, files in os.walk(root_dir):
        print("(Examining directory \"%s\")" % root)
        if any(f in files for f in ["conanfile.txt", "conanfile.py"]):
            print("Found conanfile in directory %s, installing" % root)
            install_directory(root)
        dirs[:] = [d for d in dirs if d[0] != '.' and not d.startswith("build")]
else:
    install_directory(root_dir)
