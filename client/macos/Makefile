include /usr/local/share/luggage/luggage.make
PACKAGE_VERSION=1.0
TITLE=ants
PACKAGE_NAME=ants_macOS-${PACKAGE_VERSION}
REVERSE_DOMAIN=ch.unibas.its.cs
PAYLOAD=\
	pack-ants \
	pack-pathd \
	pack-Library-LaunchDaemons-ch.unibas.its.cs.ants.plist \
	pack-Library-LaunchDaemons-ch.unibas.its.cs.ants.run-now.plist 

l_ants: l_usr_local
	@sudo mkdir ${WORK_D}/usr/local/ants
	@sudo chown -R root:wheel ${WORK_D}/usr/local/ants
	@sudo chmod -R 755 ${WORK_D}/usr/local/ants
	@sudo mkdir ${WORK_D}/usr/local/ants/etc
	@sudo chown -R root:wheel ${WORK_D}/usr/local/ants/etc
	@sudo chmod -R 755 ${WORK_D}/usr/local/ants/etc
	@sudo mkdir ${WORK_D}/usr/local/ants/antslib
	@sudo chown -R root:wheel ${WORK_D}/usr/local/ants/antslib
	@sudo chmod -R 755 ${WORK_D}/usr/local/ants/antslib

l_pathd: l_private_etc
	@sudo mkdir ${WORK_D}/private/etc/paths.d
	@sudo chown -R root:wheel ${WORK_D}/private/etc/paths.d
	@sudo chmod -R 755 ${WORK_D}/private/etc/paths.d

pack-ants: l_ants
	# Ants binary
	@sudo ${CP} ../ants.py ${WORK_D}/usr/local/ants/
	@sudo chown root:wheel ${WORK_D}/usr/local/ants/ants.py
	@sudo chmod 755 ${WORK_D}/usr/local/ants/ants.py
	# Inventory AD
	@sudo ${CP} ../inventory_ad.py ${WORK_D}/usr/local/ants/
	@sudo chown root:wheel ${WORK_D}/usr/local/ants/inventory_ad.py
	@sudo chmod 755 ${WORK_D}/usr/local/ants/inventory_ad.py
	# Inventory Default
	@sudo ${CP} ../inventory_default.py ${WORK_D}/usr/local/ants/
	@sudo chown root:wheel ${WORK_D}/usr/local/ants/inventory_default.py
	@sudo chmod 755 ${WORK_D}/usr/local/ants/inventory_default.py
	# Configuration
	@sudo ${CP} ../etc/ants.cfg ${WORK_D}/usr/local/ants/etc
	@sudo chown root:wheel ${WORK_D}/usr/local/ants/etc/ants.cfg
	@sudo chmod 644 ${WORK_D}/usr/local/ants/etc/ants.cfg
	# Lib
	@sudo find ../ -name "*.pyc" -exec rm -rf {} \;
	@sudo ${CP} -R ../antslib ${WORK_D}/usr/local/ants
	@sudo chown -R root:wheel ${WORK_D}/usr/local/ants/antslib
	@sudo chmod -R 755 ${WORK_D}/usr/local/ants/antslib

pack-pathd: l_pathd
	@sudo ${CP} ch.unibas.its.cs.ants ${WORK_D}/private/etc/paths.d
	@sudo chown -R root:wheel ${WORK_D}/private/etc/paths.d/ch.unibas.its.cs.ants
	@sudo chmod -R 644 ${WORK_D}/private/etc/paths.d/ch.unibas.its.cs.ants
