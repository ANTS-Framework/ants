"""pre_run_checker
==================
Check different requirements necessary for ants
"""
from __future__ import print_function
import os
import subprocess
import sys
import urllib.parse as up

from antslib import logger


def check_git_installed():
    """
    Checks if the git command can be run.
    """
    try:
        subprocess.Popen(
            "git", bufsize=1, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
    except OSError:
        sys.exit("Git is not installed")

    logger.console_logger.info("Git is installed.")


def check_known_host(args):
    """
    Reads the used git repository as well as the known hosts file from the config.
    Checks if the repository hostname is contained in the known_hosts_file.
    """
    known_hosts_file = args.known_hosts_file

    if os.path.isfile(known_hosts_file):
        file = open(known_hosts_file, "r")
        git_repo = args.git_repo
        hostname = (up.urlparse(git_repo)).hostname

        if hostname in file.read():
            logger.console_logger.info(
                "Hostname {hostname} for git-repository {git_repo} is added in {known_hosts_file}".format(
                    hostname=hostname,
                    git_repo=git_repo,
                    known_hosts_file=known_hosts_file,
                )
            )
        else:
            sys.exit(
                "Hostname {hostname} for git-repository {git_repo} is not added in {known_hosts_file}".format(
                    hostname=hostname,
                    git_repo=git_repo,
                    known_hosts_file=known_hosts_file,
                )
            )

    else:
        sys.exit(
            "Known hosts file {known_hosts_file} does not exists.".format(
                known_hosts_file=known_hosts_file
            )
        )


def check_ssh_key(args):
    if os.path.isdir(args.destination):
        if os.path.isfile(args.ssh_key):
            try:
                pull_statement = [
                    "git",
                    "-C",
                    args.destination,
                    "checkout",
                    args.branch,
                ]
                subprocess.Popen(
                    pull_statement,
                    bufsize=1,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
            except OSError as e:
                sys.exit("Permissions not sufficient.")

            logger.console_logger.info("Connection to playbook successful.")
        else:
            sys.exit("Given ssh-key does not exist.")
    else:
        try:
            clone_statement = ["git", "clone", args.git_repo, args.destination]
            subprocess.Popen(
                clone_statement,
                bufsize=1,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except OSError as e:
            sys.exit(
                "Could not clone the playbook repository, please check the permissions."
            )

        logger.console_logger.info("Clone of the playbook successful.")


def check_run_requirements(args):
    check_git_installed()
    check_known_host(args)
    check_ssh_key(args)
