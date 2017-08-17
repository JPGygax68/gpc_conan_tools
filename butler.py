#!python3

import os
import sys
#import subprocess as sub
import pathlib as pl
import importlib as il
import inspect


print("Butler V0.00")

have_conanfile   = pl.Path('conanfile.txt').is_file()
have_conanrecipe = pl.Path('conanfile.py' ).is_file()

if have_conanfile and have_conanrecipe:
    print("CAUTION! This directory has both a conanfile and a conan recipe, aborting for safety")
    sys.exit()
if have_conanfile:
    print("conanfile found")
if have_conanrecipe:
    print("conan recipe found, trying to extract dependencies")
    spec = il.util.spec_from_file_location("recipe", "./conanfile.py")
    module = il.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for name, cls in inspect.getmembers(module, inspect.isclass):
        for base in cls.__bases__:
            if base.__name__ == "ConanFile":
                print("Recipe class found (%s)" % cls.__name__)
                inst = cls()
                print("Requires: %s" % inst.requires)
    #recipe.


