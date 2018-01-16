USE_PKGBUILD=1
include /usr/local/share/luggage/luggage.make

TITLE=ants_client
REVERSE_DOMAIN=com.github.antsframework.ants
PACKAGE_VERSION:=$(shell grep ^__version__ ../bin/ants | cut -d "'" -f 2 )
PAYLOAD=\
		ants_client_virtualenv \
		pack-script-preinstall \
		pack-script-postinstall \
		pack-pathd \
		pack-Library-LaunchDaemons-ch.unibas.its.cs.ants.plist \
		pack-Library-LaunchDaemons-ch.unibas.its.cs.ants.run-now.plist

ANTS_LIB=/Library/ANTS-Framework
VENV_PYTHON_EXE=${ANTS_LIB}/bin/python

setup_virtualenv:
	# Install ants_client into a virtual environment
	# We could install virtualenv with --user but the luggage is running as root
	@sudo mkdir -p ${WORK_D}${ANTS_LIB}
	@sudo /usr/local/bin/pip install virtualenv
	@sudo /usr/local/bin/virtualenv ${WORK_D}${ANTS_LIB}
	@sudo ${WORK_D}${ANTS_LIB}/bin/pip install ants_client --pre
	@sudo find ${WORK_D} -name "*.pyc" -exec rm -rf {} \;

fix_venv_path: setup_virtualenv
	# Delete build dir reference in venv path
	# Source: https://github.com/google/macops/blob/master/packages/python/Makefile
	for f in $$(/usr/bin/sudo grep -RIl ${WORK_D} ${WORK_D});do \
		/usr/bin/sudo sed -i '' -e "s^${WORK_D}^^" $${f}; \
	done

fix_venv_path_inventory: setup_virtualenv
	# Set correct hashbang for inventory scripts
	# This is necessary because ansible-pull doesn't have antslib in it's path
	for f in $$(/usr/bin/sudo grep -RIl '#!/usr/bin/env python' ${WORK_D}/${ANTS_LIB}/lib/python2.7/site-packages/antslib/inventory);do \
		/usr/bin/sudo sed -i '' -- 's/\/usr\/bin\/env python/\/Library\/ANTS-Framework\/bin\/python/g' $${f}; \
	done

ants_client_virtualenv: fix_venv_path fix_venv_path_inventory

l_pathd:
	@sudo mkdir -p ${WORK_D}/private/etc/paths.d
	@sudo chown -R root:wheel ${WORK_D}/private/etc/paths.d
	@sudo chmod -R 755 ${WORK_D}/private/etc/paths.d

pack-pathd: l_pathd
	@sudo ${CP} ch.unibas.its.cs.ants ${WORK_D}/private/etc/paths.d
	@sudo chown -R root:wheel ${WORK_D}/private/etc/paths.d/ch.unibas.its.cs.ants
	@sudo chmod -R 644 ${WORK_D}/private/etc/paths.d/ch.unibas.its.cs.ants

ants_client:
	# Install ants_client to system python
	@sudo /usr/local/bin/pip install --root ${WORK_D} -I ants_client --pre
