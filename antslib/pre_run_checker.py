"""pre_run_checker
==================
Check different requirements necessary for ants
"""
import os
import subprocess
import sys
import urllib.parse as up

from antslib import logger, configer


def check_git_installed():
    try:
        null = open("/dev/null", "w")
        subprocess.Popen("git", stdout=null, stderr=null)
        null.close()
    except OSError:
        sys.exit("Git is not installed")

    logger.console_logger.info("Git is installed.")


def check_known_host():
    CFG = configer.read_config("main")
    known_hosts_file = CFG["known_hosts_file"]

    if os.path.isfile(known_hosts_file):
        file = open(known_hosts_file, "r")
        git_repo = CFG["git_repository"]
        hostname = (up.urlparse(git_repo)).hostname

        if hostname in file.read():
            logger.console_logger.info(
                f"Hostname {hostname} for git-repository {git_repo} is added in {known_hosts_file}"
            )
        else:
            sys.exit(
                f"Hostname {hostname} for git-repository {git_repo} is not added in {known_hosts_file}"
            )

    else:
        sys.exit(f"Known hosts file {known_hosts_file} does not exists.")


def check_ssh_key():
    pass


def check_run_requirements():
    check_git_installed()
    check_known_host()
    check_ssh_key()


if __name__ == "__main__":
    check_run_requirements()
