==============
ANTS Framework
==============

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
- Make sure ``Git`` is installed on your machine
- Install the latest ants client using pip: ``pip install ants_client``
- Pip will install the ANTS client with a default configuration and put the executable in your path.

******************************************
Installing ants using macOS .pkg installer
******************************************
- Download the latest .pkg installer from the `releases page <https://github.com/ANTS-Framework/ants/releases>`__
- Execute the installer. This will take care of all dependencies
- A launch daemon will be installed, running `ants` every 15 minutes. It will trigger after the next restart.

********
Run ants
********
- Open your terminal
- Start an ANTS run by typing ``ants``.
- Wait for ANTS to finish, then open another shell. You will see the message of the day.

**************
What happened?
**************
Running ANTS with the default configuration will use ansible-pull to clone
`the ANTS playbook <https://github.com/ANTS-Framework/playbook>`__ from a github repository and execute an ansible run.

By default, this will add a message of the day to your macOS or Linux host. Logs of all the runs are stored at ``/var/log/ants``.

----------------------
Where to go from here?
----------------------

-------------------------
Look at the configuration
-------------------------
Run ``ants -h`` to see all command line options or write your own configuration.

Besides the default configuration file in the ants_client package, ANTS
will also look for a local configuration file at ``/etc/ants/ants.cfg``.

Do not modify the default configuration file as it might be overwritten when updating ANTS.

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
Ansible-pull cat clone a git repository using ssh. You can enable this by creating your own private playbook,
adding ssh authentication and a read only ssh key to the repository.
Configure ANTS to use that key.

By default, ANTS will look for a private key at ``/etc/ants/id_ants``

You can generate a key with ``ssh-keygen -t rsa -b 4096 -N '' -C "ants client" -f /etc/ants/id_ants``

By default, ANTS is configured to run with strict host key checking disabled and will add the host key for github.com to your known_hosts file.
You should change this in production. To do so, add ``ssh_stricthostkeychecking = True`` to your ants.cfg

------------------------------
Add a dynamic inventory source
------------------------------
Ansible supports dynamic inventory scripts. (A json representation of hosts to group mappings.)

You can use scripts to tell ansible-pull which tasks to run on which host.
You need an inventory source and a script that can read and return it in the
`correct format: <http://docs.ansible.com/ansible/latest/dev_guide/developing_inventory.html>`__

By default, ANTS will run a dummy script ``inventory_default`` that will just return your hostname belonging to a group
named *ants-common*.

But we also provide ``inventory_ad`` which will connect to your Active Directory and return all groups your
host is a member of. Just add your configuration to ``/etc/ants/ants.cfg``. Note that read only rights for the
Active Directory user are sufficient.

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

No additional infrastructure required.

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
