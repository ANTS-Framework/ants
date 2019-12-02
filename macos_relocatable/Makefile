USE_PKGBUILD=1
include /usr/local/share/luggage/luggage.make

TITLE=ants_client
REVERSE_DOMAIN=com.github.antsframework.ants
PACKAGE_VERSION:=$(shell grep ^__version__ ../bin/ants | cut -d '"' -f 2 )
PAYLOAD=\
		ants_client_relocatable_python \
		pack-script-preinstall \
		pack-script-postinstall \
		pack-pathd \
		pack-Library-LaunchDaemons-ch.unibas.its.cs.ants.plist \
		pack-Library-LaunchDaemons-ch.unibas.its.cs.ants.run-now.plist

ANTS_LIB=/Library/ANTS-Framework
VENV_PYTHON_EXE=${ANTS_LIB}/bin/python
PYTHON_VERSION=3.7.4

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
	# This is necessary because we install the python.framework in /tmp for packaging and therefore the paths map towards /tmp
	for f in $$(/usr/bin/sudo grep -GRIl '#!/private/tmp/the_luggage/ants_client-1.9.1/root/Library/ANTS-Framework/.*' ${WORK_D}/${ANTS_LIB}/Python.framework/Versions/Current/bin);do \
		/usr/bin/sudo sed -i '' -- 's/\/private\/tmp\/the_luggage\/ants_client-1.9.1\/root//g' $${f}; \
	done
	# Set the correct hashbang in the inventory scripts
	# This is necessary because ansible-pull doesn't have antslib in it's path
	for f in $$(/usr/bin/sudo grep -RIl '#!/usr/bin/env python' ${WORK_D}/${ANTS_LIB}/Python.framework/Versions/Current/lib/python*/site-packages/antslib/inventory);do \
		/usr/bin/sudo sed -i '' -- 's/\/usr\/bin\/env python/\/Library\/ANTS-Framework\/Python.framework\/Versions\/Current\/Resources\/Python.app\/Contents\/MacOS\/Python/g' $${f}; \
	done

ants_client_relocatable_python: clone_reloc_python setup_reloc_python fix_python_path

l_pathd:
	@sudo mkdir -p ${WORK_D}/private/etc/paths.d
	@sudo chown -R root:wheel ${WORK_D}/private/etc/paths.d
	@sudo chmod -R 755 ${WORK_D}/private/etc/paths.d

pack-pathd: l_pathd
	@sudo ${CP} ch.unibas.its.cs.ants ${WORK_D}/private/etc/paths.d
	@sudo chown -R root:wheel ${WORK_D}/private/etc/paths.d/ch.unibas.its.cs.ants
	@sudo chmod -R 644 ${WORK_D}/private/etc/paths.d/ch.unibas.its.cs.ants