#!/usr/bin/python

"""ants
====


Run ansible-pull with a set of defined parameters
and log the content of these runs.
"""

__version__ = '1.0'

__author__ = "Balz Aschwanden"
__email__ = "balz.aschwanden@unibas.ch"
__copyright__ = "Copyright 2017, University of Basel"

__credits__ = ["Balz Aschwanden", "Jan Welker"]
__license__ = "GPL"


import os
import sys
import subprocess
import datetime


from antslib import argparser
from antslib import logger
from antslib import configer

CFG = configer.read_config('main')

ANTS_PATH = os.path.dirname(os.path.realpath(__file__))
DYNAMIC_INVENTORY = os.path.join(ANTS_PATH, CFG['hosts_file'])
DESTINATION = os.path.expanduser(CFG['destination'])


def parse_proc(proc):
    """Read subprocess output and dispatch it to logger.


    Cases handled separately:
        * task_line
            * Line with the name of a task.
            * Printed directly befor the task status.
        * recap_line
            * A single line a the end of an Ansible run.
            * It indicates the number of failes/changed/ok tasks.
            * The line after 'PLAY RECAP' contains the recap
    """
    task_line = None
    recap_line = None
    get_recap = False
    start_run_time = datetime.datetime.now()
    for line in iter(proc.stdout.readline, ''):
        logger.write_log(line, task_line)
        if line.startswith('TASK'):
            task_line = line
        if get_recap:
            recap_line = line
        get_recap = bool(line.startswith('PLAY RECAP'))

    end_run_time = datetime.datetime.now()
    if recap_line is not None:
        logger.log_recap(start_run_time, end_run_time, recap_line)
    return


def run_ansible(args):
    """Run ansible-pull.


    The ansible python api is provided as is and the core team
    reserve the right to push breakting changed.

    Hence, we call the cli directly and do not attempt to work with the api.

    Documentation:
    http://docs.ansible.com/ansible/dev_guide/developing_api.html
    """
    cmd = ['/usr/local/bin/ansible-pull',
           '--clean',
           '-f',
           '-i', args.inventory,
           '-d', args.destination,
           '-U', args.git_repo,
           '-C', args.branch,
           '-e', 'ants__roles_path=%s/roles' % args.destination,
           args.playbook]
    if os.path.isfile(args.ssh_key):
        logger.console_logger.debug("Found ssh key at %s" % args.ssh_key)
        cmd.append('--private-key')
        cmd.append(args.ssh_key)
    else:
        logger.console_logger.debug("No key found at %s" % args.ssh_key)
    if args.verbose:
        logger.console_logger.debug("Running ansible-pull in verbose mode")
        cmd.append('-v')
    if not args.stricthostkeychecking:
        logger.console_logger.debug(
            "Disable strict host key checking for ansible-pull.")
        cmd.append('--accept-host-key')
    if args.wait:
        logger.console_logger.debug(
            "Running ansible-pull with a random wait intervall of %s sec" % CFG['wait_interval'])
        cmd.append('-s')
        cmd.append(CFG['wait_interval'])

    proc = subprocess.Popen(cmd, bufsize=1, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    parse_proc(proc)
    return proc.poll()


def __main__():
    args = argparser.parse_args(__version__, os.path.join(CFG['log_dir'], 'recap.log'),
                                DYNAMIC_INVENTORY, DESTINATION, CFG)
    if args.verbose:
        logger.console_logger.setLevel(logger.logging.DEBUG)
    if not configer.is_root():
        sys.exit('Script must be run as root')
    logger.status_file_rollover()
    run_ansible(args)


if __name__ == "__main__":
    __main__()
