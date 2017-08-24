A framework to manage and apply macOS and Linux client configurations using Ansible Pull.

The ANTS Framework is developed by the Client Services Team of the `University of Basel <https://www.unibas.ch/>`__ `IT Services <https://its.unibas.ch>`__
and released under the `GNU General Public License Version 3 <https://www.gnu.org/licenses/gpl-3.0.en.html>`__. `Ansible <https://docs.ansible.com/ansible/latest/index.html>`__ is a trademark of `Red Hat, Inc. <https://www.redhat.com>`__

------------
Introduction
------------
The ANTS Framework consists of the following components:

- A wrapper for Ansible-Pull
- An Ansible Dynamic Inventory Script (MS Active Directory Connector)
- A modular collection of roles ready to be used
- Strong logging integration

.. image:: ANTS_Client.svg
   :align: center 

Communication
-------------
- Issues: Please use the `GitHub issue tracker <https://github.com/ANTS-Framework/ants-framework.github.io/issues>`__ to file issues.
- Contributions: Please use a `GitHub Pull-Request <https://github.com/ANTS-Framework/ants-framework.github.io/pulls>`__ to suggest changes.

-----------------------------------------------------
Comparison of plain Ansible and Ansible Tower to ANTS
-----------------------------------------------------

What does ANTS do, that Ansible can not?

- ANTS gives you a set of ready to be used roles for typical macOS and Linux client configurations.
- ANTS let's you utilize Active Directory to map computers to roles. With all its delegation and nesting features.
- ANTS utilizes Ansible Pull and therefore does not require an active network connection to a central server. Roles will be locally applied even if the client is offline. 

What does Ansible or Ansible Tower do that ANTS does not?

- Tower has a nice Dashboard
- Tower has a real time job output and push-button job runs
- Tower can to job scheduling
- Tower supports run-time job promoting
- Tower supports workflows
- Ansbile can use encrypted secrets using Vault
- Ansible and Tower do offer Enterprise Support

------------
Requirements
------------
This project assumes that you are familiar with `Ansible <https://www.ansible.com/>`__
, `Git Submodules <https://git-scm.com/book/en/v2/Git-Tools-Submodules>`__ and the shell.

---------------
Getting started
---------------
#. Make sure GIT and Ansible are installed. If not installed, use your favourite package manager (e.g. pip or yum).
#. Install the ANTS client, open the terminal and start an ANTS run by typing ``ants``.
#. Wait for ANTS to finish, then open another shell. You will see the message of the day.

What happened?
--------------
Executing the installer will install the ANTS client with a default configuration
to ``/usr/local/ants``. It will also add github.com to your root users ``known_hosts`` file and
a launch daemon (macOS)/cron entry (Linux) to run ANTS at a random point in time within
a defined interval (default is 15 minutes).

Running ANTS with the default configuration will use ansible-pull to clone the ANTS playbook from git repository and execute an ansible run.

By default, this will add a message of the day to your macOS or Linux client. Logs of all the runs are stored at ``/var/log/ants``.

----------------------
Where to go from here?
----------------------

Look at the configuration
-------------------------
Run ``ants -h`` to see all command line options or write your own configuration.

The default configuration file is at ``/usr/local/ants/etc/ants.cfg`` but ANTS
will also look for a local configuration file at ``/etc/ants/ants.cfg``.

Do not modify the default configuration file as it might be overwritten when updating ANTS.

Run other roles
---------------
Fork our playbook and change the client configuration to point to your repository. Update ``local.yml`` to assign different roles to your clients.

You can use the default Ansible syntax. You can also use wildcards. Have a look at the
`Ansible documentation <http://docs.ansible.com/ansible/latest/playbooks_intro.html>`__

Add ssh authentication to your repo
-----------------------------------
Create your own private playbook, add a ssh authentication and a read only ssh key to it.
Configure ANTS to use that key.

By default, ANTS will look for a private key at ``/usr/local/ants/etc/id_ants``

You can generate a key with ``ssh-keygen -t rsa -b 4096 -N '' -C "ants client" -f /usr/local/ants/etc/id_ants``

Add a dynamic inventory source
------------------------------
You can use scripts to tell ansible-pull which tasks to run on which client.
You need an inventory source and a script that can read and return it in the
`correct format: <http://docs.ansible.com/ansible/latest/dev_guide/developing_inventory.html>`__

By default, ANTS will run a dummy script that will just return your hostname and localhost belonging to a group
named *ants-common*.

But we also provide ``inventory_ad.py`` which will connect to your Active Directory and return all groups your
host is a member of. Just add your configuration to ``/etc/ants/ants.cfg``. Note that read only rights for the
Active Directory user are sufficient.

By using a dynamic inventory source, you can assign roles using AD and let ANTS handle the configuration.

Group Layout in Active Directory
________________________________
The groups in Active Directory must have the same names as the mappings and the variables you want to assign
using Ansible. We recommend to keep the groups in a dedicated Organizational Unit to prevent naming collisions.

Nested groups with access restrictions are an easy way to offer rights delegation to other units in your organization.

-------------------
What else do I need
-------------------
Nothing. You just set up a configuration management using your AD and Github.

No additional infrastructure required.
