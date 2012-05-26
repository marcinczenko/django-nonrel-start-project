django-nonrel-start-project
===========================

# A

A startup project for django-non-rel with a script that allows to install all django-non-rel modules as git submodules.

Because setting up the django-non-rel is a pain in the ass, I made a script that installs all necessary django-non-rel
modules as git submodules and then performs all necessary linking. Only the add-django-nonrel-submodules.py is mine, the
rest is the copy of the https://github.com/django-nonrel/django-testapp.

This script is coupled to linux compatible environment. I wrote it to make my life easier on Mac OS X using system-installed
Python 2.7.1. Feel free to do whatever you like with the script so that it helps you as well. I tried to make it as
readable and self-descriptive as I could in the limited time I had. Even if you never used Python before you should
be able to read it (no fancy stuff here).

Command line options:
---------------------

$ python add-django-nonrel-submodules.py -h
usage: add-django-nonrel-submodules.py [-h] [-v] [-m MODULE_NAME]
                                       [-d DELETE_MODULE_NAME]
                                       [-b BRANCH_NAME] [-f LIB_FOLDER] [-e]
                                       [-s] [-l] [-c]

django-nonrel modules installer script. Adds django-nonrel modules as
subodules to the project and symlinks them to the appropriate folders.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -m MODULE_NAME        Name of the module to install. Only this module will
                        be installed.
  -d DELETE_MODULE_NAME
                        Name of the module to delete. Only this module will be
                        deleted.
  -b BRANCH_NAME        Branch to clone. Default is 'develop'.
  -f LIB_FOLDER         Destination folder path. Both absolute and relative
                        should work. Default is relative 'django-nonrel-lib/'
  -e                    Installs django-testapp, docs, and django-
                        nonrel.github.com to the destination folder and then
                        exits.
  -s                    If present, only creates or deletes symlinks.
  -l                    Lists the (sub)modules to be installed and exits.
  -c                    Removes submodules and then exits.

============================================
How to use this stuff in the *INTENDED* way.

* Scenario 1
You want to simply install 