"""pre_run_checker
==================
Check different requirements necessary for ants
"""
from __future__ import print_function

import os
import subprocess
import sys
import urllib.parse as up
from distutils.spawn import find_executable

from antslib import logger


def check_git_installed(subprocess_env):
    """
    Checks if the git command can be run.
    """
    path = subprocess_env["PATH"]
    try:
        subprocess.Popen("git", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError:
        sys.exit(
            "CHECK GIT:\t\tNo git executable found in the following path: {path}".format(
                path=path
            )
        )

    git_path = find_executable("git", path=path)
    logger.console_logger.info(
        "CHECK GIT:\t\tWorking git executable found at the following location: {path}.".format(
            path=git_path
        )
    )


def check_known_host(args):
    """
    Reads the used git repository as well as the known hosts file used by ansible.
    The possible known hosts files come from https://github.com/ansible/ansible/blob/8ac0bbcbf60b2874ea1aaa4538389859c028b12c/lib/ansible/module_utils/known_hosts.py#L99-L109
    Afterwards checks if the repository hostname is contained in the known_hosts_file.
    """
    if "USER" in os.environ:
        user_known_host_file = os.path.expandvars("~${USER}/.ssh/known_hosts")
    else:
        user_known_host_file = "~/.ssh/known_hosts"

    known_hosts_file = os.path.expanduser(user_known_host_file)

    possible_files = [
        known_hosts_file,
        "/etc/ssh/ssh_known_hosts",
        "/etc/ssh/ssh_known_hosts2",
        "/etc/openssh/ssh_known_hosts",
    ]

    # Is the host key found in any of the known_host_files
    found = False
    # Does one of the possible known host files exist
    exist = False

    git_repo = args.git_repo
    hostname = (up.urlparse(git_repo)).hostname

    for file in possible_files:
        if os.path.isfile(file):
            exist = True
            file_obj = open(file, "r")

            if hostname in file_obj.read():
                found = True
                found_file = file
                break

    if not exist:
        sys.exit(
            "CHECK KNOWN HOSTS:\tNo possible known hosts file {possible_files} does exist.".format(
                possible_files=possible_files
            )
        )

    if found:
        logger.console_logger.info(
            "CHECK KNOWN HOSTS:\tHostname {hostname} for git-repository {git_repo} is added in {known_hosts}".format(
                hostname=hostname, git_repo=git_repo, known_hosts=found_file
            )
        )
    else:
        sys.exit(
            "CHECK KNOWN HOSTS:\tHostname {hostname} could not be found in: {possible_files}".format(
                hostname=hostname, possible_files=possible_files
            )
        )


def check_ssh_key(args, subprocess_env):
    """
    Checks if a checkout of the playbook repository is possible to validate the ssh-key. If the repository is not
    yet cloned, a clone will be attempted which serves the same purpose.
    """
    if os.path.isdir(args.destination):
        if os.path.isfile(args.ssh_key):
            try:
                checkout_statement = [
                    "git",
                    "-C",
                    args.destination,
                    "checkout",
                    args.branch,
                ]
                proc = subprocess.Popen(
                    checkout_statement,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    env=subprocess_env,
                )
            except OSError:
                logger.console_logger.error(proc.stdout.read())
                logger.console_logger.error(proc.stderr.read())
                sys.exit(
                    "CHECK SSH KEY:\t\tPermissions for git checkout of {repo} at {dest} not sufficient.".format(
                        repo=args.git_repo, dest=args.destination
                    )
                )

            logger.console_logger.info(
                "CHECK SSH KEY:\t\tConnection to playbook repository {repo} at {dest} successful.".format(
                    repo=args.git_repo, dest=args.destination
                )
            )
        else:
            sys.exit("CHECK SSH KEY:\t\tGiven ssh-key does not exist.")
    else:
        try:
            clone_statement = ["git", "clone", args.git_repo, args.destination]
            subprocess.Popen(
                clone_statement, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
        except OSError:
            sys.exit(
                "CHECK SSH KEY:\t\tCould not clone the playbook repository {repo} to {dest}, please check the "
                "permissions.".format(repo=args.git_repo, dest=args.destination)
            )

        logger.console_logger.info(
            "CHECK SSH KEY:\t\tClone of the playbook repository {repo} to {dest} successful.".format(
                repo=args.git_repo, dest=args.destination
            )
        )


def check_run_requirements(args, subprocess_env):
    """
    Takes the ants arguments of the argparser and forwards it to 3 check functions which are then executed.
    """
    check_git_installed(subprocess_env)
    check_known_host(args)
    check_ssh_key(args, subprocess_env)
