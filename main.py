import os
import sys
import json
import shutil
import subprocess
import hashlib
from pathlib import Path

TOOLS_DIR = "./Tools"
DIR_GAME_ROOT_PATH = ""
DIR_GAME_AUDIOASSETS = "GenshinImpact_Data/StreamingAssets/AudioAssets"
DIR_GAME_FILES_UPDATE = ""
DIR_AUDIO_LOCALIZATION_FILES_UPDATE = ""
LANG_DICTIONARY=["English(US)", "Japanese", "Chinese", "Korean"]
EXEC_EXTENTION = ""
DIR_SLASH = "/"
if os.name == 'nt':
	EXEC_EXTENTION = ".exe"
	DIR_SLASH = "\\"

# Searching for files, that will be modified
# optimization auido list for prevent checking checksum of files, that not be modified
def dir_scan(root_dir: Path):
	file_list = []
	for (dirpath, dirnames, filenames) in os.walk(root_dir):
			for f in filenames:
				if not f[0] == '.':
					file_list.append(os.path.join(dirpath, f))
	return file_list

def file_replace(src_path: Path, dst_path: Path):
	os.makedirs(os.path.dirname(dst_path), exist_ok=True)
	shutil.copy(src_path, dst_path)
	os.remove(src_path)

def audio_file_finder(hdiff_audio: list, audio_checksum: list):
	audio_list: list[dict] = []
	for hdiff_file in hdiff_audio:
		hdiff_file_stem = Path(hdiff_file).stem
		for checksum in audio_checksum:
			if checksum['FileName'] == hdiff_file_stem:
				audio_list.append(checksum)
			#TODO What happend if audio pck file wouldn't exist, but hdiff will be?
	return audio_list

# Opening checksum file and returning list of dict
# filled by file name and md5 checksum
def reading_and_formating_checksum_file(checksum_file_path: Path):
	checksum_list: list[dict]= []
	with open(checksum_file_path, "r") as audio_checksum_file:
		while True:
			line = audio_checksum_file.readline().strip()
			if not line:
				break
			line_to_dict = json.loads(line)
			checksum_list.append({'FileName': os.path.basename(line_to_dict['remoteName']), 'md5': line_to_dict['md5']})
	return checksum_list

# Returning list, that containt filtered checksum list by suffix
def checksum_files_filter(raw_checksum_list: list, suff: str):
	checksum_list: list[dict] = []
	checksum_list = list(filter(lambda name: Path(name['FileName']).suffix == suff, raw_checksum_list))
	return checksum_list

def files_checksum_checker(checksum_to_compare: str, file_path: Path):
	file_info = os.path.split(file_path)
	with open(file_path, 'rb') as file_to_check:
		data = file_to_check.read()
		calculated_md5 = hashlib.md5(data).hexdigest()
	if calculated_md5 == checksum_to_compare:
		print('Checksum of', file_info[1], 'valid', sep=" ")
		return True
	else:
		print('Somthing wrong with', file_info[1], 'at', file_info[0], sep=" ")
		return False

def audio_files_checksum_processing(hdiff_files_list: list, checksum_list: list, path_audio: Path):
	files_list_for_patching = audio_file_finder(hdiff_files_list, checksum_list)
	for file in files_list_for_patching:
		#if checksum failed, give a choice to abort execution or continue with corrupted file
		if not files_checksum_checker(file['md5'], Path.joinpath(path_audio, file['FileName'])):
			print('Checksum of', file['FileName'], "didn't match \n")
			print('Continuation may cause corruption and you will have to download the full audio archive')
			answer = input('Continue? Enter "no" if you want to abort: ')
			if answer[0].lower() == 'n':
				sys.exit(1)

def audio_assets_patching(original_files_dir: Path, patch_files_dir: Path, patch_dir: Path, file_list: list, checksum_list: list[dict]):
	temp_folder_dir = Path.joinpath(Path(DIR_GAME_ROOT_PATH), "tempFolder")
	if Path(temp_folder_dir).is_dir():
		shutil.rmtree(temp_folder_dir)		
	os.mkdir(temp_folder_dir)
	hpatch_exec = Path.joinpath(Path(TOOLS_DIR).resolve(), "hpatchz" + EXEC_EXTENTION) #add executable extension for NT
	patch_dir_abs = Path.joinpath(patch_files_dir, patch_dir)
	for file_name in file_list:
		# Get original file name without .hdiff extension
		file_name_stem = Path(file_name).stem
		# Searching for checksum of .pck file
		checksum_pck = next(checksum for checksum in checksum_list if checksum['FileName'] == file_name_stem)
		path_of_patched_pck = Path.joinpath(temp_folder_dir, file_name_stem)
		subprocess.call([hpatch_exec, Path.joinpath(original_files_dir, file_name_stem), Path.joinpath(patch_dir_abs, file_name), path_of_patched_pck])
		#check for hpatch create patched pck
		if path_of_patched_pck.exists():
			print(str(file_name_stem), "patched, checking cheksum..", sep=" ")
			#checking checksum before replacing OG file
			if files_checksum_checker(checksum_pck['md5'], path_of_patched_pck):
				print("Replaceing old pck by patched pck..")
				#replace old audio pck with patched pck
				file_replace(Path.joinpath(temp_folder_dir, file_name_stem), Path.joinpath(original_files_dir, file_name_stem))
				print("Deleting hdiff ", file_name)
				os.remove(Path.joinpath(patch_dir_abs, file_name))
	patch_dir_abs.rmdir()

