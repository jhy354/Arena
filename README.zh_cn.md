# Arena ![GitHub Release Date](https://img.shields.io/github/release-date/jhy354/arena) ![GitHub](https://img.shields.io/github/license/jhy354/arena) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/jhy354/arena) ![GitHub repo file count](https://img.shields.io/github/directory-file-count/jhy354/arena)
<div align="center">
	<img src=https://raw.githubusercontent.com/jhy354/READMEIMAGE/master/Arena/logo.png width=5% />
	<img src=https://raw.githubusercontent.com/jhy354/READMEIMAGE/master/Arena/game_title.png width=17% />
</div>
Arena是一个基于pygame编写的局域网2D平台类游戏

## 语言💭
[简体中文](README.zh_cn.md) | [English](README.md)

## 目录
1. [运行环境⚙️](#运行环境)
2. [着手开始🛠️](#着手开始)
3. [编译💻](#编译项目)
4. [游戏控制🎮](#游戏控制)
5. [项目截图🎞️](#项目截图)
6. [警告⚠️](#警告)
7. [参与项目🧩](#参与项目)
8. [License GPL-3.0📄](#license-gpl-30)

## 运行环境⚙️
- python
- [pip](https://github.com/pypa/pip)
- [pygame](https://github.com/pygame/pygame)
- [pytmx](https://github.com/bitcraft/pytmx)
- [pyinstaller](https://github.com/pyinstaller/pyinstaller)
> [!TIP]
> 经过测试的运行环境:
>     pygame 2.6.0 (SDL 2.28.4, Python 3.12.4)
>     PyTMX 3.32
> 以及:
>     pygame 2.6.0 (SDL 2.28.4, Python 3.11.1)
>     PyTMX 3.32
> [!NOTE]
> 该游戏已在 Python 3.11.x 和 3.12.x 上进行过测试。其他版本可能能正常运行, 但不作官方支持。
> 如果遇到无法解决的问题, 请确保运行环境与以上环境一致
> 你也可以在*Issue*中提问

## 着手开始🛠️

### 准备工作

1. 建议在 ~~~~Python3.12 及以上版本中运行
```shell
# 检查python版本
python --version
```

2. 确保你已经在环境中安装了以下第三方包
```shell
pip install -r requirements.txt
```
或者手动安装
```shell
pip install pygame~=2.6.0
pip install PyTMX~=3.32
pip install pyinstaller~=6.11.0 

### 运行游戏

1. 运行服务端
```shell
# usage: python server.py [-a | --address] [-m | --map_index] [-b | background_index]
python server.py --address [服务端IP]
```

2. 运行客户端
```shell
# usage: python server.py [-a | --address]
python main.py --address [服务端IP]
```

### 编译项目💻

你可以通过 *`build.py`* 编译 *Arena* 
```shell
python build.py
```

## 游戏控制🎮
- 使用 W/A/S/D 或 上下左右箭头键 来移动或攻击。

## 项目截图🎞️
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

## 警告⚠️
> [!WARNING]
> 本项目目前使用 *pickle* 实现, 请不要在公共网络中运行, 以防遭受网络攻击

## 参与项目🧩
> 参见 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

## License GPL-3.0📄
> 项目[开源协议](LICENSE.md).

---

> 用❤️制作 [jhy354(Romulus)](https://github.com/jhy354/)
