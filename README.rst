==============
ANTS Framework
==============

.. image:: https://img.shields.io/pypi/v/ants_client.svg
    :target: https://pypi.python.org/pypi/ants_client/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/l/ants_client.svg
    :target: https://pypi.python.org/pypi/ants_client/
    :alt: License

ANTS is a framework to manage and apply macOS and Linux host configurations using Ansible Pull.

The ANTS Framework is developed by the Client Services Team of the `University of Basel <https://www.unibas.ch/>`__ `IT Services <https://its.unibas.ch>`__
and released under the `GNU General Public License Version 3 <https://www.gnu.org/licenses/gpl-3.0.en.html>`__.

`Ansible <https://docs.ansible.com/ansible/latest/index.html>`__ is a trademark of `Red Hat, Inc. <https://www.redhat.com>`__.

------------
Introduction
------------
The ANTS Framework consists of the following components:

- A wrapper for Ansible-Pull
- An Ansible Dynamic Inventory Script (MS Active Directory Connector)
- A modular collection of roles ready to be used
- Strong logging integration

------------
Requirements
------------
This project assumes that you are familiar with `Ansible <https://www.ansible.com/>`__
, `Git <https://git-scm.com/book/en/v2>`__ and the shell.

---------------
Getting started
---------------
*************************
Installing ants using pip
*************************
- Make sure ``git`` is installed on your machine
- Install the latest ants client using pip: ``pip install ants_client``
- Pip will install the ANTS client with a default configuration and put the executable in your path.

******************************************
Installing ants using macOS .pkg installer
******************************************
- Download the latest .pkg installer from the `releases page <https://github.com/ANTS-Framework/ants/releases/latest>`__.
- Execute the installer. This will take care of all dependencies.
- A launch daemon will be installed, running `ants` every 15 minutes. It will trigger after the next restart.

********
Run ants
********
- Open your terminal
- Start an ANTS run by typing ``ants``.
- Wait for ANTS to finish, then open another shell. You will see a new message of the day.

**************
What happened?
**************
Running ANTS with the default configuration will use ansible-pull to clone
`the ANTS playbook <https://github.com/ANTS-Framework/playbook>`__ via https from a github repository and execute an ansible run.

By default, this will generate ``/etc/motd`` to add a message of the day to your macOS or Linux host.
Logs of all the runs are stored at ``/var/log/ants``.

Also by default, ants will add github to your ``known_hosts`` file. This is important for later, when you want to enable git clone
using ssh.

----------------------
Where to go from here?
----------------------

*******************
Look at the options
*******************
Run ``ants -h`` to see all command line options.

****************************
Write your own configuration
****************************
Run ``ants --show-config`` to see the active configuration.

Run ``ants --initialize`` to write your own configuration.

Your local configuration file will be saved at ``/etc/ants/ants.cfg``.
You can also edit it using your favorite text editor.

Do not modify the default configuration file as it might be overwritten when updating ANTS.

On Mac OS, you can also configure ANTS with a preference list (plist) or configuration profile.
Please note that configurations set in this manner will override any other configuration, including ``ants.cfg``.

---------------
Run other roles
---------------
Fork or duplicate `our example playbook <https://github.com/ANTS-Framework/playbook>`__
and change the client configuration to point to your repository. 
Update ``main.yml`` to assign different roles to your hosts.

You can use the default Ansible syntax. You can also use wildcards. Have a look at the
`Ansible documentation <http://docs.ansible.com/ansible/latest/playbooks_intro.html>`__

-----------------------------------------
Add ssh authentication to your repository
-----------------------------------------
Ansible-pull can clone a git repository using ssh. You can enable this by creating your own private playbook,
adding ssh authentication and a read only ssh key to the repository.
Configure ANTS to use that key.

By default, ANTS will look for a private key at ``/etc/ants/id_ants``

You can generate a key with ``ssh-keygen -t rsa -b 4096 -N '' -C "ants client" -f /etc/ants/id_ants``

By default, ANTS is configured to run with strict host key checking disabled
and will add the host key for your repo to your ``known_hosts`` file.
You should change this in production. To do so, add ``ssh_stricthostkeychecking = True`` to your ants.cfg

------------------------------
Add a dynamic inventory source
------------------------------
Ansible supports dynamic inventory scripts. (A json representation of hosts to group mappings.)

You can use scripts to tell ansible-pull which tasks to run on which host.
You need an inventory source and a script that can read and return it in the
`correct format: <http://docs.ansible.com/ansible/latest/dev_guide/developing_inventory.html>`__

By default, ANTS will run a dummy script ``inventory_default`` that will just return your hostname belonging to a group
named *ants-common*. You can edit ``main.yml`` straight away and assign roles using host names. But
ANTS shows it's real power when ansible-pull is combined with a dynamic inventory using group mappings.

For this we provide the ``inventory_ad`` script  which will connect to your Active Directory and return all groups your
host is a member of. Just add your configuration to ``/etc/ants/ants.cfg``. Note that read only rights for the
Active Directory user are sufficient.

*Your host DOSN'T have to be bound to Active Directory in order for this to work.*
You can use a placeholder object.

By using a dynamic inventory source, you can assign roles to a host using AD and let ANTS handle the configuration.

--------------------------------
Group Layout in Active Directory
--------------------------------
The groups in Active Directory must have the same names as the mappings and the variables you want to assign
using Ansible. We recommend to keep the groups in a dedicated Organizational Unit to prevent naming collisions.

Nested groups with access restrictions are an easy way to offer rights delegation to other units in your organization.

-------------------
What else do I need
-------------------
Nothing. You just set up a configuration management that communicates savely over ssh using your AD and Github.

No additional infrastructure and no AD binding required.

-------
Testing
-------
You made changes to the ANTS code or you want to test a feature that hasn't been released yet? This is
what you should do:

If what you're looking for is already available in pypi as a pre-release, you can simply install it
by telling pip to include pre-releases in its search: ``pip install ants_client --pre``

If you made local changes to your code and want to test them, you can set up a `virtual environment <https://virtualenv.pypa.io/en/stable/>`__, `activate it <https://virtualenv.pypa.io/en/stable/userguide/#activate-script>`__ and install your code locally using ``pip install -e <path_to_ants>``.

-------------
Communication
-------------
- Please use the `GitHub issue tracker <https://github.com/ANTS-Framework/ants/issues>`__ to file issues.
- Please use a `GitHub Pull-Request <https://github.com/ANTS-Framework/ants/pulls>`__ to suggest changes.

-----------------------------------------------------
Comparison of plain Ansible and Ansible Tower to ANTS
-----------------------------------------------------
****************************************
What does ANTS do, that Ansible can not?
****************************************

- ANTS gives you a set of ready to be used roles for typical macOS and Linux host configurations.
- ANTS let's you utilize Active Directory to map computers to roles. With all it's delegation and nesting features.
- ANTS utilizes Ansible Pull and therefore does not require an active network connection to a central server. Roles will be locally applied even if the host is offline. 

*********************************************************
What does Ansible or Ansible Tower do that ANTS does not?
*********************************************************

- Tower has a nice Dashboard
- Tower has a real time job output and push-button job runs
- Tower can to job scheduling
- Tower supports run-time job promoting
- Tower supports workflows
- Ansbile can use encrypted secrets using Vault
- Ansible and Tower do offer Enterprise Support
