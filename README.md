django-nonrel-start-project
==================

A startup project for django-nonrel with a script that allows you to install all django-non-rel modules as git submodules.

Because setting up the django-non-rel is a pain in the ass, I made a script that installs all necessary django-non-rel modules as git submodules and then performs all necessary linking. Only the add-django-nonrel-submodules.py is mine, the rest is the copy of the https://github.com/django-nonrel/django-testapp.

This script is coupled to linux compatible environment. I wrote it to make my life easier on Mac OS X using system-installed Python 2.7.1. Feel free to do whatever you like with the script so that it helps you as well. I tried to make it as readable and self-descriptive as I could in the limited time I had. Even if you never used Python before you should be able to read it (no fancy stuff here).

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
      -n                    Only prints the commands but does not execute them.
	  --keep-symlinks       Symlinks will not be affected by any command.
	  --skip-git-cmds       Commands operating on git repository will not be
	                        executed.


# How to use this stuff in the *INTENDED* way.

## Default simple installation
You want to simply install the _django_nonrel_ modules as git submodules in the default _django-nonrel-lib_ folder. In this case you simply run

    $ python add-django-nonrel-submodules.py

## Changing destination folder
You want to change the name of the default django lib folder:

    $ python add-django-nonrel-submodules.py -f my_django_lib_folder

## Switching between the master and development branches
This is really the reason you need the script to do it quickly and frequently. django-non-rel stability is (for me) questionable and so sometimes this is the _develop_ branch that works and the _master_ is unstable. So sometimes it is nice to be able to switch between branches and see what's happening. Additionally, just to make everyones life easier, most branches have _develop_ as the default branch but you must be prepared that some have _master_ as the default branch. Using the `-b <branch_name>` command with `git submodule add` fails when used on the default branch. The script is trying to solve the problem for you, but if the heroes from django_nonrel decide to change the policy the script needs to be updated (easy to do: just adjust the _default_branch_ directory options in the repositories structures in the code).
The default branch is _develop_.

So let's rock. Say you created submodules from the _develop_ branch and you would like to take a look if the master branch still works. So first you want to get rid of the symlinks in your root folder:

    $ python add-django-nonrel-submodules.py -c -s

The `-c` option says clean all, but than `-s` option says "relax" I will actually only remove symlinks. If you do not specify the `-s` option then `-c` will do the following:

1. It will first remove the symlinks (it does not remove the symlink for an extra module like _docs_ because no symlink will be created in such a case).

2. It will issue the following _git_ commands for each (sub)module:

        git rm --cached --ignore-unmatch <path_to_submodule>
        git config -f .git/config --remove-section submodule.<path_to_submodule>
        git config -f .gitmodules --remove-section submodule.<path_to_submodule>
        rm -Rf .git/modules/<path_to_submodule>

    See also the description of the `--skip-git-cmds` and `--keep-symlinks` options in the _Installing or deleting only one selected module_ section below.

3. It will remove the destination lib folder.

**NOTE** The script _.gitmodules_ will not be deleted - you may have other submodules in your project.

Now, you can create submodules for your master branch:

    $ python add-django-nonrel-submodules.py -b master -f your_master_branch_folder

This will create git submodules in _your_master_branch_folder_ folder and symlink to it.

Now you may want to go back to the _develop_ branch which you created earlier. Again, delete the symlinks with

    $ python add-django-nonrel-submodules.py -c -s

and then just symlink to the old (default in this case) folder:

    $ python add-django-nonrel-submodules.py -s

Notice the `-s` option - only symlinks will be created.

## Installing or deleting only one selected module.
Sometimes something goes wrong with one module only. Yes, it sucks, but the script can help here as well.
Say you want to remove completely just one module. First you need to know which modules are supported, and so you say:

    $ python add-django-nonrel-submodules.py -l

Option `-l` lists all available module. Know to delete a specific module you do:

    $ python add-django-nonrel-submodules.py -d <module_name>

That's it. Both the submodule and the link will be removed. When removing the module from the git repository the following commands are executed:

    git rm --cached --ignore-unmatch <path_to_submodule>
	git config -f .git/config --remove-section submodule.<path_to_submodule>
	git config -f .gitmodules --remove-section submodule.<path_to_submodule>
    rm -Rf .git/modules/<path_to_submodule>

Sometimes you may want to skip these commands (especially when any of them fails - than it will cause the whole script to fails). For this you have the
`--skip-git-cmds`:

    $ python add-django-nonrel-submodules.py -d <module_name> --skip-git-cmds

And finally, sometimes you may want to remove submodules but actually keep the symlinks (this may happen when you have another _lib_ folder with different branch and you do not want to use it anymore). The option you may be looking for in such a case is `--keep-symlinks`:

    $ python add-django-nonrel-submodules.py -d <module_name> --keep-symlinks

If you only wanted to remove symlink but leave the submodule in place, you have the `-s` option.

    $ python add-django-nonrel-submodules.py -d <module_name> -s

Finally, to install a module (git submodule + symlinking):

    $ python add-django-nonrel-submodules.py -m <module_name>

and to only add a symlink to a specific submodule:

    $ python add-django-nonrel-submodules.py -m <module_name> -s

## Installing extras
If you want to add (as git submodules) also the original django-testapp, docs, and django-nonrel.github.com repositories to your destination library folder, you can use the `-e` option:

    $ python add-django-nonrel-submodules.py -e

## Preview before everything turns into a crap :)
Yes, the script allows you to just see the commands that will be executed without actually executing them:

    $ python add-django-nonrel-submodules.py -n
