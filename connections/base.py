#!/usr/bin/env python3
from abc import abstractmethod
from config.config import Config
from config.connection import ConnectionConfig
from connections.torrent import TorrentInfo

class Connection:

    @abstractmethod
    def __init__(self, connection_config: ConnectionConfig, global_config: Config):
        pass

    @abstractmethod
    def refresh_client(self):
        pass

    @abstractmethod
    def get_torrents(self, only_tags: list[str] = None):
        pass

    @abstractmethod
    def add_torrents(self, torrents: list[TorrentInfo], existing: list[TorrentInfo], source_config: ConnectionConfig):
        pass
