"""configer
====================

Handle parsing of configuraiton file options.
"""
from __future__ import print_function


from future import standard_library

standard_library.install_aliases()
from builtins import input
import configparser
import os
import re

try:
    from antslib import macos_prefs

    use_macos_prefs = True
except ImportError:
    use_macos_prefs = False

_ROOT = os.path.abspath(os.path.dirname(__file__))


def is_root():
    """Check if user is root and return True or False."""
    if os.geteuid() == 0:
        return True
    return False


def create_dir(dir_name):
    """Create directory"""
    uid = os.getuid()
    gid = os.getgid()
    os.mkdir(dir_name, 0o755)
    os.chown(dir_name, uid, gid)


def read_config(config_section, config_file="ants.cfg"):
    """Read indicated configuraton section and return a dict.

    Uses config.optionxform to preserver upper/lower case letters
    in config file.
    """

    default_config = os.path.join(_ROOT, "etc", config_file)
    config_path = "/etc/ants/"
    system_config = os.path.join(config_path, config_file)

    if not os.path.isfile(default_config):
        raise OSError("Default config file not found at %s" % default_config)

    config = configparser.ConfigParser()
    config.optionxform = str
    try:
        config.read([default_config, system_config])
    except configparser.MissingSectionHeaderError as xxx_todo_changeme:
        configparser.ParsingError = xxx_todo_changeme
        print("Error while reading configuration from %s." % system_config)
        print("Ignoring system configuraiton")
        config.read([default_config])

    config_dict = dict(config.items(config_section))

    if use_macos_prefs:
        macos_dict = macos_prefs.read_prefs(config_section)
        config_dict = macos_prefs.merge_dicts(config_dict, macos_dict)

    # Add base search path to config
    # This is done to allow for easy append of custom paths while keeping the
    # default search path as well
    if config_section == "main":
        config_dict["ansible_callback_plugins_base_path"] = os.path.join(
            os.path.join(_ROOT, "plugins", "callback")
        )

    return config_dict


def get_values(cfg, section_name):
    """Take and return a dict of values and prompt the user for a reply."""
    msg = "Configuration for section: %s" % section_name
    print("%s" % re.sub(r"[a-zA-Z :]", "#", msg))
    print("%s" % msg)
    print("%s" % re.sub(r"[a-zA-Z :]", "#", msg))
    for key, value in cfg.items():
        cfg[key] = input("%s [Example: %s]:" % (key, value)) or value
    return cfg


def get_config():
    """Get configuration from command line and return ConfigParser opject

    If no value is specified by the user, the value marked as *example*
    will be written set.

    Only values that differ from the system defaults are written to
    the local config file.
    """
    cfg_main = get_values(read_config("main"), "main")
    cfg_ad = None
    cfg_callback_plugins = None
    if cfg_main["inventory_script"] == "inventory_ad":
        cfg_ad = get_values(read_config("ad"), "ad")
    if cfg_main["ansible_callback_whitelist"]:
        cfg_callback_plugins = get_values(
            read_config("callback_plugins"), "callback_plugins"
        )

    config = configparser.ConfigParser()
    config.add_section("main")
    for key, value in cfg_main.items():
        config.set("main", key, value)
    if cfg_ad:
        config.add_section("ad")
        for key, value in cfg_ad.items():
            config.set("ad", key, value)
    if cfg_callback_plugins:
        config.add_section("callback_plugins")
        for key, value in cfg_ad.items():
            config.set("callback_plugins", key, value)
    return config


def write_config(config, config_file="ants.cfg"):
    """Writing ConfigParser object to local configuration.
    Existing files will be overwritten."""
    config_path = "/etc/ants/"
    system_config = os.path.join(config_path, config_file)
    if not os.path.isdir(config_path):
        create_dir(config_path)
    with open(system_config, "w") as cfg:
        config.write(cfg)


if __name__ == "__main__":
    pass
