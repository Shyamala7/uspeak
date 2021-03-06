#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess


def set_volume(delta, *args):
    if delta:
        return subprocess.call('amixer -D pulse set Master 1+ {}'.format(delta), shell=True)
    return 1


def is_muted():
    try:
        return subprocess.check_output(
            'amixer -D pulse sget Master 1+ | egrep -c -m 1 "\[off\]"', shell=True
        ).strip() == b'1'
    except:
        return False


def get_volume():
    try:
        return int(subprocess.check_output(
            'amixer -D pulse sget Master 1+ | grep -oiP -m 1 "Front .*\[\K[0-9]+"', shell=True
        ).strip())
    except:
        return None


class reduced_volume():
    def __init__(self):
        self.was_muted = False
        self.initial_volume = 100
        self.reduction_level = 2

    def __enter__(self, factor=None):
        if is_muted():
            self.was_muted = True
        else:
            self.initial_volume = get_volume()
            self.reduction_level = factor or self.reduction_level
            if self.initial_volume:
                set_volume('{}%'.format(self.initial_volume // self.reduction_level))

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.was_muted:
            return
        set_volume('{}%'.format(self.initial_volume))


command_to_method = {
    'volume': set_volume,
    'next': lambda *args: subprocess.call("xte 'key XF86AudioNext'", shell=True),
    'prev': lambda *args: subprocess.call("xte 'key XF86AudioPrev'", shell=True),
    'pause': lambda *args: subprocess.call("xte 'key XF86AudioPlay'", shell=True),
}


def run(*args, **kwargs):
    try:
        media_action = command_to_method.get(args[0])
        return media_action(*args[1:])
    except IndexError:
        return 1
