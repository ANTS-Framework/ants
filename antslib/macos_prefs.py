"""macos_prefs
====================

Handle parsing of macOS configuration preference options.

Allows macOS configuration preferences to override
config file options using a plist or configuration
profile for the set BUNDLE_ID.

Preferences can be defined several places. Precedence is:
    - MCX/configuration profile
    - /var/root/Library/Preferences/[BUNDLE_ID].plist
    - /Library/Preferences/[BUNDLE_ID].plist
    - .GlobalPreferences defined at various levels (ByHost, user, system)
"""


# PyLint cannot properly find names inside Cocoa libraries, so issues bogus
# No name 'CFPreferencesCopyAppValue' in module 'Foundation' warnings.
# Disable them.
# pylint: disable=E0611
from builtins import str
from Foundation import CFPreferencesCopyAppValue

# pylint: enable=E0611


BUNDLE_ID = "com.github.ants-framework"


#####################################################
# prefs functions
#####################################################


def convert_dict(nsdict):
    """Generates Python dict of strings from Obj-C NSDict."""
    python_dict = {}
    for k in list(nsdict.keys()):
        python_dict[str(k)] = str(nsdict[k])
    return python_dict


def merge_dicts(config_dict, macos_dict):
    """Merge config and MacOS prefs dictionaries.

    Overwrites values in config dict if also found in prefs dict.
    """
    for item in list(config_dict.keys()):
        if item in list(macos_dict.keys()):
            config_dict[item] = macos_dict[item]
    return config_dict


def read_prefs(prefs_section):
    """Read indicated preferences section and return a dict.

    Uses CFPreferencesCopyAppValue.
    Preferences can be defined several places. Precedence is:
        - MCX/configuration profile
        - /var/root/Library/Preferences/[BUNDLE_ID].plist
        - /Library/Preferences/[BUNDLE_ID].plist
        - .GlobalPreferences defined at various levels (ByHost, user, system)
    """
    macos_dict = CFPreferencesCopyAppValue(prefs_section, BUNDLE_ID)
    if macos_dict is None:
        macos_dict = {}
    else:
        macos_dict = convert_dict(macos_dict)
    return macos_dict


if __name__ == "__main__":
    pass
