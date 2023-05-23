# Arena ![GitHub Release Date](https://img.shields.io/github/release-date/jhy354/arena) ![GitHub](https://img.shields.io/github/license/jhy354/arena) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/jhy354/arena) ![GitHub repo file count](https://img.shields.io/github/directory-file-count/jhy354/arena)
<div align="center">
	<img src=https://raw.githubusercontent.com/jhy354/READMEIMAGE/master/Arena/logo.png width=5% />
	<img src=https://raw.githubusercontent.com/jhy354/READMEIMAGE/master/Arena/game_title.png width=17% />
</div>
Arena is a 2D platform LAN game based on pygame and socket

## Language
[简体中文](README.zh_cn.md) | [English](README.md)

## Contents
1. [Requirements](#requirements)
2. [Getting Started](#getting-started)
3. [Build to Binary](#build-to-binary)
4. [Screenshots](#screenshots)
5. [Developing](#developing)
6. [License GPL-3.0](#license-gpl-30)

## Requirements
- python (Tested on 3.6+)
- [pip](https://github.com/pypa/pip)
- [pygame](https://github.com/pygame/pygame)
- [pytmx](https://github.com/bitcraft/pytmx)
- [pyinstaller](https://github.com/pyinstaller/pyinstaller)

## Getting Started

### Preparation

1. Make sure you are running this on Python3.4+
```shell
# check your python version
python --version
```

2. Make sure you already installed following packages in your python environment
```shell
pip install pygame
pip install pytmx
pip install pyinstaller
```

### Run Game

1. Run server
```shell
# usage: python server.py [-a | --address] [-m | --map_index] [-b | background_index]
python server.py -address [SERVER IP]
```

2. Run client
```shell
# usage: python server.py [-a | --address]
python main.py -address [SERVER IP]
```

### Build Project

You can build *Arena* by *`build.py`*
```shell
python build.py
```

## Screenshots
Game Screen:
<div align="center">
<img src=https://raw.githubusercontent.com/jhy354/READMEIMAGE/master/Arena/start_menu.png width=45% />
<img src=https://raw.githubusercontent.com/jhy354/READMEIMAGE/master/Arena/du_dust.png width=45% />
<img src=https://raw.githubusercontent.com/jhy354/READMEIMAGE/master/Arena/du_nefort.png width=45% />
<img src=https://raw.githubusercontent.com/jhy354/READMEIMAGE/master/Arena/du_arena.png width=45% />
</div>

Player:
<div align="center">
<img src=https://raw.githubusercontent.com/jhy354/READMEIMAGE/master/Arena/Player/0.png width=5% />
<img src=https://raw.githubusercontent.com/jhy354/READMEIMAGE/master/Arena/Player/crown.png width=5% />
<img src=https://raw.githubusercontent.com/jhy354/READMEIMAGE/master/Arena/Player/hazmat.png width=5% />
<img src=https://raw.githubusercontent.com/jhy354/READMEIMAGE/master/Arena/Player/knight.png width=5% />
<img src=https://raw.githubusercontent.com/jhy354/READMEIMAGE/master/Arena/Player/ninja.png width=5% />
<img src=https://raw.githubusercontent.com/jhy354/READMEIMAGE/master/Arena/Player/reaper.png width=5% />
<img src=https://raw.githubusercontent.com/jhy354/READMEIMAGE/master/Arena/Player/robe.png width=5% />
<img src=https://raw.githubusercontent.com/jhy354/READMEIMAGE/master/Arena/Player/rogue.png width=5% />
<img src=https://raw.githubusercontent.com/jhy354/READMEIMAGE/master/Arena/Player/soldier.png width=5% />
</div>

## Warning
This project is using *pickle*, so DO NOT run it under public network

## Developing
See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

## License GPL-3.0
Project License can be found [here](LICENSE.md).

---

Made With ❤️ by [jhy354(Romulus)](https://github.com/jhy354/)
