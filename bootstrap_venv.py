# this script executes the virtualenv bootstrapping script.  Destination dir is projectroot/.venv
# requires python>=3.3
import os, platform, sys
from os.path import join

if hasattr(sys, 'real_prefix') or  hasattr(sys, 'base_prefix'):
    print('virtual environment is activate, please deactivate before proceeding.')
    exit()

if platform.system() == 'Windows':
	os.system(join(os.getcwd(), 'setup.bat'))
else:
	os.system('bash ' + join(os.getcwd(), 'setup.sh'))
	