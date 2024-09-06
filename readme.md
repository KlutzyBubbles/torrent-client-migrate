# Torrent Client Migrate

Migrating from one client to another is a pain, this tool will hopefully make the process bareable.

- [Installation](#installation)
- [Configuration](#configuration)
- [Running](#running)

## Installation

Simply

```sh
git clone https://github.com/KlutzyBubbles/torrent-client-migrate.git
cd torrent-client-migrate
python3 -m pip install -r requirements.txt
python3 tcm
```

## Configuration

On first run, a config file is generated. An example of a full config can be found in `config.ini.example` or looks like

```ini
[global]
skip_check = False
add_paused = True

[node1]
type = qbittorrent
host = 127.0.0.1
port = 8080
username = admin
password = adminadmin

[node2]
type = transmission
protocol = http
host = 127.0.0.1
port = 9091
url_path = /transmission/
torrent_path = ~/.config/transmission-daemon/torrents
save_path = /mnt/files/downloads
```

Sections are used as the key for the connection, with the exception of `global` which is used for regular config options

### Connections

When adding a new connection, this table should help in what options you should use.

- ✔️ means value is required
- ❔ means value is optional
- ❌ means value isnt used

| Option       | Description                                                                        | qBittorrent | Transmission | Defaults to       |
|--------------|------------------------------------------------------------------------------------|-------------|--------------|-------------------|
| type         | transmission or qbittorrent                                                        | ✔️           | ✔️            |                   |
| protocol     | http or https                                                                      | ❔           | ❔            | ''                |
| host         | Hostname or IP of the web client                                                   | ✔️           | ✔️            |                   |
| port         | Port of the web client                                                             | ❔           | ❔            | 80                |
| username     | Username to authenticate with                                                      | ❔           | ❔            | ''                |
| password     | Password to authenticate with                                                      | ❔           | ❔            | ''                |
| url_path     | Additional web path for api (including starting /)                                 | ❌           | ❔            | /transmission/rpc |
| torrent_path | Path to the source torrent files, qbittorrent source exports torrents from web API | ❔           | ✔️            |                   |
| save_path    | Destination save path (must be absolute)                                           | ❔           | ❔            | Source save path  |

## Running

use `python3 tcm migrate [SOURCE] [DESTINATION]` to run, you can also use `--help` on any command to list all the options. Source and destination should match the sections added to the config.

Options for migrate are

- `--filter-tag` `-t`: Filter the source torrents and only migrate the ones that have this supplied tag. Can be used multiple times (`python3 tcm migrate node1 node2 -t tag1 -t tag2`). Only works when the source is qBittorrent
- `--confirm` `-C`: Prompt for confirmation before migrating the torrents, by default it lists how many torrents will be migrated, using in conjunction with `--verbose` will list each torrent name

Global Options:
- `--config` `-c`: Use a config file that isnt in the default location, `--help` will show what is defaults to.
- `--verbose` `-v`: Print more verbose messages usually used for debugging issues.

You can also use `python3 tcm config` to view the loaded config and list its location, this is useful to double check the config is setup corrently.

## Issues

If you have any issues feel free to [create a Github issue](https://github.com/KlutzyBubbles/torrent-client-migrate/issues/new), or even PR. The code is already a bit all over the place so any changes / fixes are always welcome.
