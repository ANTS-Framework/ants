"""argparser
================

Custom argparse actions and main argparse are
defined here.
"""


import subprocess
import argparse
import os
import sys

from antslib import configer


class InitializeAntsAction(argparse.Action):
    """Prompt user for configuration input and write local config file."""

    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super(InitializeAntsAction,
              self).__init__(option_strings, dest, nargs=0, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        if not configer.is_root():
            sys.exit('Script must be run as root')
        config = configer.get_config()
        configer.write_config(config)
        parser.exit()


class GetStatusAction(argparse.Action):
    """Print ants status to stdout and exit."""

    def __init__(self, option_strings, logfile, dest, nargs=None, **kwargs):
        self.logfile = logfile
        super(GetStatusAction,
              self).__init__(option_strings, dest, nargs=0, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        status = 'failed'
        logfile = self.logfile
        if os.path.isfile(logfile):
            with open(logfile, 'r') as f:
                for line in f:
                    if 'Client status:' in line:
                        status = line.rstrip().split(
                            'Client status:')[1].split()[0]
        print status
        parser.exit()


class GetGroupsAction(argparse.Action):
    """Execute inventory script and exit."""

    def __init__(self, option_strings, inventory_script, dest, nargs=None,
                 **kwargs):
        self.inventory_script = inventory_script
        super(GetGroupsAction, self).__init__(option_strings, dest, nargs=0,
                                              **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        cmd = [self.inventory_script]
        proc = subprocess.Popen(cmd,
                                bufsize=1,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        (out, err) = proc.communicate()
        print out
        parser.exit()


class GetActiveBranchAction(argparse.Action):
    """Print active git brunch to stdout and exit."""

    def __init__(self, option_strings, branch, dest, nargs=None, **kwargs):
        self.branch = branch
        super(GetActiveBranchAction, self).__init__(option_strings, dest,
                                                    nargs=0, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        print 'Branch: %s' % self.branch
        parser.exit()


class GetGitRepoAction(argparse.Action):
    """Print active git repo to stdout and exit."""

    def __init__(self, option_strings, repo, dest, nargs=None, **kwargs):
        self.repo = repo
        super(GetGitRepoAction, self).__init__(option_strings, dest, nargs=0,
                                               **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        print 'Repo: %s' % self.repo
        parser.exit()


class GetPolicyVersionAction(argparse.Action):
    """Print repo version file content and exit."""

    def __init__(self, option_strings, uccm_dir, dest, nargs=None, **kwargs):
        self.uccm_dir = uccm_dir
        super(GetPolicyVersionAction, self).__init__(option_strings, dest,
                                                     nargs=0, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        policy_version_file = os.path.join(self.uccm_dir, 'version')
        version = 'v0.0'
        if os.path.isfile(policy_version_file):
            with open(policy_version_file, 'r') as f:
                version = f.read().rstrip()
        print version
        parser.exit()


def str2bool(v):
    """Make argparse read strings and return bool values.

    Source: https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse
    """
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def parse_args(version, LOG_RECAP, DYNAMIC_INVENTORY, DESTINATION, CFG):
    """Parse and return command line parameters.

    This function relies on the custom actions defined previousely.
    Custom actions will be called if the corresponding argument is
    entered on the command line.
    """
    parser = argparse.ArgumentParser()
    ants_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    # Information
    parser.add_argument('--version', help='Print software version and exit',
                        action='version',
                        version='%(prog)s Version: {version}'.format(version=version))
    parser.add_argument('-s', '--status',
                        help='Print status of last run and exit',
                        action=GetStatusAction, logfile=LOG_RECAP)
    parser.add_argument('-g', '--groups',
                        help='Print group information for this host and exit',
                        action=GetGroupsAction,
                        inventory_script=DYNAMIC_INVENTORY)
    parser.add_argument('-a', '--active_branch',
                        help='Print the active branch name and exit',
                        action=GetActiveBranchAction, branch=CFG['branch'])
    parser.add_argument('-p', '--policy_version',
                        help='Print policy version and exit',
                        action=GetPolicyVersionAction, uccm_dir=DESTINATION)
    parser.add_argument('-r', '--repo',
                        help='Print the active git repo name and exit',
                        action=GetGitRepoAction, repo=CFG['git_repository'])

    # Action
    parser.add_argument('--initialize', help='Write a local configuration for ants. Existing local configuration will be overwritten',
                        action=InitializeAntsAction)
    parser.add_argument('-v', '--verbose',
                        help='Run ansible pull in verbose mode',
                        action='store_true')
    parser.add_argument('-i', '--inventory',
                        help='Add a custom inventory script or file',
                        default=os.path.join(ants_path, CFG['hosts_file']))
    parser.add_argument('-w', '--wait', help='Wait a random interval before starting ansible-pull',
                        action='store_true')
    parser.add_argument('-d', '--destination',
                        help='Set destionation for git checkout',
                        default=DESTINATION)
    parser.add_argument('-b', '--branch', help='Set active branch',
                        default=CFG['branch'])
    parser.add_argument('--git_repo', help='Set git repository',
                        default=CFG['git_repository'])
    parser.add_argument('--ssh_key', help='Path to private key',
                        default=os.path.join(ants_path, 'etc', CFG['ssh_key']))
    parser.add_argument('--playbook', help='Path to playbook file',
                        default=CFG['ansible_playbook'])
    parser.add_argument('--stricthostkeychecking', help='Enable/Disable strict host key checking for ssh.',
                        type=str2bool, default=CFG['ssh_stricthostkeychecking'])
    return parser.parse_args()


if __name__ == '__main__':
    pass
