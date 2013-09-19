import os


def get_mroot():
    return os.path.abspath(os.path.dirname(__file__))


def validate_dict(dict, key_list):
    missing_keys = []
    for key in key_list:
        if not key in dict:
            missing_keys.append(key)

    if len(missing_keys) > 0:
        raise ValueError('Invalid arguments, dictionary keys missing: {}'.format(', '.join(missing_keys)))

    return True
