# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import stat

from konlpy_tc import data


def get_datadir():
    for konlpy_tcdir in data.path:
        if (os.path.exists(konlpy_tcdir) and is_writable(konlpy_tcdir)):
            return konlpy_tcdir


def is_writable(path):
    if not os.path.exists(path):
        return False

    # If we're on a posix system, check its permissions.
    if hasattr(os, 'getuid'):
        statdata = os.stat(path)
        perm = stat.S_IMODE(statdata.st_mode)
        # is it world-writable?
        if (perm & 0o002):
            return True
        # do we own it?
        elif statdata.st_uid == os.getuid() and (perm & 0o200):
            return True
        # are we in a group that can write to it?
        elif (statdata.st_gid in [os.getgid()] + os.getgroups()) and (perm & 0o020):
            return True
        # otherwise, we can't write to it.
        else:
            return False
    # Otherwise, we'll assume it's writable.
    return True


def chmod(path):
    os.chmod(path, os.stat(path).st_mode | stat.S_IEXEC)