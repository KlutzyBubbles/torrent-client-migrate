import configparser
from typing import Literal
from rich import print
import typer

supported_types = ['qbittorrent', 'transmission']
supported_protocols = ['http', 'https', '']

class ConnectionConfig:

    protocol: Literal['http', 'https', ''] = ''
    host: str = ''
    port: str = '80'
    username: str = None
    password: str = None
    url_path: str = ''
    torrent_path: str = ''
    save_path: str = ''
    type: str = ''
    key: str = ''

    def __init__(self, key: str):
        self.key = key

    def load(self, config: configparser.ConfigParser):
        self.protocol = config.get(self.key, 'protocol', fallback='').lower()
        self.host = config.get(self.key, 'host', fallback='')
        self.port = config.get(self.key, 'port', fallback='80')
        self.username = config.get(self.key, 'username', fallback=None)
        self.password = config.get(self.key, 'password', fallback=None)
        self.url_path = config.get(self.key, 'url_path', fallback='')
        self.torrent_path = config.get(self.key, 'torrent_path', fallback='')
        self.save_path = config.get(self.key, 'save_path', fallback='')
        self.type = config.get(self.key, 'type', fallback='').lower()
        if self.type not in supported_types:
            self.print_invalid('connection type', self.type, supported_types)
            raise typer.Exit()
        if self.protocol not in supported_protocols:
            self.print_invalid('protocol', self.protocol, supported_protocols)
            raise typer.Exit()
        Literal['http', 'https']
    
    def print_invalid(
            self,
            option: str,
            value: str,
            supported: list):
        print('[bold red]Value \'{}\' is an unknown {} on key {} (currently supports {})[/bold red]'
              .format(value, option, self.key, ', '.join(supported)))

    def print_config(self):
        print('[bold yellow]{}:[/bold yellow]'.format(self.key))
        print({
            'type': self.type,
            'protocol': self.protocol,
            'host': self.host,
            'port': self.port,
            'username': self.username,
            'password': self.password,
            'url_path': self.url_path,
            'torrent_path': self.torrent_path,
            'save_path': self.save_path
        })