def audio_localization_package_updater(path_game_root: Path, path_update_root: Path):
	print('Select audio pack, that you want to update (1 per execution)')
	lang_id = int(input('1: English\n2: Japanese\n3: Chinese\n4: Korean\nEnter a number: '))
	path_game_localization_files = Path.joinpath(path_game_root, DIR_GAME_AUDIOASSETS, LANG_DICTIONARY[lang_id - 1])

	# Check for folder exist and permission granted
	if not os.path.exists(path_game_localization_files):
		print("Selected language directory doesn't exist or permission not granted")
		sys.exit(1)
	
	#prepare for checking checksum
	checksum_file_name = "Audio_" + LANG_DICTIONARY[lang_id - 1] + "_pkg_version"
	checksum_list_original = reading_and_formating_checksum_file(Path.joinpath(path_game_root, checksum_file_name))
	checksum_list_patched = reading_and_formating_checksum_file(Path.joinpath(path_update_root, checksum_file_name))
	path_audio_hdiff = Path.joinpath(Path(DIR_GAME_AUDIOASSETS), LANG_DICTIONARY[lang_id - 1])
    # Get .hdiff files list at localization update folder
	file_list = []
	for (dirpath, dirnames, filenames) in os.walk(Path.joinpath(path_update_root, path_audio_hdiff)):
		for f in filenames:
				#filter for hidden files
				if not f[0] == '.':
					file_list.append(f)
		break
	hdiff_files_list = list(filter(lambda name: Path(name).suffix == ".hdiff", file_list)) # List of hdiff files in present folder
	pck_files_list = list(filter(lambda name: Path(name).suffix == ".pck", file_list)) # List of pck files in preset folder
	#moving new audio file to their folder
	if len(pck_files_list) > 0:
		for file in pck_files_list:
			file_replace(Path.joinpath(path_update_root, path_audio_hdiff, file), Path.joinpath(path_game_localization_files, file))
	#checksum of existing pck processing
	if len(hdiff_files_list) > 0:
		#check OG audio files before patching
		audio_files_checksum_processing(hdiff_files_list, checksum_list_original, path_game_localization_files)
	audio_assets_patching(path_game_localization_files, path_update_root, path_audio_hdiff, hdiff_files_list, checksum_list_patched)
	file_replace(Path.joinpath(path_update_root, checksum_file_name), Path.joinpath(path_game_root, checksum_file_name))
	print('Audio localization', LANG_DICTIONARY[lang_id - 1], 'has updated', sep=' ')
	ending_question()	

def game_audio_updater(path_game_root: Path, path_update_root: Path):
	print("Updating game audio files")
	path_checksum_file_current = Path.joinpath(path_game_root, "pkg_version")
	path_checksum_file_new = Path.joinpath(path_update_root, "pkg_version")
	path_game_audioassets = Path.joinpath(path_game_root, DIR_GAME_AUDIOASSETS)
	path_update_audioassets = Path.joinpath(path_update_root, DIR_GAME_AUDIOASSETS)
	checksum_list_original = checksum_files_filter(reading_and_formating_checksum_file(path_checksum_file_current), ".pck")
	checksum_list_patched = checksum_files_filter(reading_and_formating_checksum_file(path_checksum_file_new), ".pck")
	os.remove(Path.joinpath(path_update_root, 'hdifffiles.txt'))
	file_list = []
	for (dirpath, dirnames, filenames) in os.walk(path_update_audioassets):
		for f in filenames:
			if not f[0] == '.':
				file_list.append(f)
		break
	hdiff_files_list = list(filter(lambda name: Path(name).suffix == ".hdiff", file_list)) 	# List of hdiff files in present folder
	pck_files_list = list(filter(lambda name: Path(name).suffix == ".pck", file_list)) 		# List of pck files in preset folder
	#moving new audio file to their folder
	if len(pck_files_list) > 0:
		for file in pck_files_list:
			file_replace(Path.joinpath(path_update_audioassets, file), Path.joinpath(path_game_audioassets, file))
	if len(hdiff_files_list) > 0:
		#check OG audio files before patching
		audio_files_checksum_processing(hdiff_files_list, checksum_list_original, path_game_audioassets)
	audio_assets_patching(path_game_audioassets, path_update_root, Path(DIR_GAME_AUDIOASSETS), hdiff_files_list, checksum_list_patched)
	print('Game audio files updated')
	
