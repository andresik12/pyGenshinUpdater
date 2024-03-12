# pyGenshinUpdater
PC "Genshin Impact" updater, written in Python

Script, that allow to bypass original Genshin impact launcer patching process, in case when you playing on  unsupported platform, like macOS or Linux. 
Allows mannualy specify the path to unpacked patch arhive, even when patch on another drive.

## Requirements:
	1. >=Python3.11
	1. Unziped patch files (you can download zip's manually from mihoyo servers, just google "direct download links for genshin impact")
	2. hpatchz execution file. You can find files here https://github.com/sisong/HDiffPatch/releases. You need to choose zip, depend from your OS (look at file name). This is same program, that mihoyo used in genshin (and in another products, probably), but they pre-compiled it in there execution, so we can't use from game dir.
	3. Make sure, that you have enough free space for patched game, because script can't do it (rn)

## Instruction
	1. Make sure, that python installed. type in cmd or in your terminal "python --version", you should get somthing like that: "Python *.*.*". Make sure version equal or greater that 3.11.0
