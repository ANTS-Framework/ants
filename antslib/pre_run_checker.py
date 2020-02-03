"""pre_run_checker
==================
Check different requirements necessary for ants
"""
import subprocess
import sys

from antslib import logger


def check_git_installed():
    try:
        null = open("/dev/null", "w")
        subprocess.Popen("git", stdout=null, stderr=null)
        null.close()
    except OSError:
        sys.exit("Git is not installed")

    logger.console_logger.info("Git is installed.")


def check_known_host():
    pass


def check_ssh_key():
    pass


def check_run_requirements():
    check_git_installed()
    check_known_host()
    check_ssh_key()


if __name__ == "__main__":
    check_run_requirements()
