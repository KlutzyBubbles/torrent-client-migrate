import typer

from config.config import Config
from connections.qbittorrent import QbittorrentConnection
from connections.transmission import TransmissionConnection

def get_connection(connection_config, config: Config):
    if connection_config.type == 'qbittorrent':
        return QbittorrentConnection(connection_config, config)
    elif connection_config.type == 'transmission':
        return TransmissionConnection(connection_config, config)
    else:
        print('[red]Attempted to connect to unknown connection type: {}[/red]'.format(connection_config.type))
        raise typer.Exit()