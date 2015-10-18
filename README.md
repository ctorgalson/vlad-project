# vlad-project
Small python script to download and arrange the file structure for a new Drupal
project using [VLAD](https://drupal.org/project/vlad).

Developed mainly against Ubuntu 15.04, but should work as well on recent
OSX versions.

## Sample workflow

The project envisions a workflow like this (especially for quickly
getting up-to-speed on existing projects):

    $ mkdir example.com
    $ cd example.com
    $ cp ../example_drupal.sql example_drupal.sql
    $ git clone git@github.com:ctorgalson/vlad-project.git
    $ ./vlad-project/setup.py git@github.com:username/example.com.git
    $ cp ../settings.php example.com/docroot/sites/default/settings.php
    $ cd vlad
    $ vagrant up
    $ cd ..
    $ cp vlad-project/tools/* .
    $ npm install
    $ grunt

### Rationale

This setup involves *three* permanent git repositories:

  1. The repository of the actual Drupal project ("example.com" above),
  2. The repository of the Vlad configuration (created by setup.py),
  3. The Vlad repository (as a submodule of the Vlad configuration
     repository).

This makes it possible to:

  1. Keep the development environment configuration out of the main
     Drupal repository, but
  2. Maintain a shareable development environment repository, and
  3. Make use of upstream updates to Vlad.

### Sample workflow explained

The **Sample workflow** section above performs the following tasks:

#### `mkdir example.com`

  - Creates the project directory.

#### `cd example.com`

  - Make the new project directory the current working directory.

#### `cp ../example_drupal.sql example_drupal.sql`

  - Copies a Drupal database dump from some other directory to the
    current (project) directory.

#### `git clone git@github.com:ctorgalson/vlad-project.git`

  - Clones this repository into the project directory.

#### `./vlad-project/setup.py git@github.com:username/example.com.git`

  - Runs the `setup.py` script in this repository. The script:
    - Requests the following information:
      - The webserver hostname (e.g. `example.dev`),
      - Webserver hostname aliases: (e.g.
        `www.example.dev,www1.example.dev`),
      - The IP address for the box (e.g. `192.168.10.10` or `10.0.10.10`),
      - The name for the box (e.g. `EXAMPLE`).
      - The host synced folder (i.e. the document root of the project
        repository, e.g. `example.com/docroot`),
      - The synced folder type (e.g `nfs` or possibly `rsync`),
      - The database name (e.g. example_drupal.sql),
      - The database import up setting (i.e. whether or not to import a
        databse dump into the database, e.g. `example_drupal.sql`),
    - Creates a file at `settings/vlad_settings.yml`. A sample version
      of this file, `vlad_settings.example.yml` can be found in the root
      of this repository.
    - Copies the database dump (if one was provided) into the location
      expected by Vlad.
    - Copies the `drupal.yml` Ansible playbook into place in the project
      directory.
    - Initializes a git repository (including a `.gitignore` file) in the
      project directory that:
      - Ignores the main project, adds the `./vlad` directory as a git
        submodule, and adds all other non-excluded files to the repo.
    - Clones the github project provided into the project repository.

#### `cp ../settings.php example.com/docroot/sites/default/settings.php`

  - Copies a drupal `settings.php` file into the appropriate location in
    the project.

#### `cd vlad`

  - Changes the working directory to `./vlad`.

#### `vagrant up`

  - Starts the virtual machine (this will take some time at the
    beginning).

#### `cd ..`

  - Returns to the project directory.

#### **Optional**: `cp ./vlad-project/tools/* .`

  - Copies two files, `package.json` and `Gruntfile.js` into the project
    directory. The Grunt file can be used to auto-rsync the Vagrant
    synced folder in cases where a) `synced_folder_type` is set to
    `rsync`, **and** `rsync` can't be made to work in another way. See
    next steps.

#### **Optional**: `npm install`

  - Installs Grunt dependencies.

#### **Optional**: `grunt`

  - Runs Grunt watch task.
