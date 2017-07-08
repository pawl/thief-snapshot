import os
import shutil

import thief_snapshot


def copy_settings():
    """Copies the example settings from the package to the current directory"""
    new_filename = 'settings.ini'
    if os.path.isfile(new_filename):
        error_msg = '{} already exists'.format(new_filename)
        raise Exception(error_msg)

    # determine the path of the example settings in the package
    pkgdir = os.path.dirname(thief_snapshot.__file__)
    example_ini_path = os.path.join(pkgdir, 'example_settings.ini')

    copy_path = os.path.join(os.getcwd(), new_filename)
    shutil.copy(example_ini_path, copy_path)
