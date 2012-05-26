#!/usr/bin/env python

import sys
import argparse
import subprocess

DJANGO_GIT_ROOT = "https://github.com/django-nonrel/"
ADIEU_GIT_ROOT = "https://github.com/adieu/"

description = 'django-nonrel modules installer script. Adds django-nonrel modules as subodules to the project and symlinks them to the appropriate folders.'

def separator(text):
	print "********************************************************"
	print text
	print "********************************************************"
	
def add_trailing_slash(path):
	if 0 != len(path) and '/' != path[len(path)-1]:
		return path + '/'
	else:
		return path
		
def create_lib_folder():
	execute_command("mkdir -p %s" % lib_folder)
		
	
def list_modules_and_exit():
	separator("%s repositories:" % DJANGO_GIT_ROOT)
	for module_description in django_nonrel_git_repositories:
		print "%s" % module_description['git-module']
	separator("%s repositories:" % ADIEU_GIT_ROOT)
	for module_description in adieu_django_autoload_git_repository:
		print "%s" % module_description['git-module']
	sys.exit(0)
	
def execute_command(cmd):
	print cmd
	if preview_only:
		return
	try:
		output = subprocess.check_output(cmd.split(' '))
	except subprocess.CalledProcessError as err:
		print 'ERROR:',err
		sys.exit(0)
	else:
		if 0 != len(output):
			print output

def add_git_submodule(root,module_descriptor):
	if not only_symlinks and not skip_git:
		if module_descriptor['force-default-branch'] or branch_name == module_descriptor['default-branch']:
			execute_command("git submodule add %s%s.git %s%s" % (root,module_descriptor['git-module'],lib_folder,module_descriptor['git-module']))
		else:
			execute_command("git submodule add -b %s %s%s.git %s%s" % (branch_name,root,module_descriptor['git-module'],lib_folder,module_descriptor['git-module']))

def link_module(module_descriptor):
	execute_command("ln -s %s%s %s" % (lib_folder,module_descriptor['source'],module_descriptor['target']))
			
def remove_symlink(path):
	if not keep_symlinks:
		execute_command("rm -f %s" % path)

def remove_git_submodule(submodule):
	if not only_symlinks:
		if not skip_git:
			execute_command("git rm --cached --ignore-unmatch %s%s" % (lib_folder,submodule))
			execute_command("git config -f .git/config --remove-section submodule.%s%s" % (lib_folder,submodule))
			execute_command("git config -f .gitmodules --remove-section submodule.%s%s" % (lib_folder,submodule))
		execute_command("rm -Rf .git/modules/%s%s" % (lib_folder,submodule))

def remove_submodule_folder(submodule):
	if not only_symlinks:
		execute_command("rm -rf %s%s" % (lib_folder,submodule))

def remove_lib_folder():
	if not only_symlinks:
		execute_command("rm -rf %s" % lib_folder)

def clean_repositories(repositories):
	for module_descriptor in repositories:
		remove_symlink(module_descriptor['target'])
		remove_git_submodule(module_descriptor['git-module'])

def clean_extras(repositories):
	for module_descriptor in repositories:
		remove_git_submodule(module_descriptor['git-module'])

	
def clean_and_exit():
	clean_repositories(django_nonrel_git_repositories)
	clean_repositories(adieu_django_autoload_git_repository)
	clean_extras(extras)
	remove_lib_folder()
	sys.exit(0)
		
def add_submodules(git_root,modules):
	for module_descriptor in modules:
		install_module(git_root,module_descriptor)

def add_extras(git_root,modules):
	for module_descriptor in modules:
		add_git_submodule(git_root,module_descriptor)

def delete_submodule(module_descriptor):
	remove_symlink(module_descriptor['target'])
	remove_git_submodule(module_descriptor['git-module'])
	remove_submodule_folder(module_descriptor['git-module'])

def delete_extra(module_descriptor):
	remove_git_submodule(module_descriptor['git-module'])
	remove_submodule_folder(module_descriptor['git-module'])

def install_module(root,module_descriptor):
	add_git_submodule(root,module_descriptor)
	link_module(module_descriptor)
	
def add_module_and_exit(module_name):
	for module_descriptor in django_nonrel_git_repositories:
		if module_name == module_descriptor['git-module']:
			add_submodules(DJANGO_GIT_ROOT,[module_descriptor])
			sys.exit(0)
	for module_descriptor in adieu_django_autoload_git_repository:
		if module_name == module_descriptor['git-module']:
			add_submodules(ADIEU_GIT_ROOT,[module_descriptor])
			sys.exit(0)
	for module_descriptor in extras:
		if module_name == module_descriptor['git-module']:
			add_extras(DJANGO_GIT_ROOT,[module_descriptor])
			sys.exit(0)
	sys.exit(1)
	
