from pathlib import Path
import typer
from config.config import Config
from config.connection import ConnectionConfig
from connections.base import Connection
from transmission_rpc import Client
from rich import print
from rich.progress import track
import os

from connections.torrent import TorrentInfo
from utils import print_verbose

class TransmissionConnection(Connection):
    
    config: ConnectionConfig
    global_config: Config
    client: Client

    def __init__(self, connection_config: ConnectionConfig, global_config: Config):
        if connection_config.type != 'transmission':
            print('[bold red]Attempting to make a transmission connection with a non transmission type[/bold red]')
            raise typer.Exit()
        self.config = connection_config
        self.global_config = global_config
        self.refresh_client()
    
    def refresh_client(self):
        print_verbose('{}:refresh_client()'.format(self.config.key), self.global_config.verbose)
        try:
            print_verbose('Attempting to connect...', self.global_config.verbose)
            self.client = Client(
                protocol=str(self.config.protocol or 'http'),
                host=self.config.host,
                port=self.config.port,
                username=self.config.username,
                password=self.config.password,
                path=str(self.config.url_path or '/transmission/rpc')
            )
        except:
            print('[red]Unable to establish transmission connection to {}[/red]'.format(self.config.key))
            raise typer.Abort()
        print('[yellow]Connected to transmission client keyed: {}[/yellow]'.format(self.config.key))

    def get_torrents(self, only_tags: list[str] = None):
        print_verbose('{}:get_torrents()'.format(self.config.key), self.global_config.verbose)
        tr_torrents = self.client.get_torrents()
        torrents = []
        for torrent in tr_torrents:
            info = TorrentInfo()
            info.from_transmission(torrent)
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
            torrents.append(info)
        print('Found {} torrents from Transmission'.format(len(torrents)))
        return torrents

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
            print_verbose(torrent.save_path, self.global_config.verbose)
            print_verbose(save_path, self.global_config.verbose)
            if use_files:
                if torrent.hash in source_files:
                    self.client.add_torrent(
                        torrent=source_files[torrent.hash],
                        download_dir=save_path,
                        labels=torrent.tags,
                        paused=self.global_config.add_paused
                    )
                    print_verbose('Added torrent: {} Path: {}'.format(torrent.name, save_path), self.global_config.verbose)
                else:
                    print('[red]Unable to find torrent file for {} from API[/red]'.format(torrent.name))
            else:
                if os.path.exists(torrent_path):
                    self.client.add_torrent(
                        torrent=open(torrent_path, 'rb'),
                        download_dir=save_path,
                        labels=torrent.tags,
                        paused=self.global_config.add_paused
                    )
                    print_verbose('Added torrent: {} Path: {}'.format(torrent.name, save_path), self.global_config.verbose)
                else:
                    print('[red]Unable to find torrent file for {} at path:[/red] {}'.format(torrent.name, torrent_path))
        print_verbose('{}:add_torrents()'.format(self.config.key), self.global_config.verbose)
        #hash_names = {}
        #for torrent in existing:
        #    hash_names[torrent.hash] = torrent.name
        # TODO: Add transmission torrents
        pass
