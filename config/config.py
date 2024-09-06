#!/usr/bin/env python3
import configparser
import os
import typer
from typing import Dict
from config.connection import ConnectionConfig
from rich import print

from utils import print_verbose

class Config:

    skip_check: bool = False
    add_paused: bool = True
    verbose: bool = False
    connections: Dict[str, ConnectionConfig] = {}
    path: str = ''

    def __init__(self, path: str, verbose: bool):
        self.path = path
        self.verbose = verbose
        self.load(True)

    def load(self, create_default = False):
        print_verbose('Config.load({})'.format(create_default), self.verbose)
        config = configparser.ConfigParser(interpolation=None)
        try:
            print_verbose('Reading config', self.verbose)
            open(self.path)
            config.read(self.path)
        except:
            if create_default:
                self.save()
                print("Please edit the configuration file: {0}".format(self.path))
            else:
                print("Cannot find config at: {0}".format(self.path))
            raise typer.Exit(code=1)
        finally:
            print_verbose('Loading config', self.verbose)
            sections = config.sections()
            for section in sections:
                print_verbose('Loading {} section'.format(section), self.verbose)
                if section == 'global':
                    try:
                        self.skip_check = config.getboolean(section, 'skip_check', fallback=False)
                        self.add_paused = config.getboolean(section, 'add_paused', fallback=True)
                    except:
                        print('[red]Global options could not be loaded[/red]')
                        continue_default = typer.confirm('Do you want to continue with defaults')
                        if continue_default:
                            self.skip_check = False
                            self.add_paused = True
                            self.verbose = False
                        else:
                            raise typer.Exit()
                else:
                    temp = ConnectionConfig(section)
                    temp.load(config)
                    self.connections[section] = temp
    
    def save(self):
        print_verbose('Config.save()', self.verbose)
        config = configparser.ConfigParser(interpolation=None)
        if not os.path.exists(os.path.dirname(self.path)):
            print_verbose('Creating directory(s)', self.verbose)
            os.makedirs(os.path.dirname(self.path))
        config.add_section('global')
        config.set('global', 'skip_check', "{}".format(self.skip_check))
        config.set('global', 'add_paused', "{}".format(self.add_paused))
        for key in self.connections:
            config.add_section(key)
            config.set(key, 'protocol', self.connections[key].protocol)
            config.set(key, 'host', self.connections[key].host)
            config.set(key, 'port', self.connections[key].port)
            config.set(key, 'username', self.connections[key].username)
            config.set(key, 'password', self.connections[key].password)
            config.set(key, 'url_path', self.connections[key].url_path)
            config.set(key, 'torrent_path', self.connections[key].torrent_path)
        print_verbose('Writing config to file', self.verbose)
        config.write(open(self.path, 'w'))
    
    def print_config(self):
        print('[bold yellow]Config Path:[/bold yellow] {}'.format(self.path))
        print('[bold]Global Config:[/bold]')
        print({
            'skip_check': self.skip_check,
            'add_paused': self.add_paused,
            'verbose': self.verbose
        })
        print('[bold]Connections:[/bold]')
        for key in self.connections:
            self.connections[key].print_config()
