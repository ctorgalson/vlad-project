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
    host_synced_folder = "../docroot",
    aux_synced_folder = "../vlad_aux",
    synced_folder_type = "nfs",
    dbname = [],
    db_import_up = [],
    vlad_custom_play = True,
    vlad_custom_play_path = '../',
    vlad_custom_play_file = drupal_perms.yml
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
    string_prompt = "{0} [{1}]: "
    list_prompt = "{0}: "

    """webserver_hostname"""
    print "\nThe hostname of the site you are about to create. By default this is then combined with the variable webserver_hostname_alias to add 'www' to the start (string)."
    vlad_defaults["webserver_hostname"] = __string_setting_input(vlad_defaults, "webserver_hostname", string_prompt)

    """webserver_hostname_aliases"""
    print "\nIn order to support multiple projects, or Drupal multi-site installations, this lets you add a list of fully qualified names for your web server aliases (comma or space-separated list)."
    vlad_defaults["webserver_hostname_aliases"] = __list_setting_input(vlad_defaults, "webserver_hostname_aliases", list_prompt)

    """boxipaddress"""
    print "\nThe IP address of the virtual machine (string)."
    vlad_defaults["boxipaddress"] = __string_setting_input(vlad_defaults, "boxipaddress", string_prompt)

    """boxname"""
    print "\nThe name of the box that will be used by Vagrant to label the box inside your virtual machine manager of choice. This value should contain only letters, numbers, hyphens or dots (string)."
    vlad_defaults["boxname"] = __string_setting_input(vlad_defaults, "boxname", string_prompt)

    """host_synced_folder"""
    print "\nThis is the directory that will be used to serve the files from. Should be located inside the repository (string)"
    vlad_defaults["host_synced_folder"] = __string_setting_input(vlad_defaults, "host_synced_folder", string_prompt)

    """synced_folder_type"""
    print "\n*Only applicable for when running VLAD on a non-Windows host.* Use 'nfs' or 'rsync' for VM file editing in synced folder (string)."
    vlad_defaults["synced_folder_type"] = __string_setting_input(vlad_defaults, "synced_folder_type", string_prompt)

    """dbname"""
    print "\nthis is a list of databases that Vlad will generate. As a default a single database is created but this value can be changed to make Vlad add more databases (comma or space-separated list)."
    vlad_defaults["dbname"] = __list_setting_input(vlad_defaults, "dbname", list_prompt)

    """db_import_up"""
    print "Database to import at `vagrant up`. Database import won't occur if the first present database has any tables defined (in order to prevent data loss)."
    vlad_defaults["db_import_up"] = __list_setting_input(vlad_defaults, "db_import_up", list_prompt)

    """vlad settings"""
    try:
        """File system variables"""
        settings_directory = "settings"
        settings_file = "vlad_settings.yml"
        settings_path = os.path.join(settings_directory, settings_file)
        db_io_path = os.path.join("vlad_aux", "db_io")

        """Make the directory and try to write the file"""
        os.mkdir(settings_directory)
        os.makedirs(db_io_path)
        with open(settings_path, "w") as output:
            output.write(yaml.dump(vlad_defaults, default_flow_style = False))

        """Copy the db dump (if any) into the right place"""
        if len(vlad_defaults["db_import_up"]) == len(vlad_defaults["dbname"]):
            for d in vlad_defaults["db_import_up"]:
               shutil.copy(d, os.path.join(db_io_path, os.path.basename(d)))
        else:
            print "There should be a `db_import_up` value for each database in `dbname`!"

    except IndexError:
        print "Could not crate vlad settings file!"

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
