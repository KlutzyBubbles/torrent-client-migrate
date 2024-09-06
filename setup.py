#!/usr/bin/env python3
from setuptools import setup

import re
VERSIONFILE="_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

setup(
    name = "torrent-client-migrate",
    description = "Migrate torrents from one client to another.",
    version = verstr,
    url = 'https://github.com/KlutzyBubbles/torrent-client-migrate',
    py_modules = [
        '_version',
        'utils',
        'config.config',
        'config.connection',
        'connections.base',
        'connections.qbittorrent',
        'connections.torrent',
        'connections.transmission'
    ],
    scripts = ['tcm'],
    install_requires = [
        'qbittorrent-api~=2024.8.65',
        'transmission-rpc~=7.0.11',
        'typer~=0.12.5',
        'packaging>=24.1'
    ]
)