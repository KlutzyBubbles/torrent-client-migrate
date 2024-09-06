#!/usr/bin/env python3
from typing import Literal

from qbittorrentapi import TorrentDictionary
from transmission_rpc import Torrent

class TorrentInfo:

    save_path: str
    creation_date: int
    completion_date: int | None
    progress: float
    status: Literal['stopped', 'downloading', 'checking', 'seeding', 'unknown']
    hash: str
    name: str
    tags: list[str]

    def from_qbittorrent(self, torrent: TorrentDictionary):
        self.save_path = torrent.save_path
        self.creation_date = torrent.added_on
        self.completion_date = torrent.completion_on
        self.progress = torrent.progress
        self.hash = torrent.hash
        self.name = torrent.name
        temp_status = torrent.state
        if temp_status in ['uploading', 'queuedUP', 'stalledUP', 'checkingUP', 'forcedUP']:
            self.status = 'seeding'
        elif temp_status in ['checkingResumeData', 'checkingDL']:
            self.status = 'checking'
        elif temp_status in ['downloading', 'allocating', 'metaDL', 'queuedDL', 'stalledDL', 'forcedDL']:
            self.status = 'downloading'
        elif temp_status in ['pausedDL', 'pausedUP']:
            self.status = 'stopped'
        else:
            self.status = 'unknown'
        self.tags = torrent.tags.split(',')

    def from_transmission(self, torrent: Torrent):
        self.save_path = torrent.download_dir
        self.creation_date = torrent.added_date
        self.completion_date = torrent.done_date
        self.progress = torrent.percent_done # Could use percent_complete, but done seems more useful
        self.hash = torrent.hash_string
        self.name = torrent.name
        temp_status = torrent.status
        if temp_status in ['seeding', 'seed pending']:
            self.status = 'seeding'
        elif temp_status in ['checking', 'check pending']:
            self.status = 'checking'
        elif temp_status in ['downloading', 'download pending']:
            self.status = 'downloading'
        elif temp_status in ['stopped']:
            self.status = 'stopped'
        else:
            self.status = 'unknown'
        self.tags = torrent.labels
