#!/usr/bin/env python3
from rich import print

def print_verbose(data, verbose: bool):
    if verbose:
        print('[bold yellow]Verbose: [/bold yellow]{}'.format(data))
