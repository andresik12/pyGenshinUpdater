# pyGenshinUpdater
"Genshin Impact" PC version updater, written in Python

Script, that allow to bypass original Genshin impact launcher patching process, in case when you playing on unsupported platform, like macOS or Linux, or you just don't like endless list of electron app on your pc. 
Allows manually specify the path to unpacked patch archive, even when patch folder on another drive.

## Requirements:
`Python 3.11.0` or higher <br />
Download `main.py` from repo <br />
Unzipped patch files. <br />
hpatchz execution file. You can find files on their [GitHub releases page](https://www.github.com/sisong/HDiffPatch/releases/). <br />

Make sure, that you have **enough free space** for patched game, because script can't do it.  <br />

- Where you can download patch zip? You can download zip's manually from mihoyo servers, just google "direct download links for genshin impact".  <br />
	When you will downloading patch's zip's, pay attention to version. Mihoyo writes version in zip file name, like "game_4.0.0_4.1.0_hdiff", where 4.0.0 is version, that you have on your device and 4.1.0 is version, which will be the result of patching process. Usually, they provide for downloading 2 version below. Example: current version 4.3.0 - mihoyo api will provide "game_4.2.0_4.3.0_hdiff" and "game_4.1.0_4.3.0_hdiff", so you can update to current version from 4.2.0 and 4.1.0 etc.

- What is hpatchz? This is same program, that mihoyo used in genshin to create audio banks file (and in another products, probably), but they pre-compiled it in there execution, so we can't use from game dir.  <br />

- Where i need to place unzipped patch files? **Where you want.** I tested it by putting it on an external drive, works flawless. I don't recommend use network folders on Windows, macOS and Linux users can try, but i'm not tested it. <br />

- Where i can find, what version of game installed right now? In "Genshin impact game" folder you have `config.ini` file (open it by text editing tool), that contain `game_version=` line, where number after `=` is version of your game. If you want start game with launcher, you need to edit this number, after patching process, otherwise game launcher will try to update your game<br />



# Instructions

## Windows
Make sure, that python installed. type in cmd `python --version`, you should get something like that: `Python *.*.*`. Make sure version equal or greater that **3.11.0**. <br />
If you don't have installed python, you can download and install from their [official site](https://www.python.org/downloads/). <br />
Place `main.py` in any directory with `Tools` folder, that contain `hpatchz.exe` <br />

Your folder should look like that:
- /your dir
	- main.py
	- /Tools
		- hpatchz.exe <br />

After that, open `cmd` and change your directory by `cd` command to that folder. Try to execute the script by `python main.py`, you should get message with list of commands. To select something - enter function number and press **Enter**. <br />
After selecting function, you will be asked about path to game folder and patch folder. Simply drag and drop folder to `cmd` window and press **Enter**. <br />

## macOS
Make sure, that python installed. type in Terminal (cmd+space, type "terminal" and press enter) `python --version`, you should get something like that: `Python *.*.*`. If you don't have python or version lower, install it via [brew](https://brew.sh/) or from [official site](https://www.python.org/downloads/). <br />
Place `main.py` in any directory with `Tools` folder, that contain `hpatchz`. For the first run, you need to manually execute `hpatchz` by right click (click with two fingers) and press open, otherwise macOS don't allow execute it by security reason. It will launch terminal window and quickly closed by it self - that's fine.<br />

Your folder should look like that:
- /your dir
	- main.py
	- /Tools
		- hpatchz <br />

After that, open `Terminal` and change your directory by `cd` command to that folder. You can type `cd`, press **space** and drop folder, where main.py and Tools/ are located. Try to execute the script by `python main.py`, you should get message with list of commands. To select something - enter function number and press **Enter**. <br />
After selecting function, you will be asked about path to game folder and patch folder. Simply drag and drop folder to `cmd` window and press **Enter**. <br />

## Linux
If you here for instruction, i don't know what to say /kappa/. You can read instruction for macOS, it's pretty much the same.

# Commands

**First command: Old game file cleaning** - execute it first, if you want patch you game. It's take list of files, that can be removed from game patch folder. You need enter path "Genshin impact game" folder and after that path to unzipped patch folder "game_". After execution you will get successful message and question, what do next. Press enter to return to beginning. <br />

**Second command: Game files update** - select once, after successful first command. If you run the command after the first one, you will not be asked about the paths, otherwise, you will need to specify path to "Genshin impact game" folder and patch folder. For example, you can execute first command, close script and open again. <br />

**Third command: Audio localization files update** - updating your localization pack. One pack per execution. At first execution, you will be asked about path to "Genshin impact game" folder and audio patch folder. After path, script will be ask you, what language you want to update. Pay attention, audio path must match with selected language, otherwise it will cause data corruption. Audio patch's will be called by different names: English audio patch will starts by "en-us_", Chinese - "zh-cn_", Japanese - "ja-jp_", Korean - "ko-kr_". If you have more than one sound pack, you need to update each in any order. <br />

After patching, you need manually change version of your game in "Genshin impact game" folder at `config.ini` file. You can do it by any text editing tool. Edit `game_version=` line to patch version.

Tested on:

	macOSx64 13.4.1 with python 3.11.8
	Windows 10 with python 3.11.8
	steamOS 3.5.7 (archlinux) and python 3.11.3