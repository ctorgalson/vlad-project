# vlad-project
Small python script to download and arrange the file structure for a new Drupal project using [VLAD](https://drupal.org/project/vlad).

## Quickstart

  1. Create a directory for your project, e.g. `mkdir
     vlad-project-test`.
  2. Change directories into your new directory, e.g. `cd
     vlad-project-test`.
  3. Clone this repository, e.g. `git clone
     git@github.com:ctorgalson/vlad-project.git`.
  4. Run `setup.py` with the url of a git repository (**Note** there is a
     known bug if you clone using https**, so use `git@github.com...`),
     e.g. `python vlad-project/setup.py
     git@github.com:path/to/some/drupal/repo.git`.
  5. Answer the questions (note that the docroot path will be
     `../path/to/the/docroot/of/the/repo/from/step/4/docroot`
  6. Visit the site at the hostname you gave in step 5.
