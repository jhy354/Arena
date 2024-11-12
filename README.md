# Arena ![GitHub Release Date](https://img.shields.io/github/release-date/jhy354/arena) ![GitHub](https://img.shields.io/github/license/jhy354/arena) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/jhy354/arena) ![GitHub repo file count](https://img.shields.io/github/directory-file-count/jhy354/arena)
<div align="center">
	<img src=https://raw.githubusercontent.com/jhy354/READMEIMAGE/master/Arena/logo.png width=5% />
	<img src=https://raw.githubusercontent.com/jhy354/READMEIMAGE/master/Arena/game_title.png width=17% />
</div>
Arena is a 2D platform LAN game based on pygame and socket

## Language💭
[简体中文](README.zh_cn.md) | [English](README.md)

## Contents
1. [Dependencies⚙️](#dependencies)
2. [Getting Started🛠️](#getting-started)
3. [Build the Project💻](#build-the-project)
4. [Game Controls🎮](#game-controls)
5. [Gameplay Screenshots🎞️](#gameplay-screenshots)
6. [Warning⚠️](#warning)
7. [Developing🧩](#developing)
8. [License GPL-3.0📄](#license-gpl-30)

## Dependencies⚙️
- python
- [pip](https://github.com/pypa/pip)
- [pygame](https://github.com/pygame/pygame)
- [pytmx](https://github.com/bitcraft/pytmx)
- [pyinstaller](https://github.com/pyinstaller/pyinstaller)
> [!TIP]
> Tested Environment: 
>     pygame 2.6.0 (SDL 2.28.4, Python 3.12.4)
>     PyTMX 3.32
> and:
>     pygame 2.6.0 (SDL 2.28.4, Python 3.11.1)
>     PyTMX 3.32

> [!NOTE]
> The game has been tested on Python 3.11.x and 3.12.x. Other versions may work, but are not officially supported.
> If you encounter an unsolvable issue, please make sure that your environment matches the one mentioned above.  
> You can also ask questions in the *Issue* section.

## Getting Started🛠️

### Preparation

1. It is recommended to run on Python 3.12 or higher.
```shell
# check your python version
python --version
```

2. Ensure that the following packages are installed in your Python environment
```shell
pip install -r requirements.txt
```
or manually
```shell
pip install pygame~=2.6.0
pip install PyTMX~=3.32
pip install pyinstaller~=6.11.0 
```

### Run Game

1. Run server
```shell
# usage: python server.py [-a | --address] [-m | --map_index] [-b | background_index]
python server.py --address [SERVER IP]
```

2. Run client
```shell
# usage: python server.py [-a | --address]
python main.py --address [SERVER IP]
```

### Build the Project💻

You can build *Arena* by *`build.py`*
```shell
python build.py
```

## Game Controls🎮
- Use **W/A/S/D** or **UP/LEFT/DOWN/RIGHT** to move or attack.

## Gameplay Screenshots🎞️
Game Screen:
<div align="center">
<img src=https://raw.githubusercontent.com/jhy354/READMEIMAGE/master/Arena/start_menu.png width=45% />
<img src=https://raw.githubusercontent.com/jhy354/READMEIMAGE/master/Arena/du_dust.png width=45% />
<img src=https://raw.githubusercontent.com/jhy354/READMEIMAGE/master/Arena/du_nefort.png width=45% />
<img src=https://raw.githubusercontent.com/jhy354/READMEIMAGE/master/Arena/du_arena.png width=45% />
</div>

Player Skins:
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

## Warning⚠️
> [!WARNING]
> This project is currently implemented using *pickle*. Please avoid running it on public networks to prevent potential security risks.

## Developing🧩
> See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

## License GPL-3.0📄
> Project License is available [here](LICENSE.md).

---

> Made With ❤️ by [jhy354](https://github.com/jhy354/)
