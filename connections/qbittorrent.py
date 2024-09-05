from pathlib import Path
from qbittorrentapi import Client
import typer
from config.config import Config
from config.connection import ConnectionConfig
from connections.base import Connection
from rich import print
from rich.progress import track
import os

from connections.torrent import TorrentInfo
from utils import print_verbose

class QbittorrentConnection(Connection):
    
    config: ConnectionConfig
    global_config: Config
    client: Client

    def __init__(self, connection_config: ConnectionConfig, global_config: Config):
        if connection_config.type != 'qbittorrent':
            print('[bold red]Attempting to make a qbittorrent connection with a non qbittorrent type[/bold red]')
            raise typer.Exit()
        self.config = connection_config
        self.global_config = global_config
        self.refresh_client()
    
    def refresh_client(self):
        print_verbose('{}:refresh_client()'.format(self.config.key), self.global_config.verbose)
        host = self.config.host
        if self.config.protocol != '' and self.config.protocol != None:
            host = '{}://{}'.format(self.config.protocol, self.config.host)
        print_verbose('Constructed host: {}'.format(host), self.global_config.verbose)
        try:
            print_verbose('Attempting to connect...', self.global_config.verbose)
            self.client = Client(
                host=host,
                port=self.config.port,
                username=self.config.username,
                password=self.config.password
            )
            self.client.auth_log_in()
        except:
            print('[red]Unable to establish qbittorrent connection to {}[/red]'.format(self.config.key))
            raise typer.Abort()
        print('[yellow]Connected to qBittorrent client keyed: {}[/yellow]'.format(self.config.key))

    def get_torrents(self, only_tags: list[str] = None):
        print_verbose('{}:get_torrents()'.format(self.config.key), self.global_config.verbose)
        qb_torrents = self.client.torrents_info()
        torrents = []
        for torrent in qb_torrents:
            info = TorrentInfo()
            info.from_qbittorrent(torrent)
            if only_tags != None and len(only_tags) > 0:
                contains_tag = False
                for tag in only_tags:
                    if tag in info.tags:
                        contains_tag = True
                        break
                if contains_tag:
                    torrents.append(info)
            else:
                torrents.append(info)
        print('Found {} torrents from qBittorrent'.format(len(torrents)))
        return torrents
    
    def get_torrent_files(self, torrents: list[TorrentInfo]):
        print_verbose('{}:get_torrent_files()'.format(self.config.key), self.global_config.verbose)
        file_info = {}
        for torrent in track(torrents, description='Getting torrent files...'):
            bytes = self.client.torrents_export(torrent.hash)
            file_info[torrent.hash] = bytes
        return file_info


    def add_torrents(self, torrents: list[TorrentInfo], existing: list[TorrentInfo], source_config: ConnectionConfig, source_files = None):
        print_verbose('{}:add_torrents()'.format(self.config.key), self.global_config.verbose)
        existing_hashes = [torrent.hash for torrent in existing]
        use_files = source_files != None and len(source_files) > 0
        for torrent in track(torrents, description='Adding torrents...'):
            if torrent.hash in existing_hashes:
                print_verbose('Torrent {} already exists in qBittorrent, skipping.'.format(torrent.name), self.global_config.verbose)
                continue
            torrent_path = str(Path(source_config.torrent_path).expanduser().joinpath('{}.torrent'.format(torrent.hash)).absolute())
            save_path = torrent.save_path
            if self.config.save_path != '' and self.config.save_path != None:
                save_path = self.config.save_path
            if use_files:
                if torrent.hash in source_files:
                    self.client.torrents_add(
                        torrent_files=source_files[torrent.hash],
                        save_path=save_path,
                        is_skip_checking=self.global_config.skip_check,
                        is_paused=self.global_config.add_paused
                    )
                    print_verbose('Added torrent: {} Path: {}'.format(torrent.name, save_path), self.global_config.verbose)
                else:
                    print('[red]Unable to find torrent file for {} from API[/red]'.format(torrent.name))
            else:
                if os.path.exists(torrent_path):
                    self.client.torrents_add(
                        torrent_files=open(torrent_path, 'rb'),
                        save_path=save_path,
                        is_skip_checking=self.global_config.skip_check,
                        is_paused=self.global_config.add_paused
                    )
                    print_verbose('Added torrent: {} Path: {}'.format(torrent.name, save_path), self.global_config.verbose)
                else:
                    print('[red]Unable to find torrent file for {} at path:[/red] {}'.format(torrent.name, torrent_path))
