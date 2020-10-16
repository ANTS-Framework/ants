USE_PKGBUILD=1
include /usr/local/share/luggage/luggage.make

TITLE=ants_client
REVERSE_DOMAIN=com.github.antsframework.ants
PACKAGE_VERSION:=$(shell grep ^__version__ ../bin/ants | cut -d '"' -f 2 )
PAYLOAD=\
		ants_client_relocatable_python \
		pack-script-preinstall \
		pack-script-postinstall \
		pack-Library-LaunchDaemons-ch.unibas.its.cs.ants.plist \
		pack-Library-LaunchDaemons-ch.unibas.its.cs.ants.run-now.plist

ANTS_LIB=/Library/ANTS-Framework
VENV_PYTHON_EXE=${ANTS_LIB}/bin/python
PYTHON_VERSION=3.8.5

clone_reloc_python:
	# Clone the relocatable python project (https://github.com/gregneagle/relocatable-python) into /tmp
	# First remove the directory if it exists
	@sudo rm -rf /private/tmp/reloc_python
	git clone https://github.com/gregneagle/relocatable-python.git /private/tmp/reloc_python

setup_reloc_python:
	# Use the relocatable python project to create a python framework and install ants-client
	echo "Using python Version ${PYTHON_VERSION}"
	@sudo mkdir -p ${WORK_D}${ANTS_LIB}
	@sudo /private/tmp/reloc_python/make_relocatable_python_framework.py --pip-requirements requirements_pkg.txt --destination ${WORK_D}${ANTS_LIB} --python-version ${PYTHON_VERSION}

fix_python_path:
	# Set correct hashbang in python files
	# Source: https://github.com/google/macops/blob/master/packages/python/Makefile
	# This is necessary because we install the python.framework in /tmp for packaging and therefore the paths map towards /tmp
	for f in $$(/usr/bin/sudo grep -RIl ${WORK_D} ${WORK_D});do \
		/usr/bin/sudo sed -i '' -e "s^/private${WORK_D}^^" $${f}; \
	done

ants_client_relocatable_python: clone_reloc_python setup_reloc_python fix_python_path