def delete_module_and_exit(module_name):
	for module_descriptor in django_nonrel_git_repositories:
		if module_name == module_descriptor['git-module']:
			delete_submodule(module_descriptor)
			sys.exit(0)
	for module_descriptor in adieu_django_autoload_git_repository:
		if module_name == module_descriptor['git-module']:
			delete_submodule(module_descriptor)
			sys.exit(0)
	for module_descriptor in extras:
		if module_name == module_descriptor['git-module']:
			delete_extra(module_descriptor)
			sys.exit(0)
	sys.exit(1)

django_nonrel_git_repositories = [{'git-module':'djangoappengine','source':'djangoappengine','target':'djangoappengine','default-branch':'develop','force-default-branch':False},
								  {'git-module':'djangotoolbox','source':'djangotoolbox/djangotoolbox','target':'djangotoolbox','default-branch':'develop','force-default-branch':False},
								  {'git-module':'django-permission-backend-nonrel','source':'django-permission-backend-nonrel/permission_backend_nonrel','target':'permission_backend_nonrel','default-branch':'develop','force-default-branch':False},
								  {'git-module':'django-nonrel','source':'django-nonrel/django','target':'django','default-branch':'develop','force-default-branch':False},
								  {'git-module':'django-dbindexer','source':'django-dbindexer/dbindexer','target':'dbindexer','default-branch':'develop','force-default-branch':False},
								  {'git-module':'nonrel-search','source':'nonrel-search/search','target':'search','default-branch':'develop','force-default-branch':False}]
								
adieu_django_autoload_git_repository = [{'git-module':'django-autoload','source':'django-autoload/autoload','target':'autoload','default-branch':'master','force-default-branch':True}]

extras = [{'git-module':'django-testapp','default-branch':'develop','force-default-branch':False},
		  {'git-module':'docs','default-branch':'master','force-default-branch':True},
		  {'git-module':'django-nonrel.github.com','default-branch':'master','force-default-branch':True}]

parser = argparse.ArgumentParser(
	description=description,
	version='1.0')

parser.add_argument('-m',action="store",dest="module_name",help="Name of the module to install. Only this module will be installed.")
parser.add_argument('-d',action="store",dest="delete_module_name",help="Name of the module to delete. Only this module will be deleted.")	
parser.add_argument('-b',action="store",default="develop",dest="branch_name",help="Branch to clone. Default is 'develop'.")
parser.add_argument('-f',action="store",default="django-nonrel-lib/",dest="lib_folder",help="Destination folder path. Both absolute and relative should work. Default is relative 'django-nonrel-lib/'")
parser.add_argument('-e',action="store_true",default=False,dest="install_extras_only",help="Installs django-testapp, docs, and django-nonrel.github.com to the destination folder and then exits.")
parser.add_argument('-s',action="store_true",default=False,dest="only_symlinks",help="If present, only creates or deletes symlinks.")
parser.add_argument('-l',action="store_true",default=False,dest="list_modules_only",help="Lists the (sub)modules to be installed and exits.")
parser.add_argument('-c',action="store_true",default=False,dest="clean_only",help="Removes submodules and then exits.")
parser.add_argument('-n',action="store_true",default=False,dest="preview_only",help="Only prints the commands but does not execute them.")
parser.add_argument('--keep-symlinks',action="store_true",default=False,dest="keep_symlinks",help="Symlinks will not be affected by any command.")
parser.add_argument('--skip-git-cmds',action="store_true",default=False,dest="skip_git",help="Commands operating on git repository will not be executed.")

cmd_line_args = parser.parse_args()
branch_name = cmd_line_args.branch_name
install_extras_only = cmd_line_args.install_extras_only
list_modules_only = cmd_line_args.list_modules_only
clean_only = cmd_line_args.clean_only
only_symlinks = cmd_line_args.only_symlinks
lib_folder = add_trailing_slash(cmd_line_args.lib_folder)
module_name = cmd_line_args.module_name
delete_module_name = cmd_line_args.delete_module_name
preview_only = cmd_line_args.preview_only
keep_symlinks = cmd_line_args.keep_symlinks
skip_git = cmd_line_args.skip_git

if clean_only:
	clean_and_exit()

if list_modules_only:
	list_modules_and_exit()
	
if delete_module_name and len(delete_module_name) > 0:
	delete_module_and_exit(delete_module_name)
	
if install_extras_only:
	add_extras(DJANGO_GIT_ROOT,extras)
	sys.exit(0)

create_lib_folder()

if module_name and len(module_name) > 0:
	add_module_and_exit(module_name)
	
add_submodules(DJANGO_GIT_ROOT,django_nonrel_git_repositories)
add_submodules(ADIEU_GIT_ROOT,adieu_django_autoload_git_repository)
