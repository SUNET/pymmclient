"""
This module provide utility functions.
"""

import os


def get_mroot():
    """
    Get absolute path for myself.
    """
    return os.path.abspath(os.path.dirname(__file__))


def validate_dict(my_dict, key_list):
    """
    Function to quickly validate that the provided dict contain all necessary keys.
    """
    missing_keys = []
    for key in key_list:
        if not key in my_dict:
            missing_keys.append(key)

    if len(missing_keys) > 0:
        raise ValueError('Invalid arguments, dictionary keys missing: {}'.format(', '.join(missing_keys)))

    return True