def game_files_updater(path_game_root: Path, path_update_root: Path):
	print('Game files updating')
	for full_path in dir_scan(path_update_root):
		print('Moving', os.path.basename(full_path))
		file_replace(Path(full_path), Path.joinpath(path_game_root, full_path.replace(str(path_update_root) + DIR_SLASH, '')))
	print('Game files updated')
	ending_question()

def dir_Selector(case_type: int):
	global DIR_GAME_FILES_UPDATE 
	global DIR_GAME_ROOT_PATH
	global DIR_AUDIO_LOCALIZATION_FILES_UPDATE

	def path_corrector(path_string:str):
		if path_string[0] == '"':
			path_string = path_string.replace('"', '')
		if path_string[0] == "'":
			path_string = path_string.replace("'", '')
		if path_string[len(path_string) - 1] == ' ':
			path_string = path_string[:-1]
		if os.name == 'posix':
			path_string = path_string.replace('\\', '')
		return path_string

	if len(DIR_GAME_ROOT_PATH) < 1:
		DIR_GAME_ROOT_PATH = input('Enter path to "Genshin impact game" directory. Example: "D:/games/genshin impact game" \n')
		DIR_GAME_ROOT_PATH = path_corrector(DIR_GAME_ROOT_PATH)
	match case_type:
		case 0:
			DIR_GAME_FILES_UPDATE = input('Enter path of directory with game update files. Should starts "game_4.4.0_4.5.0" \n')
			DIR_GAME_FILES_UPDATE = path_corrector(DIR_GAME_FILES_UPDATE)
		case 1:
			DIR_AUDIO_LOCALIZATION_FILES_UPDATE = input('Enter path of directory with audio localization update. Should starts like "en-us_4.4.0_4.5.0" \n')
			DIR_AUDIO_LOCALIZATION_FILES_UPDATE = path_corrector(DIR_AUDIO_LOCALIZATION_FILES_UPDATE)
		case _:
			return 0

def old_files_cleaning(game_root: Path, patch_root: Path):
	with open(Path.joinpath(patch_root, 'deletefiles.txt')) as f:
		content = list(filter(None, f.read().split('\n')))
		for file_path in content:
			os.remove(Path.joinpath(game_root, file_path))
			print("%s has been removed successfully" %file_path)
	print('Removing old files finished')
	os.remove(Path.joinpath(patch_root, 'deletefiles.txt'))
	ending_question()

def ending_question():
	answer = input('Do you want to continue execution? If not, enter "no" \n')
	if answer[0].lower() == 'n':
		sys.exit(1)
	else:
		func_selector()
	
def func_selector():
	caseNumber = input("\n 1: Old game file cleaning \n 2: Game files update \n 3: Audio localization files update \n")
	print('Type "4" to exit')

	match caseNumber:
		case "1":
			dir_Selector(0)
			old_files_cleaning(Path(DIR_GAME_ROOT_PATH), Path(DIR_GAME_FILES_UPDATE))
		case "3":
			dir_Selector(1)
			audio_localization_package_updater(Path(DIR_GAME_ROOT_PATH), Path(DIR_AUDIO_LOCALIZATION_FILES_UPDATE))
		case "2":
			dir_Selector(0)
			game_audio_updater(Path(DIR_GAME_ROOT_PATH), Path(DIR_GAME_FILES_UPDATE))
			game_files_updater(Path(DIR_GAME_ROOT_PATH), Path(DIR_GAME_FILES_UPDATE))
		case _:
			print("Nothing selected, exit")

def main():
	print("Created for non-commercial purposes by https://github.com/andresik12")
	print("Genshin impact files patcher")
	print("For entering path of directories, you can simply drag and drop folder at cmd window (for widnows), terminal window (for macos), konsole (for linux)")
	print("Extra symbols will be removed automatically")
	print("Enter number of function to execute:")
	func_selector()
	

is_first_start = True
if is_first_start:
	is_first_start = False
	main()