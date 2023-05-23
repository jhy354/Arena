# Arena ![GitHub Release Date](https://img.shields.io/github/release-date/jhy354/arena) ![GitHub](https://img.shields.io/github/license/jhy354/arena) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/jhy354/arena) ![GitHub repo file count](https://img.shields.io/github/directory-file-count/jhy354/arena)
<div align="center">
	<img src=https://raw.githubusercontent.com/jhy354/READMEIMAGE/master/Arena/logo.png width=5% />
	<img src=https://raw.githubusercontent.com/jhy354/READMEIMAGE/master/Arena/game_title.png width=17% />
</div>
Arena是一个基于pygame编写的局域网2D平台类游戏

## 语言
[简体中文](README.zh_cn.md) | [English](README.md)

## 目录
1. [运行环境](#运行环境)
2. [着手开始](#着手开始)
3. [编译](#编译)
4. [项目截图](#项目截图)
5. [参与项目](#参与项目)
6. [License GPL-3.0](#license-gpl-30)

## 运行环境
- python (已在python3.6+中测试运行)
- [pip](https://github.com/pypa/pip)
- [pygame](https://github.com/pygame/pygame)
- [pytmx](https://github.com/bitcraft/pytmx)
- [pyinstaller](https://github.com/pyinstaller/pyinstaller)

## 着手开始

### 准备工作

1. 确保你在 python3.4+ 上运行
```shell
# 检查python版本
python --version
```

2. 确保你已经在环境中安装了以下第三方包
```shell
pip install pygame
pip install pytmx
pip install pyinstaller
```

### 运行游戏

1. 运行服务端
```shell
# usage: python server.py [-a | --address] [-m | --map_index] [-b | background_index]
python server.py -address [服务端IP]
```

2. 运行客户端
```shell
# usage: python server.py [-a | --address]
python main.py -address [服务端IP]
```

### 编译项目

你可以通过 *`build.py`* 编译 *Arena* 
```shell
python build.py
```

## 项目截图
游戏截图:
<div align="center">
<img src=https://raw.githubusercontent.com/jhy354/READMEIMAGE/master/Arena/start_menu.png width=45% />
<img src=https://raw.githubusercontent.com/jhy354/READMEIMAGE/master/Arena/du_dust.png width=45% />
<img src=https://raw.githubusercontent.com/jhy354/READMEIMAGE/master/Arena/du_nefort.png width=45% />
<img src=https://raw.githubusercontent.com/jhy354/READMEIMAGE/master/Arena/du_arena.png width=45% />
</div>

玩家皮肤:
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

## 警告
本项目目前使用 *pickle* 实现, 请不要在公共网络中运行

## 参与项目
参见 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

## License GPL-3.0
项目[开源协议](LICENSE.md).

---

用❤️制作 [jhy354(Romulus)](https://github.com/jhy354/)
