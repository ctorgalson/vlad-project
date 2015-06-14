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
import os, re, shutil, subprocess, sys, yaml

"""Variables"""
vlad_remote = "git@github.com:hashbangcode/vlad.git"
vlad_project_directory = os.path.dirname(os.path.abspath(__file__))
vlad_defaults = dict(
    webserver_hostname = 'drupal.local',
    webserver_hostname_aliases = [
        "www.drupal.local"
    ],
    boxipaddress = "192.168.100.100",
    boxname = "vlad",
    host_synced_folder = "./docroot",
    dbname = []
)

"""Tools"""
def __string_setting_input(dictionary, key, prompt_pattern):
    return raw_input(prompt_pattern.format(key, dictionary[key])) or dictionary[key]

def __list_setting_input(dictionary, key, prompt_pattern):
    list_input = raw_input(prompt_pattern.format(key, dictionary[key]))
    if list_input is not dictionary[key]:
        value = re.compile(" +|, ?").split(list_input) or list_input
    else:
        value = dictionary[key]
    return value

"""Build."""
try:
    """Argument input."""
    project_remote = sys.argv[1]
    project_directory = os.path.splitext(os.path.split(project_remote)[1])[0]

    """cd"""
    subprocess.check_call("cd ..", shell = True)

    """Further input.

    We are not looping through the dict a) because the order will not be
    respected, and b) because we want to offer advice about the expected input
    for each different setting."""

    """Set up the formats for our input prompts."""
    string_prompt = "{0} {1}: "
    list_prompt = "{0}: "

    """webserver_hostname"""
    print "\nPlease provide the webserver hostname for this box."
    vlad_defaults["webserver_hostname"] = __string_setting_input(vlad_defaults, "webserver_hostname", string_prompt)

    """webserver_hostname_aliases"""
    print "\nPlease provide any hostname aliases for this box as a comma or string-separated list."
    vlad_defaults["webserver_hostname_aliases"] = __list_setting_input(vlad_defaults, "webserver_hostname_aliases", list_prompt)

    """boxipaddress"""
    print "\nPlease provide the local IP address at which to access this box."
    vlad_defaults["boxipaddress"] = __string_setting_input(vlad_defaults, "boxipaddress", string_prompt)

    """boxname"""
    print "\nPlease provide the box name for this server."
    vlad_defaults["boxname"] = __string_setting_input(vlad_defaults, "boxname", string_prompt)

    """host_synced_folder"""
    print "\nPlease provide the path to the docroot of the website relative to ./vlad/vagrantfile."
    vlad_defaults["host_synced_folder"] = __string_setting_input(vlad_defaults, "host_synced_folder", string_prompt)

    """dbname"""
    print "\nPlease provide any databases that should be created for this box as a comma or string-separated list."
    vlad_defaults["dbname"] = __list_setting_input(vlad_defaults, "dbname", list_prompt)

    with open("vlad_settings.yml", "w") as output:
         output.write(yaml.dump(vlad_defaults, default_flow_style = False))

    """gitignore"""
    try:
        gitignore = open(".gitignore", "w")
        gitignore.write("{0}\nvlad-project".format(project_directory))
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
    print "\t2. Read about and configure VLAD: http://vlad-docs.readthedocs.org/en/latest."
    print "\n"

    """Cleanup"""
#    shutil.rmtree(vlad_project_directory)

except IndexError:
    print "You must provide a repository for your project!"
