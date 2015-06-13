#!/usr/bin/python
#
# -*- mode: python -*-
# vi: set ft=python

"""This script:

  1. Initializes a git repository in the current directory.
  2. Adds the VLAD project as a submodule.
  3. Clones a git repository into the current directory.
  4. Adds that repository and this script to the intial repository's .gitignore
     file."""

"""Modules"""
import os, shutil, subprocess, sys

"""Variables"""
vlad_remote = "git@github.com:hashbangcode/vlad.git"
vlad_project_directory = os.path.dirname(os.path.abspath(__file__))

"""Build"""
try:
    """User input"""
    project_remote = sys.argv[1]
    project_directory = os.path.splitext(os.path.split(project_remote)[1])[0]

    """cd"""
    subprocess.check_call("cd ..", shell = True)

    """gitignore"""
    try:
        gitignore = open(".gitignore", "w")
        gitignore.write("{0}\nsetup.py".format(project_directory))
        gitignore.close()
    except IndexError:
        print "Unable to create .gitignore file!"

    """git init"""
    subprocess.check_call("git init .", shell = True)

    """git submodule add ..."""
    subprocess.check_call("git submodule add {0} vlad".format(vlad_remote), shell = True)

    """git commit"""
    subprocess.check_call("git add .", shell = True)
    subprocess.check_call("git commit -m \"Adds project container, .gitignore, and VLAD submodule to repository.\"", shell = True)

    """git clone"""
    subprocess.check_call("git clone {0}".format(project_remote), shell = True)

    """Advice"""
    print "\n"
    print "Project setup complete. You can now manage your project (in `{0}`), configure VLAD in the root directory, and update the VLAD codebase from inside `vlad`.".format(project_directory)
    print "To get started, you should:"
    print "\n"
    print "\t1. Add a git remote to this repository and push."
    print "\t3. Read about and configure VLAD: http://vlad-docs.readthedocs.org/en/latest."
    print "\n"

    """Cleanup"""
    shutil.rmtree(vlad_project_directory)

except IndexError:
    print "You must provide a repository for your project!"
