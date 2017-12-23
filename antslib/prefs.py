"""prefs
====================

Handle parsing of configuration preference options.

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
from Foundation import CFPreferencesCopyAppValue
from PyObjCTools import Conversion
# pylint: enable=E0611


BUNDLE_ID = 'com.antsframework.ants'


#####################################################
# prefs functions
#####################################################


def convert_prefs_dict(prefs_dict):
    """Convert Obj-C preference dictionary to Python dictionary.

    Also converts every object in dictionary to a string.
    """
    python_dict = Conversion.pythonCollectionFromPropertyList(prefs_dict)
    for k in python_dict.keys():
        python_dict[k] = str(python_dict[k])
    return python_dict


def merge_prefs(config_dict, prefs_dict):
    """Merge config and prefs dictionaries.

    Overwrites values in config dict if also found in prefs dict.
    """
    for item in config_dict.keys():
        if item in prefs_dict.keys():
            config_dict[item] = prefs_dict[item]
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
    pref_dict = CFPreferencesCopyAppValue(prefs_section, BUNDLE_ID)
    if pref_dict is None:
        pref_dict = {}
    else:
        pref_dict = convert_prefs_dict(pref_dict)
    return pref_dict


if __name__ == '__main__':
    pass
