"""argparser
================

Custom argparse actions and main argparse are
defined here.
"""


import argparse
import os
import subprocess
import sys

from antslib import configer


class InitializeAntsAction(argparse.Action):
    """Prompt user for configuration input and write local config file."""

    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super(InitializeAntsAction, self).__init__(
            option_strings, dest, nargs=0, **kwargs
        )

    def __call__(self, parser, namespace, values, option_string=None):
        if not configer.is_root():
            sys.exit("Script must be run as root")
        config = configer.get_config()
        configer.write_config(config)
        parser.exit()


class GetStatusAction(argparse.Action):
    """Print ants status to stdout and exit."""

    def __init__(self, option_strings, logfile, dest, nargs=None, **kwargs):
        self.logfile = logfile
        super(GetStatusAction, self).__init__(option_strings, dest, nargs=0, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        status = "failed"
        logfile = self.logfile
        if os.path.isfile(logfile):
            with open(logfile, "r") as f:
                for line in f:
                    if "Client status:" in line:
                        status = line.rstrip().split("Client status:")[1].split()[0]
        sys.stdout.write("%s\n" % status)
        parser.exit()


class ShowConfigAction(argparse.Action):
    """Print ants configuration to stdout and exit."""

    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super(ShowConfigAction, self).__init__(option_strings, dest, nargs=0, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        if not configer.is_root():
            sys.exit("Script must be run as root")
        cfg_sections = ["main", "ad", "callback_plugins"]
        for section in cfg_sections:
            sys.stdout.write("[%s]\n" % (section))
            c = configer.read_config(section)
            for key in c:
                sys.stdout.write("%s: %s\n" % (key, c[key]))
            sys.stdout.write("\n")
        parser.exit()


class GetGroupsAction(argparse.Action):
    """Execute inventory script and exit."""

    def __init__(self, option_strings, inventory_script, dest, nargs=None, **kwargs):
        self.inventory_script = inventory_script
        super(GetGroupsAction, self).__init__(option_strings, dest, nargs=0, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        cmd = [self.inventory_script]
        proc = subprocess.Popen(
            cmd, bufsize=1, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        (out, err) = proc.communicate()
        sys.stdout.write("%s\n" % out.decode("utf-8"))
        parser.exit()


class GetActiveBranchAction(argparse.Action):
    """Print active git brunch to stdout and exit."""

    def __init__(self, option_strings, branch, dest, nargs=None, **kwargs):
        self.branch = branch
        super(GetActiveBranchAction, self).__init__(
            option_strings, dest, nargs=0, **kwargs
        )

    def __call__(self, parser, namespace, values, option_string=None):
        sys.stdout.write("Branch: %s\n" % self.branch)
        parser.exit()


class GetGitRepoAction(argparse.Action):
    """Print active git repo to stdout and exit."""

    def __init__(self, option_strings, repo, dest, nargs=None, **kwargs):
        self.repo = repo
        super(GetGitRepoAction, self).__init__(option_strings, dest, nargs=0, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        sys.stdout.write("Repo: %s\n" % self.repo)
        parser.exit()


class GetPolicyVersionAction(argparse.Action):
    """Print repo version file content and exit."""

    def __init__(self, option_strings, uccm_dir, dest, nargs=None, **kwargs):
        self.uccm_dir = uccm_dir
        super(GetPolicyVersionAction, self).__init__(
            option_strings, dest, nargs=0, **kwargs
        )

    def __call__(self, parser, namespace, values, option_string=None):
        policy_version_file = os.path.join(self.uccm_dir, "version")
        version = "v0.0"
        if os.path.isfile(policy_version_file):
            with open(policy_version_file, "r") as f:
                version = f.read().rstrip()
        sys.stdout.write("%s\n" % version)
        parser.exit()


def str2bool(v):
    """Make argparse read strings and return bool values.

    Source: https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse
    """
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")


def parse_args(version, LOG_RECAP, DESTINATION, CFG):
    """Parse and return command line parameters.

    This function relies on the custom actions defined previousely.
    Custom actions will be called if the corresponding argument is
    entered on the command line.
    """
    parser = argparse.ArgumentParser()
    _ROOT = os.path.abspath(os.path.dirname(__file__))
    inventory = os.path.join(_ROOT, "inventory", CFG["inventory_script"])
    ansible_callback_plugins = CFG["ansible_callback_plugins"]
    ansible_callback_whitelist = CFG["ansible_callback_whitelist"]

    # Informations
    parser.add_argument(
        "--version",
        help="Print software version and exit",
        action="version",
        version="%(prog)s Version: {version}".format(version=version),
    )
    parser.add_argument(
        "-s",
        "--status",
        help="Print status of last run and exit",
        action=GetStatusAction,
        logfile=LOG_RECAP,
    )
    parser.add_argument(
        "-g",
        "--groups",
        help="Print group information for this host and exit",
        action=GetGroupsAction,
        inventory_script=inventory,
    )
    parser.add_argument(
        "-a",
        "--active_branch",
        help="Print the active branch name and exit",
        action=GetActiveBranchAction,
        branch=CFG["branch"],
    )
    parser.add_argument(
        "-p",
        "--policy_version",
        help="Print policy version and exit",
        action=GetPolicyVersionAction,
        uccm_dir=DESTINATION,
    )
    parser.add_argument(
        "-r",
        "--repo",
        help="Print the active git repo name and exit",
        action=GetGitRepoAction,
        repo=CFG["git_repository"],
    )
    parser.add_argument(
        "--show-config",
        help="Print ants configuration information",
        action=ShowConfigAction,
    )

    # Actions
    parser.add_argument(
        "--initialize",
        help=(
            "Write a local configuration for ants. "
            "Existing local configuration will be overwritten"
        ),
        action=InitializeAntsAction,
    )
    parser.add_argument(
        "--refresh",
        help="Delete the local git repo to force a git clone by ansible-pull.",
        action="store_true",
    )

    # Callback plugin options
    # Doc: https://docs.ansible.com/ansible/latest/reference_appendices/config.html#envvar-ANSIBLE_CALLBACK_PLUGINS
    parser.add_argument(
        "--ansible_callback_plugins",
        help="Colon separated paths in which Ansible will search for Callback Plugins.",
        default=ansible_callback_plugins,
    )
    # Doc: https://docs.ansible.com/ansible/latest/reference_appendices/config.html#envvar-ANSIBLE_CALLBACK_WHITELIST
    parser.add_argument(
        "--ansible_callback_whitelist",
        help="Comma separated list of whitelisted Callback Plugins.",
        default=ansible_callback_whitelist,
    )

    # Options for ansible pull
    parser.add_argument(
        "-v", "--verbose", help="Run ansible pull in verbose mode", action="count"
    )
    parser.add_argument(
        "-q",
        "--quiet",
        help="Quiet mote. Do not print information to console",
        action="store_true",
    )
    parser.add_argument(
        "-i",
        "--inventory",
        help="Path to your dynamic inventory script",
        default=inventory,
    )
    parser.add_argument(
        "-w",
        "--wait",
        help="Wait a random interval before starting ansible-pull",
        action="store_true",
    )
    parser.add_argument(
        "--check",
        help="Do not make any changes but try to predict changes that may occur",
        action="store_true",
    ),
    parser.add_argument(
        "-d",
        "--destination",
        help="Set destionation for git checkout",
        default=DESTINATION,
    )
    parser.add_argument(
        "-b", "--branch", help="Set active branch", default=CFG["branch"]
    )
    parser.add_argument(
        "--git_repo", help="Set git repository", default=CFG["git_repository"]
    )
    parser.add_argument("--ssh_key", help="Path to private key", default=CFG["ssh_key"])
    parser.add_argument(
        "--playbook", help="Path to playbook file", default=CFG["ansible_playbook"]
    )
    parser.add_argument(
        "--stricthostkeychecking",
        help="Enable/Disable strict host key checking for ssh.",
        type=str2bool,
        default=CFG["ssh_stricthostkeychecking"],
    )
    parser.add_argument(
        "--ansible_pull_exe",
        help="Path to the ansible-pull executable",
        default=CFG["ansible_pull_exe"],
    )
    parser.add_argument(
        "--tags",
        help="List of tags to be executed. (Comma separated)",
        default=CFG["tags"],
    )
    parser.add_argument(
        "--skip-tags",
        help="List of tags to be skipped. (Comma separated)",
        default=CFG["skip_tags"],
    )

    # Ansible Python Interpreter
    parser.add_argument(
        "--ansible_python_interpreter",
        help="Specifies a specific python interpreter. Overwrites the config value",
        default=CFG["ansible_python_interpreter"]
    )

    # Parse arguments
    return parser.parse_args()


if __name__ == "__main__":
    pass
