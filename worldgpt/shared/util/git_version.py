

""" Return git related info for the tool to report the current build. """


import subprocess


def get_version():
    return subprocess.getoutput("git describe --long --tags --dirty --abbrev=8")


def get_tag():
    return subprocess.getoutput('git describe --tags')

