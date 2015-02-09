#!/usr/bin/env python
# coding=utf-8

import codecs, os.path, sys, re, shutil, time, getpass, os, distutils, random, xlrd, xlwt, glob, unicodedata, difflib, subprocess, pipes
from difflib import SequenceMatcher
from xlrd import open_workbook
from xlutils.copy import copy

reload(sys)

# GenerationDir - the directory that contains the library directories
__GenerationDir = "/content/integrator"
__CTR_dir = "/content/integrator/ctrs"
# __RemoteHost - consus unbuntu dropbox server
__RemoteHost = "root@172.16.40.92"
# GraphicsLibDir - the directory containing all the graphics directories for items
__GraphicsLibDir = "/root/ContentShare/Library-Graphics_ready/"

# Globals
__MissingFiles = []

sys.setdefaultencoding('utf-8')

__LanguageMap = {	'English' : 'ENG',
					'Arabic' : 'ARA',
					'Arabic' : 'ARB',
					'Dutch' : 'DUT',					'Russian' : 'RUS',
					'German' : 'GER',
					'Chinese' : 'CHI',
					'French' : 'PFR',
					'Parisian French' : 'PFR',
					'Canadian French' : 'CFR',
					'Japanese' : 'JAP',
					'Japanese/English' : 'JAPENG',
					'Korean' : 'KOR',
					'Hindi' : 'HIN',
					'Tagalog' : 'TAG',
					'Tamil' : 'TAM',
					'Filipino' : 'FIL',
					'Urdu' : 'URD',
					'Italian' : 'ITA',
					'Swedish' : 'SWE',
					'Norwegian' : 'NOR',
					'Silent' : 'SIL',
					'Danish' : 'DAN',
					'Azeri' : 'AZE',
					'Icelandic' : 'ICE',
					'Portuguese' : 'POR',
					'Hebrew' : 'HEB',
					'Spanish' : 'SPA',
					'Castilian Spanish' : 'CSP',
					'Latin Spanish' : 'LSP',
					'Swahili' : 'SWA',
					'Malaysian' : 'MAL',
					'Indonesia' : 'IND',
					'Indonesian' : 'IND',
					'Engels' : 'ENE',
					'Nederlands' : 'NED',
					'Vietnamese' : 'VIE',
					'Bosnian' : 'BOS',
					'Thai' : 'THA',
					'Mandarin' : 'MAN',
					'Mandalin' : 'MAN',
					'Cantonese' : 'CAN',
					'Thai' : 'THA'}

__AirlineMap = {	'ana' : 'ANA',
					'thatana' : 'ANA',
					'gulfair' : 'GFA',
					'aeroflot' : 'AFL',
					'kenya' : 'KQA',
					'northamerican' : 'NAO',
					'chinasouthern' : 'CSN',
					'ethiopian' : 'ETH',
					'sun-country' : 'SCX',
					'ram' : 'RAM',
					'fijiair' : 'FJL',
					'alaska' : 'ASA'}
					
__EditTypeMap = {	'edited' : '-ED',
					'theatrical' : '-TH',
					'special edited' : '-SE',
					'airline edited' : '-AE',
					'international' : '-INT',
					'domestic' : '-DOM'}
					
def strip_accents(input_str):
	input_str.decode('utf8', 'ignore')
	nkfd_form = unicodedata.normalize('NFKD', input_str)
	return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])
	
def TitleToFilename(file):
	retVal = file.strip().encode('utf-8')
	retVal = retVal.replace("&", "And")
	retVal = retVal.replace("é", "e") 
	retVal = retVal.replace("à", "a")
	retVal = re.sub(r'[\W]', r"", retVal)

	for i in range(0,len(retVal)-1):
		if (retVal[i] == " " and i < len(retVal)-2):
			tList = list(retVal)
			tList[i+1] = tList[i+1].upper()
			retVal = "".join(tList)
	retVal = retVal.replace(" ", "")
	return retVal.encode('utf-8')

def BuildListFromExcel(filename):
	thisXL = open_workbook(filename)
	writeXL = []
	for sheet in thisXL.sheets():
		number_of_rows = sheet.nrows
		number_of_columns = sheet.ncols
		page = []
		for row in range(number_of_rows):
			splits = []
			for col in range(number_of_columns):
				splits.append(sheet.cell(row,col).value)
			page.append(splits)
		writeXL.append(page)
	return writeXL
	
def BuildList(filename):
	lines = ""
	try:
		f = codecs.open(filename, 'r', 'utf-8')
		lines = f.readlines()
		f.close()
	except IOError as (errno, strerror):
		print "ZOMG I'M IO-ERRORING!!!" + filename
		print "I/O error({0}): {1}".format(errno, strerror)
	except ValueError:
		print "ZOMG I'M VALUE-ERRORING!!!"
		print "Could not convert data to an integer."
	except:
		print "ZOMG I'M UNEXPECTED-ERRORING!!!"
		print "Unexpected error:", sys.exc_info()[0]
		raise
	return lines
	
def WriteToMml(item_list):
	f.write(((indent+1) * "\t") + "<itemcount> " + str(len(item_list)) + "</itemcount>\n")
	f.write(((indent+1) * "\t") + "<flag>" + flag + "</flag>\n")
	if (background == "yes"): f.write(((indent+1) * "\t") + "<image>bg-a3.png</image>\n")
	for i in range(0, len(item_list)):
		f.write(item_list[i])
		
def WriteGenresToMml(item_list, icon, local_subcategory_itemcount):
	r = 0
	f.write(((indent+1) * "\t") + "<itemcount> " + str(local_subcategory_itemcount + all_videos_yes) + "</itemcount>\n")
	if (background == "yes"): f.write(((indent+1) * "\t") + "<image>bg-a3.png</image>\n")
	if (icon == ""):
		print "Sub-category for " + AmIaFloat(cataList[menuLangENG][c][0][1]).strip() + " does not have sub-icon type listed on Overview sheet"
		exit(1)
	if ("poster" in icon): f.write(((indent+1) * "\t") + "<flag>f</flag>\n")
	for k in range((len(cataList[menuLangENG][c]) - all_videos_yes)):
		icon = AmIaFloat(cataList[l][c][k][4]).strip()
		if (icon == ""):
			print "Sub-category for " + AmIaFloat(cataList[menuLangENG][c][k][1]).strip() + " does not have sub-icon type listed on Overview sheet"
			exit(1)
		key = AmIaFloat(cataList[l][c][k][1])
		if (not key in item_list):
			print "The sub-category " + AmIaFloat(cataList[menuLangENG][c][k][1]).strip() + " is missing from the " + AmIaFloat(cataList[menuLangENG][c][0][0]).strip() + " category in the " + directory_lang[l].upper() + " menu or does not match"
			exit(1)
		subcategory_subtext = ""
		if (l != menuLangENG): commentTitle = AmIaFloat(cataList[menuLangENG][c][k][1]).strip() + " __ " + key
		else: commentTitle = key
		if ("(" in key and ")" in key):
			localTitle = key.split('(')[0].strip()
			subcategory_subtext = key.replace(key.split('(')[0],"",1).strip()
			subcategory_subtext = subcategory_subtext[1:-1]
		else: localTitle = key
		if (len(key) > 1):
			f.write(((indent+1) * "\t") + "<menuitem> #" + commentTitle + "\n")
			f.write(((indent+2) * "\t") + "<title>" + localTitle + "</title>\n")
			if (subcategory_subtext != ""): f.write(((indent+2) * "\t") + "<subText>" + subcategory_subtext + "</subText>\n")
			if (icon.lower() == "random-poster"):
				for i in range(0, len(menu_metadata[l][c])):
					random_subcat = AmIaFloat(menu_metadata[l][c][i][4])
					if (random_subcat.rstrip('"').lstrip('"').strip().replace("#","@") == key):
						r = i
						break
				english_title = AmIaFloat(menu_metadata[l][c][r][5])
				english_episode = AmIaFloat(menu_metadata[l][c][r][6])
				poster = TitleToFilename(english_title + english_episode)
				f.write(((indent+2) * "\t") + "<poster>/content/menu/images/interface/" + poster.lower() + ".png</poster>\n")
			elif ("poster" in icon.lower()):
				poster = icon.replace("poster", "").strip()
				GetImage(poster, "", image_directory)
				f.write(((indent+2) * "\t") + "<poster>/content/menu/images/interface/" + poster.lower() + ".png</poster>\n")
			else: f.write(((indent+2) * "\t") + "<icon>/content/menu/images/icons/" + icon + ".png</icon>\n")
			if (not "digetunes" in item_list[key]): f.write(((indent+2) * "\t") + "<flag>f</flag>\n")
			if (subcategory_itemcount[key] > 0): f.write(((indent+2) * "\t") + "<itemcount>" + str(subcategory_itemcount[key]) + "</itemcount>\n")
			if (background == "yes"): f.write(((indent+2) * "\t") + "<image>bg-a3.png</image>\n")
			f.write(item_list[key])
			f.write(((indent+1) * "\t") + "</menuitem>\n")
	if (item_list.has_key("")): f.write(item_list[""])
		
def WriteAllToMml(item_list, subcategory_icon):
	keys = item_list.keys()
	keys.sort()
	f.write(((indent+1) * "\t") + "<menuitem> #All Movies\n")
	f.write(((indent+2) * "\t") + "<title>" + all_text + "</title>\n")
	if (subcategory_icon.lower() == "random-poster"):
		r = randint(0, len(menu_metadata[l][c]))
		poster = TitleToFilename(AmIaFloat(menu_metadata[l][c][r][1]).rstrip('"').lstrip('"').strip().replace("#","@") + AmIaFloat(menu_metadata[l][c][r][2]).rstrip('"').lstrip('"').strip().replace("#","@"))
		f.write(((indent+2) * "\t") + "<poster>/content/menu/images/interface/" + poster.lower() + ".png</poster>\n")
	elif (subcategory_icon.lower() == "poster"):
		poster = TitleToFilename(AmIaFloat(cataList[l][c][0][menuLangENG]).strip() + englishKeys[y][k])
		GetImage(AmIaFloat(cataList[l][c][0][menuLangENG]).strip(), "all_movies", image_directory)
		f.write(((indent+2) * "\t") + "<poster>/content/menu/images/interface/" + poster.lower() + ".png</poster>\n")
	else:
		if (subcategory_icon.lower() == "icon"): subcategory_icon = TitleToFilename(AmIaFloat(cataList[l][c][0][menuLangENG]).strip() + englishKeys[y][k])
		f.write(((indent+2) * "\t") + "<icon>/content/menu/images/icons/" + subcategory_icon + ".png</icon>\n")
	f.write(((indent+2) * "\t") + "<flag>f</flag>\n")
	f.write(((indent+2) * "\t") + "<itemcount>" + str(len(all_movies)) + "</itemcount>\n")
	if (background == "yes"): f.write(((indent+2) * "\t") + "<image>bg-a3.png</image>\n")
	for key in keys:
		f.write(item_list[key])
	f.write(((indent+1) * "\t") + "</menuitem>\n")
	
def WriteMusicCat(digetunes):
	itemAddon = ""
	itemAddon += ((indent+1) * "\t") + "<action>\n"
	itemAddon += ((indent+2) * "\t") + "<command>!digetunes --music-subdir=" + digetunes + "</command>\n"
	itemAddon += ((indent+1) * "\t") + "</action>\n"
	subcategories[subcategory] += itemAddon
	return itemAddon
	
def WriteInternetCat():
	f.write(((indent+1) * "\t") + "<icon>/content/menu/images/icons/" + AmIaFloat(cataList[l][c][0][3]).strip() + ".png</icon>\n")
	f.write(((indent+1) * "\t") + "<action>\n")
	f.write(((indent+2) * "\t") + "<command>stopwifi.sh</command>\n")
	f.write(((indent+1) * "\t") + "</action>\n")
	f.write(((indent+1) * "\t") + "<action>\n")
	f.write(((indent+2) * "\t") + "<command>!startwifi /content/menu/images/BrowserWarning.png</command>\n")
	f.write(((indent+1) * "\t") + "</action>\n")
	f.write(((indent+1) * "\t") + "<action>\n")
	f.write(((indent+2) * "\t") + "<command>run_browser.sh " + homepage + "</command>\n")
	f.write(((indent+1) * "\t") + "</action>\n")
	f.write(((indent+1) * "\t") + "<action>\n")
	f.write(((indent+2) * "\t") + "<command>stopwifi.sh</command>\n")
	f.write(((indent+1) * "\t") + "</action>\n")
	f.write((indent * "\t") + "</menuitem>\n")
	
def MenuItem(local_item, menu_lang, item_subtext):
		itemAddon = ""
		if (len(episode) > 0):
			local_episode = " - " + episode
			local_english_episode = " - " + english_episode
		else:
			local_episode = ""
			local_english_episode = ""
		if (l != menuLangENG): comment_title = english_title + local_english_episode + " __ " + title + local_episode
		else: comment_title = english_title + local_english_episode
			
		itemAddon += ((indent+2) * "\t") + "<menuitem> #" + comment_title + "\n"
		itemAddon += ((indent+3) * "\t") + "<title>" + title + local_episode + "</title>\n"
		if (item_subtext != "" and (duration.strip() != "" or rating.strip() != "")):
			item_subtext = item_subtext.replace("$DURATION", duration.strip())
			item_subtext = item_subtext.replace("$RATING", rating.strip())
			item_subtext = item_subtext.replace("$LANGUAGE", language_list.strip())
			itemAddon += ((indent+3) * "\t") + "<subText>" + item_subtext + "</subText>\n"
		itemAddon += ((indent+3) * "\t") + "<poster>/content/menu/images/interface/" + TitleToFilename(english_title + english_episode).lower() + date + ".png" + " </poster>\n"
		itemAddon += ((indent+3) * "\t") + "<text>/content/menu/text/" + subcategory_type + "/" + menu_lang + "/" + TitleToFilename(english_title + english_episode) + ".txt</text>\n"
		itemAddon += ((indent+3) * "\t") + "<actionGroup>\n"
		itemAddon += ((indent+4) * "\t") + "<title>" + play_text[l].strip() + "</title>\n"
		itemAddon += ((indent+4) * "\t") + "<action>\n"
		if (AmIaFloat(local_item[lang_start_cell + 1]).strip() != "" or AmIaFloat(local_item[lang_start_cell + 9]).strip() != ""):
			itemAddon += ((indent+5) * "\t") + "<command>play_video %1 -f DejaVuSans:20 -t \"" + title + local_episode + "\"" + ad_list + " /content/videos/" + video_filename + " </command>\n"
			if(AmIaFloat(local_item[lang_start_cell + 1]).strip() != ""):
				itemAddon += ((indent+5) * "\t") + "<argument>\n"
				itemAddon += ((indent+6) * "\t") + "<title>" + select_lang_text[l].strip() + "</title>\n"
				for x in range(lang_start_cell, lang_start_cell + 6):
					if (AmIaFloat(local_item[x]).strip() != ""):
						secondLanguage = AmIaFloat(local_item[x]).strip()
						itemAddon += ((indent+7) * "\t") + "<selection>\n"
						itemAddon += ((indent+8) * "\t") + "<title>"+ secondLanguage + " " + audio_text[l].strip() + "</title>\n"
						languagenumber = unicode(x - lang_start_cell)
						itemAddon += ((indent+8) * "\t") + "<value>-a " + languagenumber + "</value>\n"
						itemAddon += ((indent+7) * "\t") + "</selection>\n"
					else : continue
				if (AmIaFloat(local_item[lang_start_cell + 9]).strip() == ""):
					itemAddon += ((indent+5) * "\t") + "</argument>\n"
					itemAddon += ((indent+4) * "\t") + "</action>\n"
					itemAddon += ((indent+3) * "\t") + "</actionGroup>\n"
					itemAddon += ((indent+2) * "\t") + "</menuitem>\n"
				else: itemAddon += ((indent+5) * "\t") + "</argument>\n"
			if (AmIaFloat(local_item[lang_start_cell + 9]).strip() != ""):
				itemAddon += ((indent+5) * "\t") + "<argument>\n"
				itemAddon += ((indent+6) * "\t") + "<title>" + select_subtitle_text[l].strip() + "</title>\n"
				for u in range(lang_start_cell + 9, lang_start_cell + 12):
					if (AmIaFloat(local_item[u]).strip() != ""):
						itemAddon += ((indent+7) * "\t") + "<selection>\n"
						itemAddon += ((indent+8) * "\t") + "<title>"+ AmIaFloat(local_item[u]) + " " + subtitle_text[l].strip() + "</title>\n"
						subtitlenumber = unicode(u - (lang_start_cell + 9))
						itemAddon += ((indent+8) * "\t") + "<value>-u " + subtitlenumber + "</value>\n"
						itemAddon += ((indent+7) * "\t") + "</selection>\n"
					else : continue
				itemAddon += ((indent+7) * "\t") + "<selection>\n"
				itemAddon += ((indent+8) * "\t") + "<title>" + none_text[l].strip() + "</title>\n"
				itemAddon += ((indent+8) * "\t") + "<value> </value>\n"
				itemAddon += ((indent+7) * "\t") + "</selection>\n"
				itemAddon += ((indent+5) * "\t") + "</argument>\n"
				itemAddon += ((indent+4) * "\t") + "</action>\n"
				itemAddon += ((indent+3) * "\t") + "</actionGroup>\n"
				itemAddon += ((indent+2) * "\t") + "</menuitem>\n"
		else :
			itemAddon += ((indent+5) * "\t") + "<command>play_video " + aerolang + "-t \"" + title + local_episode + "\"" + ad_list + " /content/videos/" + video_filename + " </command>\n"
			itemAddon += ((indent+4) * "\t") + "</action>\n"
			itemAddon += ((indent+3) * "\t") + "</actionGroup>\n"
			itemAddon += ((indent+2) * "\t") + "</menuitem>\n"
		subcategories[subcategory] += itemAddon
		if (len(all_movies[title + episode]) < 1): all_movies[title + episode] += itemAddon  #checks for menuitems in multiple subcategories won't show up multiple times in All Movies
		writeMe[(itemcount - 1)] = itemAddon
		
def FindBestFileNameMatch(filebase, langs, file_list):
	canidates = []
	canidate_ratio = []
	highest_ratio = 0
	highest_title_ratio = 0
	highest_match = -1
	item_all_lang_split = langs.split("_")
	if (new_holdover.lower() == "h"): 
		threshold = .8
		if (date != ""): local_date = "-" + str(int(__Last_Month)) + "-1-" + __Last_Year
		else: local_date = date
	else: 
		threshold = .9
		local_date = date
	if (category_type != "musicvideos" and (menu_metadata[l][see][i][16] != "" or menu_metadata[l][see][i][18] != "")):
		item_langs_split = SplitUpLangs(item_all_lang_split[-2])
		item_subs_split = SplitUpLangs(item_all_lang_split[-1])
		has_subs = True
	else:
		item_langs_split = SplitUpLangs(item_all_lang_split[-1])
		item_subs_split = ""
		has_subs = False
	for k in range(len(file_list)):
		full_match = SequenceMatcher(None, filebase.replace("The", "") + local_date + edit_type + langs, file_list[k].replace(".mkv", "").replace(".enc", "").replace("The", "").replace(airline_ID, ""))
		if (full_match.ratio() > .978): return file_list[k]
		if (edit_type != "-SE" or edit_type != "-AE" or edit_type != "-INT"):
			full_match = SequenceMatcher(None, filebase.replace("The", "") + local_date + langs, file_list[k].replace(".mkv", "").replace(".enc", "").replace("The", "").replace(airline_ID, ""))
			if (full_match.ratio() > .978): return file_list[k]
			file_list_splits = file_list[k].replace(".mkv", "").replace(".enc", "").split("_")
			if (has_subs):
				file_langs_split = SplitUpLangs(file_list_splits[-2])
				file_subs_split = SplitUpLangs(file_list_splits[-1])
				if (not HasLangs(item_subs_split, file_subs_split)): continue
				if (not HasLangs(item_langs_split, file_langs_split)): continue
			else:
				file_langs_split = SplitUpLangs(file_list_splits[-1])
				if (not HasLangs(item_langs_split, file_langs_split)): continue
			basic_title_match = SequenceMatcher(None, TitleToFilename(filebase.replace("The", "").lower() + local_date), TitleToFilename(file_list_splits[0].replace("The", "").replace(airline_ID, "").replace("-ED", "").replace("-TH", "").lower()))
			edittype_title_match = SequenceMatcher(None, TitleToFilename(filebase.replace("The", "").lower() + edit_type + local_date), TitleToFilename(file_list_splits[0].replace("The", "").replace(airline_ID, "").lower()))
			dateless_title_match = SequenceMatcher(None, TitleToFilename(filebase.replace("The", "").lower() + edit_type), TitleToFilename(file_list_splits[0].replace("The", "").replace(airline_ID, "").lower()))
			matches = [basic_title_match.ratio(), edittype_title_match.ratio(), dateless_title_match.ratio()]
			title_match = max(matches)
			if (title_match >= threshold):
				canidates.append(file_list[k])
				canidate_ratio.append(title_match)
			if ((title_match + full_match.ratio()) > highest_ratio):
				highest_match = k
				highest_ratio = title_match + full_match.ratio()
				highest_title_ratio = title_match
	if (len(canidates) > 1):
		print "\nSelect video file. Expecting " + holder_new + " title: " 
		print TitleToFilename(english_title.replace("'", "").lower().title() + dash + english_episode.replace("'", "").lower().title()) + local_date + langs + ".mkv"
		print "\nEnter selection #:"
		for can in range(len(canidates)):
			print "\n#" + str(can + 1) + " - " + canidates[can] + " - " + str(canidate_ratio[can])
		print "\n#" +  str(len(canidates) + 1) + " - None of these video files\n"
		selection = input("Enter selection: ")
		if (selection <= len(canidates)): return canidates[(selection - 1)]
		return "MISSINGVIDEO"
	elif (len(canidates) == 0):
		return "MISSINGVIDEO"
	else:
		return file_list[highest_match]

def SplitUpLangs(local_langs):
	langs_split = []
	for s in range((len(local_langs)/3)):
		ls = s*3
		langs_split.append(local_langs[ls] + local_langs[ls+1] + local_langs[ls+2])
	return langs_split

def HasLangs(are_these, in_those):
	for ls in are_these:
		if (not ls in in_those):
			if ("PFR" == ls and "FRE" in in_those):
				continue
			return False
	return True
	
def GetVideoFileName(local_video_dir, e_place, t_place, v_place):
	this_title = TitleToFilename(english_title + english_episode).lower()
	if (new_holdover.lower() == "h" and lastXL != ""):
		for i in range(6, lastXL.nsheets):
			for r in range(1, lastXL.sheet_by_index(i).nrows):
				last_title = AmIaFloat(lastXL.sheet_by_index(i).cell(r,t_place).value) + AmIaFloat(lastXL.sheet_by_index(i).cell(r,e_place).value)
				if (TitleToFilename(last_title).lower() == this_title and lastXL.sheet_by_index(i).cell(r,v_place).value.strip() != ""): return lastXL.sheet_by_index(i).cell(r,v_place).value.strip()
	for i in range (len(local_video_dir)):
		video_list = os.listdir(local_video_dir[i])
		result = FindBestFileNameMatch(TitleToFilename(english_title.replace("'", "").lower().title()) + dash + TitleToFilename(english_episode.replace("'", "").lower().title()), video_filename_langs, video_list)
		if (result != "MISSINGVIDEO"): return local_video_dir[i] + result
	return "MISSINGVIDEO"
	
def GetFileNameLanguages(local_item):
	lang_list = ""
	lang = ""
	if (local_item[lang_start_cell].strip() != ""): lang_list += "_"
	for i in range(lang_start_cell, lang_start_cell + 6):
		if (local_item[i].strip() != ""):
			lang = local_item[i].strip()
			if (lang in __LanguageMap): lang_list += __LanguageMap[lang]
			else:
				print lang + " Language code not found for " + title.encode('utf-8')
				exit(1)
	if (local_item[lang_start_cell + 7].strip() != ""):
		lang = local_item[lang_start_cell + 7].strip()
		if (lang in __LanguageMap): lang_list += "_" + __LanguageMap[lang]
		else:
			print lang + " Language code not found for " + title.encode('utf-8')
			exit(1)
		if (local_item[lang_start_cell + 8].strip() != ""):
			lang = local_item[lang_start_cell + 8].strip()
			if (lang in __LanguageMap): lang_list += __LanguageMap[lang]
			else:
				print lang + " Language code not found for " + title.encode('utf-8')
				exit(1)
	if (local_item[lang_start_cell + 9].strip() != ""): lang_list += "_"
	for j in range(lang_start_cell + 9, lang_start_cell + 12):
		if (local_item[j].strip() != ""):
			lang = local_item[j].strip().encode('utf-8')
			lang = re.sub(r'[\W]', r"", lang)
			if (lang in __LanguageMap): lang_list += __LanguageMap[lang].lower()
			else:
				print lang + " Language code not found for " + title.encode('utf-8')
				exit(1)
	return lang_list

def GetLanguages(local_metadata):
	local_lang = ""
	local_sub = ""
	for x in range(lang_start_cell, (lang_start_cell + 6)):
		if (local_metadata[x].strip() != ""): local_lang = local_lang + ", " + local_metadata[x]
	if (local_lang != ""): local_lang = local_lang[2:]
	for g in range((lang_start_cell + 7), (lang_start_cell + 12)):
		subtitle_list = local_metadata[g].strip()
		if (subtitle_list.strip() != ""):
			if (local_sub.strip() == ""): local_sub = " (" + subtitle_list.strip()
			else: local_sub = local_sub + ", " + subtitle_list.strip()
	if (local_sub.strip() != ""): local_sub = local_sub + " " + subtitle_text[l].strip() + ")"
	language_list = local_lang + local_sub
	return language_list
	
def GetBulkFiles(ext, input, output):
	if(not os.path.exists(__OutputDir + "menu/" + output + "/")): os.makedirs(__OutputDir + "menu/" + output + "/")
	if(os.path.exists(os.getcwd() + "/config" + __Demo + "/" + input + "/")):
		sourceIcons = os.listdir(os.getcwd() + "/config" + __Demo + "/" + input + "/")
		for files in sourceIcons:
			if files.endswith(ext): shutil.copy(os.getcwd() + "/config" + __Demo + "/" + input + "/" + files,__OutputDir + "menu/" + output + "/")
	else: __MissingFiles.append(os.getcwd()+ "config" + __Demo + "/" + input + "/ directory is missing")
			
def GetImage(local_title, local_episode, directory):
	scp_full_cmd = ""
	scp_L10full_cmd = ""
	if(not os.path.exists(__OutputDir + "menu/images/interface/")): os.makedirs(__OutputDir + "menu/images/interface/")
	if ("L10" in player_type):
		if(not os.path.exists(__OutputDir + "menu/images_L10/interface/")): os.makedirs(__OutputDir + "menu/images_L10/interface/")
	Imagefilebase = TitleToFilename(local_title) + date
	ImageFullfilebase = TitleToFilename(local_title + local_episode) + date
	if(l > 0  and os.path.exists(__OutputDir + "menu/images/interface/" + ImageFullfilebase.lower() + ".png")): return
	image_directory_list = subprocess.Popen(['ssh', __RemoteHost, "ls " + __GraphicsLibDir + directory + "/"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	image_list =  image_directory_list.communicate()[0].split()
	for images in image_list:
		if (images[:-4].lower() == ImageFullfilebase.lower()):
			scp_full_cmd = "scp " + __RemoteHost + ":" + __GraphicsLibDir + directory + "/" + images + " " + __OutputDir + "menu/images/interface/" + ImageFullfilebase.lower() + ".png"
			os.system(scp_full_cmd)
			if (player_type == "L10"):
				scp_L10_cmd = "scp " + __RemoteHost + ":" + __GraphicsLibDir + directory + "/" + images + " " + __OutputDir + "menu/images_L10/interface/" + ImageFullfilebase.lower() + ".png"
				os.system(scp_L10_cmd)
			break
	if (scp_full_cmd == ""): 
		for images in image_list:
			if (images[:-4].lower() == Imagefilebase.lower()):
				scp_full_cmd = "scp " + __RemoteHost + ":" + __GraphicsLibDir + directory + "/" + images + " " + __OutputDir + "menu/images/interface/" + ImageFullfilebase.lower() + ".png"
				os.system(scp_full_cmd)
				if (player_type == "L10"):
					scp_L10_cmd = "scp " + __RemoteHost + ":" + __GraphicsLibDir + directory + "/" + images + " " + __OutputDir + "menu/images_L10/interface/" + ImageFullfilebase.lower() + ".png"
					os.system(scp_L10_cmd)
				break
	if (scp_full_cmd == ""): __MissingFiles.append(ImageFullfilebase + ".png in " + directory)
	if (player_type == "L7-L10"):
		imageL10_directory_list = subprocess.Popen(['ssh', __RemoteHost, "ls " + __GraphicsLibDir + directory + "L10/"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		for images in imageL10_directory_list.communicate():
			if (images[:-4].lower() == ImageFullfilebase.lower()):
				scp_L10full_cmd = "scp " + __RemoteHost + ":" + __GraphicsLibDir + directory + "L10/" + images + " " + __OutputDir + "menu/images_L10/interface/" + ImageFullfilebase.lower() + ".png"
				os.system(scp_L10full_cmd)
			break
		if (scp_L10full_cmd == ""): 
			for images in imageL10_directory_list.communicate():
				if (images[:-4].lower() == Imagefilebase.lower()):
					scp_L10full_cmd = "scp " + __RemoteHost + ":" + __GraphicsLibDir + directory + "L10/" + images + " " + __OutputDir + "menu/images_L10/interface/" + ImageFullfilebase.lower() + ".png"
					os.system(scp_L10full_cmd)
				break
		if (scp_L10full_cmd == ""): __MissingFiles.append(ImageFullfilebase + ".png in " + directory + "L10")
		
def GetSynop(menu_lang, video_type):
	if(not os.path.exists(__OutputDir + "menu/text/" + video_type + "/" + menu_lang + "/")):
		os.makedirs(__OutputDir + "menu/text/" + video_type + "/" + menu_lang + "/")
	filebase = TitleToFilename(english_title + english_episode)
	if(os.path.exists(__Airline_OutputDir + "config" + __Demo + "/" + synop_basefile + ".txt")):
		BASE = codecs.open(__Airline_OutputDir + "config" + __Demo + "/" + synop_basefile + ".txt", 'r', 'utf-8').read()
		BASE = BASE.replace("$TITLE", title)
		BASE = BASE.replace("$EPISODE", episode)
		BASE = BASE.replace("$DURATION", duration)
		BASE = BASE.replace("$RATING", rating)
		BASE = BASE.replace("$LANGUAGE", language_list)
		BASE = BASE.replace("$GENRE", genre)
		BASE = BASE.replace("$CAST", cast)
		BASE = BASE.replace("$SYNOPSIS", synopsis)
		BASE = BASE.replace("<span style=\"font-size:14pt\"></span><br>", "")
		BASE = BASE.replace("<span style=\"font-size:12pt\"> / </span><br>", "")
		BASE = BASE.replace("<span style=\"font-size:12pt\"></span><br>", "")
		outFile = codecs.open(__OutputDir + "menu/text/" + video_type + "/" + menu_lang + "/" + filebase + ".txt", 'w+', 'utf-8')
		outFile.write(BASE)
		outFile.close()
	else:
		print synop_basefile + ".txt does not exist in " + __OutputDir
		exit(1)
		
def GetLangText(excel, row):
	text = []
	cell = 2
	for i in range(menu_length):
		text.append(excel[menu_lang_page][row][(cell + i)])
	return text
	
def WriteMagazineCat():
	if (len(episode) > 0):
			local_episode = " - " + episode
			local_english_episode = " - " + english_episode
	else:
		local_episode = ""
		local_english_episode = ""
	itemAddon = ""
	itemAddon += ((indent+2) * "\t") + "<menuitem> #" + english_title + local_english_episode +"\n"
	itemAddon += ((indent+3) * "\t") + "<title>" + title + local_episode + "</title>\n"
	itemAddon += ((indent+3) * "\t") + "<poster>/content/menu/images/interface/" + TitleToFilename(english_title + local_english_episode).lower() + ".png" + "</poster>\n"
	itemAddon += ((indent+3) * "\t") + "<actionGroup>\n"
	itemAddon += ((indent+4) * "\t") + "<title>" + title + "</title>\n"
	itemAddon += ((indent+4) * "\t") + "<action>\n"
	itemAddon += ((indent+5) * "\t") + "<command>!viewMagazine -t \"" + title + "\" /content/magazines/" + TitleToFilename(AmIaFloat(cataList[menuLangENG][c][0][0]).split('(')[0].strip()) + "/" + directory_lang[l] + " </command>\n"
	itemAddon += ((indent+4) * "\t") + "</action>\n"
	itemAddon += ((indent+3) * "\t") + "</actionGroup>\n"
	itemAddon += ((indent+2) * "\t") + "</menuitem>\n"
	writeMe[(itemcount - 1)] = itemAddon
	
def WriteSurveyCat(survey_title):
	if(not os.path.exists(__OutputDir + "menu/survey/")): os.makedirs(__OutputDir + "menu/survey/")
	if (os.path.exists(__Airline_OutputDir + "config" + __Demo + "/test.sml")):
		shutil.copy(__Airline_OutputDir + "config" + __Demo + "/test.sml", __OutputDir + "menu/survey/" + TitleToFilename(survey_title) + str(l + 1) + ".sml")
	else:
		print "The test survey: test.sml, was not found in the config directory.\nYou should probably write the CreateSmlFromCTR method."
		exit(1)
	itemAddon = ""
	itemAddon += ((indent+2) * "\t") + "<menuitem> #" + survey_title + "\n"
	itemAddon += ((indent+3) * "\t") + "<title>" + survey_title + "</title>\n"
	itemAddon += ((indent+3) * "\t") + "<poster>/content/menu/images/interface/" + TitleToFilename(survey_title).lower() + ".png" + "</poster>\n"
	itemAddon += ((indent+3) * "\t") + "<actionGroup>\n"
	itemAddon += ((indent+4) * "\t") + "<title>" + survey_title + "</title>\n"
	itemAddon += ((indent+4) * "\t") + "<action>\n"
	itemAddon += ((indent+5) * "\t") + "<command>!digemonkey /content/menu/survey/" + TitleToFilename(survey_title) + str(l + 1) + ".sml -t \"" + survey_title + "\" </command>\n"
	itemAddon += ((indent+4) * "\t") + "</action>\n"
	itemAddon += ((indent+3) * "\t") + "</actionGroup>\n"
	itemAddon += ((indent+2) * "\t") + "</menuitem>\n"
	writeMe[(itemcount - 1)] = itemAddon
	
def Podcasts(image):
	itemAddon = ""
	itemAddon += ((indent+2) * "\t") + "<menuitem> #" + title + "\n"
	itemAddon += ((indent+3) * "\t") + "<title>" + title + "</title>\n"
	itemAddon += ((indent+3) * "\t") + "<poster>/content/menu/images/interface/" + image + ".png" + "</poster>\n"
	itemAddon += ((indent+3) * "\t") + "<actionGroup>\n"
	itemAddon += ((indent+4) * "\t") + "<title>" + play_text[l].strip() + "</title>\n"
	itemAddon += ((indent+4) * "\t") + "<action>\n"
	itemAddon += ((indent+5) * "\t") + "<command>!digetunes -t \"" + title + "\" --book /content/audio/podcasts/" + TitleToFilename(title) + " </command>\n"
	itemAddon += ((indent+4) * "\t") + "</action>\n"
	itemAddon += ((indent+3) * "\t") + "</actionGroup>\n"
	itemAddon += ((indent+2) * "\t") + "</menuitem>\n"
	writeMe[(itemcount - 1)] = itemAddon
	
def Games(menu_lang):
	itemAddon = ""
	if (source_filepath.startswith("fdg")): start_script = "start_game"
	else: start_script = source_filepath.strip()
	itemAddon += ((indent+2) * "\t") + "<menuitem> #" + english_title + "\n"
	itemAddon += ((indent+3) * "\t") + "<title>" + title + "</title>\n"
	itemAddon += ((indent+3) * "\t") + "<poster>/content/menu/images/interface/" + TitleToFilename(english_title).lower() + ".png" + "</poster>\n"
	itemAddon += ((indent+3) * "\t") + "<text>/content/menu/text/games/" + menu_lang + "/" + TitleToFilename(english_title) + ".txt" + "</text>\n"
	itemAddon += ((indent+3) * "\t") + "<actionGroup>\n"
	itemAddon += ((indent+4) * "\t") + "<title>" + game_play_text[l].strip() + "</title>\n"
	itemAddon += ((indent+4) * "\t") + "<action>\n"
	itemAddon += ((indent+5) * "\t") + "<command>/content/games/" + source_filepath.strip() + "/" + start_script + ".sh  -l " + menu_lang + "/ </command>\n"
	itemAddon += ((indent+4) * "\t") + "</action>\n"
	itemAddon += ((indent+3) * "\t") + "</actionGroup>\n"
	itemAddon += ((indent+2) * "\t") + "</menuitem>\n"
	writeMe[(itemcount - 1)] = itemAddon
	subcategories[subcategory] += itemAddon
	
def GetAdList(ad_one, ad_two):
	ads = ""
	if (ad_one != ""):
		if (avail_ad_list != ""): ads = " /content/ads/" + FindHighestFileNameMatch(ad_one, avail_ad_list)
		else: ads = " /content/ads/MISSINGAD"
	if (ad_two != ""):
		if (isinstance( ad_two, float )):
			ad_two = str(int(ad_two))
			if (ad_two == "6"): ad_two = "06"
			ads += " /content/ads/AFL-Disclaimers8sec16x9-" + ad_two + "andUp_SIL.mkv"
		else: ads += " /content/ads/MISSINGAD"
	return ads
	
def BulkAds(ad_category, menu_lang):
	filebase = TitleToFilename(ad_category + str(l + 1))
	if (synop_basefile != ""): GetBulkFiles(".txt", filebase + "/" + menu_lang, "text/" + filebase + "/" + menu_lang)
	bulkAdList = BuildList(__Airline_OutputDir + "config" + __Demo + "/" + filebase + ".txt")
	for i in range(0, len(bulkAdList)):
		item = bulkAdList[i].split('\t')
		for j in range(0, len(item)):
			if (item[j].strip() == ""): f.write("\t")
			else: f.write(item[j].strip())
		f.write("\n")
		
def AmIaFloat(float_or_not):
	if (isinstance( float_or_not, float )): float_or_not = str(int(float_or_not))
	return float_or_not.strip().replace(" ", " ").replace("\"", "")
	
def NoSynopItem(local_title, local_english_title, dir):
	itemAddon = ""
	itemAddon += ((indent+2) * "\t") + "<menuitem> #" + local_english_title + "\n"
	itemAddon += ((indent+3) * "\t") + "<title>" + local_title + "</title>\n"
	itemAddon += ((indent+3) * "\t") + "<poster>/content/menu/images/interface/" + TitleToFilename(local_english_title).lower() + ".png" + "</poster>\n"
	itemAddon += ((indent+3) * "\t") + "<actionGroup>\n"
	itemAddon += ((indent+4) * "\t") + "<title>" + play_text[l].strip() + "</title>\n"
	itemAddon += ((indent+4) * "\t") + "<action>\n"
	itemAddon += ((indent+5) * "\t") + "<command>play_video -t \"" + local_title + "\"" + ad_list + " /content/" + dir + "/MISSINGVIDEO </command>\n"
	itemAddon += ((indent+4) * "\t") + "</action>\n"
	itemAddon += ((indent+3) * "\t") + "</actionGroup>\n"
	itemAddon += ((indent+2) * "\t") + "</menuitem>\n"
	writeMe[(itemcount - 1)] = itemAddon
	
if __name__ == "__main__":

	if (len(sys.argv) < 7):
		print "Usage: MasterMenuGen.py <airline> <CTR month> <CTR year> <last CTR month> <last CTR year> <QA1 or QA2>"
		print "  Uses a source files and generates the directory structure for "
		print "  the menu if those files are available in the generation dir."
		exit(1)

	airline_name = sys.argv[1]
	if (airline_name in __AirlineMap): airline_ID = __AirlineMap[airline_name] + "-"
	else: airline_ID = ""
	if (airline_ID == "AFL"): aerolang = "-a 1 "  #reluctantly hard-coded in to handle aeroflot's unique one lang audio per menu issue
	else: aerolang = ""
	__Airline_OutputDir = "/content/integrator/content-sets/" + airline_name + "/"
	__Year = sys.argv[3]
	__Month = sys.argv[2]
	__QA = sys.argv[4]
	__Last_Year = sys.argv[6]
	__Last_Month = sys.argv[5]
	if (len(sys.argv) > 7): __Demo = sys.argv[7]
	else: __Demo = ""
	if (__Demo != ""): 
		content_tag = __Demo
		__OutputDir = __Airline_OutputDir + "content-" + airline_name + "-" + content_tag + __Month + __Year + "/"
	else: 
		content_tag = airline_name
		__OutputDir = __Airline_OutputDir + "content-" + airline_name + "-" + __Month + __Year + "/"
	
	video_dir = []
	if (os.path.exists("/content/library/l7/airlinespecific/" + airline_name.lower() + "/")):
		video_dir.append("/content/library/l7/airlinespecific/" + airline_name.lower() + "/")
	video_dir.append("/content/library/l7/movies/")
	video_dir.append("/content/library/l7/shortsubject/")
	
	musicvideo_dir = []
	if (os.path.exists("/content/library/l7/musicvideos/airlinespecific/" + airline_name.lower() + "/")): 
		musicvideo_dir.append("/content/library/l7/musicvideos/airlinespecific/" + airline_name.lower() + "/")
	musicvideo_dir.append("/content/library/l7/musicvideos/current-mv/")
	musicvideo_dir.append("/content/library/l7/musicvideos/all-mv/")
	
	if (not os.path.exists(__Airline_OutputDir)):
		print "Airline " + airline_name + " does not exist in /content/integrator/content-sets/"
		exit(1)
	if (not os.path.exists(__OutputDir)): os.makedirs(__OutputDir)
	if (not os.path.exists(__OutputDir + "menu/")): os.makedirs(__OutputDir + "menu/")
	if (not os.path.exists(__Airline_OutputDir + "/config" + __Demo + "/")):
		print __Airline_OutputDir + "/config" + __Demo + "/ does not exist"
		exit(1)
	f = codecs.open(__OutputDir + "menu/menu.mml", 'w+', 'utf-8')
	fvid = codecs.open(__Airline_OutputDir + "/config" + __Demo + "/video-list.txt", 'w+', 'utf-8')
	ferr = codecs.open(__Airline_OutputDir + "/config" + __Demo + "/errors.txt", 'w+', 'utf-8')
	fcit = codecs.open(__OutputDir + "content-id.txt", 'w+', 'utf-8')
	fcit.write(content_tag.title() + " " + __Month + "-" + __Year + " Content\n")
	fcit.close()
	
	ctr_filename = glob.glob(__CTR_dir + "/CTR_" + content_tag + "_" + __Year + "-" + __Month + "_eng.xls")
	if (len(ctr_filename) < 1):
		print "CTR_" + content_tag + "_" + __Year + "-" + __Month + "_eng.xls is missing"
		exit(1)
	menu_lang_page = 4														#There is 2 hidden pages for some reason
	overview_page = 5														#There is 2 hidden pages for some reason
	ctr_excel_list = BuildListFromExcel(ctr_filename[0]) 					#Gets English menu CTR for menu config info
	menu_length = (len(ctr_excel_list[menu_lang_page][2]) - 2)
	player_type = AmIaFloat(ctr_excel_list[overview_page][1][0]).strip()
	start_up_ad = AmIaFloat(ctr_excel_list[overview_page][2][1]).strip()
	if ("video" in start_up_ad):
		start_up_ad += "  /content/ads/" + AmIaFloat(ctr_excel_list[overview_page][2][2]).strip() + ".mkv"
	elif ("billboard" in start_up_ad):
		start_up_ad = "!" + start_up_ad + "  /content/menu/images/" + AmIaFloat(ctr_excel_list[overview_page][2][2]).strip() + ".png 10"
	after_lang_ad = AmIaFloat(ctr_excel_list[overview_page][3][1]).strip()
	if ("video" in after_lang_ad): after_lang_ad += "  /content/ads/" +  AmIaFloat(ctr_excel_list[overview_page][3][2]).strip() + ".mkv"
	elif ("billboard" in after_lang_ad):
		after_lang_ad = "!" + after_lang_ad + "  /content/menu/images/" + AmIaFloat(ctr_excel_list[overview_page][3][2]).strip() + ".png 10"
	menu_lang_text = GetLangText(ctr_excel_list, 2)
	play_text = GetLangText(ctr_excel_list, 3)
	game_play_text = GetLangText(ctr_excel_list, 4)
	select_lang_text = GetLangText(ctr_excel_list, 5)
	select_subtitle_text = GetLangText(ctr_excel_list, 6)
	audio_text = GetLangText(ctr_excel_list, 7)
	language_text = GetLangText(ctr_excel_list, 8)
	subtitle_text = GetLangText(ctr_excel_list, 9)
	none_text = GetLangText(ctr_excel_list, 10)
	duration_text = GetLangText(ctr_excel_list, 11)
	min = GetLangText(ctr_excel_list, 12)
	rating_text = GetLangText(ctr_excel_list, 13)
	all_movies_text = GetLangText(ctr_excel_list, 14)
	all_videos_text = GetLangText(ctr_excel_list, 15)
	intial_volume_level = AmIaFloat(ctr_excel_list[menu_lang_page][16][2]).strip()
	directory_lang = GetLangText(ctr_excel_list, 17)
	background = AmIaFloat(ctr_excel_list[menu_lang_page][18][2]).strip().lower()
	homepage = AmIaFloat(ctr_excel_list[menu_lang_page][19][2]).strip()
	image_directory = AmIaFloat(ctr_excel_list[menu_lang_page][20][2]).strip()
	calibration = AmIaFloat(ctr_excel_list[menu_lang_page][21][2]).strip().lower()
	music_directory = AmIaFloat(ctr_excel_list[menu_lang_page][22][2]).strip().lower()
	ctr_filename = []
	ctr_excel_list = []
	readXL = []
	rsync_video_list = []
	for i in range(len(directory_lang)): 									#Uses directories from English CTR to look for all CTR's in correct order
		ctr_filename.append(glob.glob(__CTR_dir + "/CTR_" + content_tag + "_" + __Year + "-" + __Month + "_" + directory_lang[i] + ".xls"))
		if (len(ctr_filename[i]) < 1):
			print "CTR_" + content_tag + "*" + directory_lang[i].strip() + ".xls is missing"
			exit(1)
		elif (len(ctr_filename[i]) > 1):
			print "There are conflicting CTR_" + content_tag + "*" + directory_lang[i] + ".xls files"
			exit(1)
		if (directory_lang[i] == "eng"): menuLangENG = i
	for i in range(len(ctr_filename)):
		readXL.append(copy(open_workbook(ctr_filename[i][0], formatting_info=True)))
		ctr_excel_list.append(BuildListFromExcel(ctr_filename[i][0])) 
	if (os.path.exists(__CTR_dir + "/CTR_" + content_tag + "_" + __Last_Year + "-" + __Last_Month + "_eng.xls")): 
		lastXL = open_workbook(__CTR_dir + "/CTR_" + content_tag + "_" + __Last_Year + "-" + __Last_Month + "_eng.xls")
	else: lastXL = ""
	cataList = []
	menu_metadata = []
	for j in range(menu_length): 
		menu_cataList = []
		menu_ctr_list = []
		category_item = []
		total_sheets = len(ctr_excel_list[j])
		if (len(ctr_excel_list[j][overview_page][2]) != 12):
			print "Wrong number of columns on " + directory_lang[j].strip().upper() + " menu than expected on Overview, you might be using the wrong CTR version"
			exit(1)
		if (len(ctr_excel_list[j][(overview_page - 1)]) != 23):
			print "Wrong number of rows on " + directory_lang[j].strip().upper() + " menu than expected on Menu Language, you might be using the wrong CTR version"
			exit(1)
		for i in range(5, len(ctr_excel_list[j][overview_page])): 			#gets Overview for each menu (subcategories, genres, and their config info)
			overview_item = ctr_excel_list[j][overview_page][i]
			del overview_item[0]
			if (len(overview_item[0]) > 0):
				menu_cataList.append(category_item)
				category_item = []
				category_item.append(overview_item)
			else: category_item.append(overview_item)
		menu_cataList.append(category_item)
		del menu_cataList[0]
		cataList.append(menu_cataList)										#cataList[ctr_lang_menu][main_cat][sub_cat][config_info]
		for sheet in range((overview_page + 1), total_sheets): 				#gets Sheets with menu-items for each menu (Movies, TV, Music, etc)
			menu_sheet_list = []
			for k in range(1, len(ctr_excel_list[j][sheet])):
				if (ctr_excel_list[j][sheet][k][1] != ""):
					menu_item = ctr_excel_list[j][sheet][k]
					menu_sheet_list.append(menu_item)
			menu_ctr_list.append(menu_sheet_list)
		menu_metadata.append(menu_ctr_list) 								#menu_metadata[ctr_lang_menu][sheet][row][cell]

	main_menu_length = len(cataList[0])
	flag = "f"
	indent = 2
	if (os.path.exists(__Airline_OutputDir + "/config" + __Demo + "/analist.txt")): temp_list = BuildList(__Airline_OutputDir + "/config" + __Demo + "/analist.txt")
	else: temp_list = ""
	GetBulkFiles(".png", "images", "images")
	GetBulkFiles(".png", "images/icons", "images/icons")
	if ("L10" in player_type):
		GetBulkFiles(".png", "imagesL10", "images_L10")
		GetBulkFiles(".png", "imagesL10/icons", "images_L10/icons")
	if (calibration == "yes"): GetBulkFiles(".png", "images/calibration", "images/calibration")
	f.write("<menuitem> #Main Menu\n")
	f.write("\t<title>Main Menu</title>\n")
	if (menu_length > 1):
		f.write("\t<itemcount>" + str(menu_length) + "</itemcount>\n")
		if (background == "yes"):
			f.write("\t<image>bg-a1.png</image>\n")
	if (start_up_ad != ""):
		f.write("\t<preAction>\n")
		f.write(((indent) * "\t") + "<command>" + start_up_ad + " </command>\n")
		f.write("\t</preAction>\n")
	for l in range(menu_length):
		c_place = 0
		if (len(menu_metadata[l][0][0]) != 48):
			print "Wrong number of columns on " + directory_lang[l].strip().upper() + " menu than expected, you might be using the wrong CTR version"
			exit(1)
		net = 0
		for ie in range(len(cataList[l])):
			if ("Internet" in cataList[l][ie][0][0]): net += 1
		if ((len(menu_metadata[l]) + net) != main_menu_length):
			print "The number of categories(sheets) on the CTR for the " + directory_lang[l].strip().upper() + " menu are different than are listed in the Overview"
			exit(1)
		if (menu_length > 1):
			f.write("\t<menuitem>#" + menu_lang_text[l].strip() + "\n")
			f.write((indent * "\t") + "<title>" + menu_lang_text[l].strip() + "</title>\n")
		f.write((indent * "\t") + "<itemcount>" + str(main_menu_length) + "</itemcount>\n")
		if (background == "yes"): f.write((indent * "\t") + "<image>bg-a2.png</image>\n")
		if (after_lang_ad != ""):
			f.write((indent * "\t") + "<preAction>\n")
			f.write(((indent+1) * "\t") + "<command>" + after_lang_ad + " </command>\n")
			f.write((indent * "\t") + "</preAction>\n")
		if (calibration == "yes"):
			f.write((indent * "\t") + "<preAction>\n")
			f.write(((indent+1) * "\t") + "<command>/bin/calibrate</command>\n")
			f.write((indent * "\t") + "</preAction>\n")
		f.write((indent * "\t") + "<flag>t</flag>\n")
		menu_category_subtext = ""
		for c in range(main_menu_length):
			if ("Internet" in cataList[menuLangENG][c][0][0]):
				see = c - c_place
				c_place += 1
			else: see = c - c_place
			f.write((indent * "\t") + "<menuitem> #" + AmIaFloat(cataList[menuLangENG][c][0][0]).strip() + "\n")
			f.write(((indent+1) * "\t") + "<title>" + AmIaFloat(cataList[l][c][0][0]).split('(')[0].strip() + "</title>\n")
			menu_category_subtext = AmIaFloat(cataList[l][c][0][0]).replace(AmIaFloat(cataList[l][c][0][0]).split('(')[0],"",1).strip()
			menu_category_subtext = menu_category_subtext[1:-1]
			category_type = AmIaFloat(cataList[l][c][0][5]).strip().lower()
			itemcount = 0
			all_videos = AmIaFloat(cataList[l][c][0][2]).strip().lower()
			if (all_videos == "yes"):
				all_videos_yes = 1
			else: all_videos_yes = 0
			if (menu_category_subtext != ""): f.write(((indent+1) * "\t") + "<subText>" + menu_category_subtext + "</subText>\n")
			if (category_type == "movies" or category_type == "tv"):
				f.write(((indent+1) * "\t") + "<icon>/content/menu/images/icons/" + AmIaFloat(cataList[l][c][0][3]).strip() + ".png</icon>\n")
				subtitle_list = ""
				subcategories = {}
				subcategory_itemcount = {}
				all_movies = {}
				writeMe = {}
				lang_start_cell = 9
				for i in range(0,len(menu_metadata[l][see])):
					if (AmIaFloat(menu_metadata[l][see][i][30]).lower() != "none" and AmIaFloat(menu_metadata[l][see][i][30]) != ""):
						ad1 = AmIaFloat(menu_metadata[l][see][i][30])
					else: ad1 = ""
					if (AmIaFloat(menu_metadata[l][see][i][31]).lower() != "none" and AmIaFloat(menu_metadata[l][see][i][31]) != ""):
						ad2 = menu_metadata[l][see][i][31]
					else: ad2 = ""
					if (ad1 != "" or ad2 != ""):
						if (os.path.exists(__Airline_OutputDir + "config" + __Demo + "/adlist.txt")): avail_ad_list = BuildList(__Airline_OutputDir + "config" + __Demo + "/adlist.txt")
						else: avail_ad_list = ""
						ad_list = GetAdList(ad1, ad2)
					else: ad_list = ""
					subcategory = AmIaFloat(menu_metadata[l][see][i][4]).strip()
					itemcount += 1
					if (airline_name == "ana" or airline_name == "thatana"):
						datecode = xlrd.xldate_as_tuple(menu_metadata[l][see][i][2], 0)
						date = "-" + '%s-%s-%s' % (datecode[1], datecode[2], datecode[0])
					else: date = ""
					new_holdover = AmIaFloat(menu_metadata[l][see][i][3]).rstrip('"').lstrip('"').strip().replace("#","@")
					if (new_holdover.lower() == "h"): holder_new = "holdover"
					else: holder_new = "new"
					title = AmIaFloat(menu_metadata[l][see][i][7])
					episode = AmIaFloat(menu_metadata[l][see][i][8])
					english_title = AmIaFloat(menu_metadata[l][see][i][5])
					english_episode = AmIaFloat(menu_metadata[l][see][i][6])
					if (english_episode != ""): dash = "-"
					else: dash = ""
					if (not all_movies.has_key(title + episode)): all_movies[title + episode] = ""
					if (menu_metadata[l][see][i][26] != "" ): duration = AmIaFloat(menu_metadata[l][see][i][26])
					else: duration = ""
					if (duration_text[l] != "" and duration != ""): duration = duration_text[l].strip() + " " + duration + " " + min[l].strip()
					elif (duration != ""): duration = duration + " " + min[l].strip()
					rating = AmIaFloat(menu_metadata[l][see][i][25]).strip()
					if (rating_text[l] != "" and rating != ""): rating = rating_text[l].strip() + " " + rating
					language_list = GetLanguages(menu_metadata[l][see][i])
					if (language_text[l] != ""): language_list = language_text[l].strip() + " " + language_list
					genre = AmIaFloat(menu_metadata[l][see][i][22]).strip()
					if (AmIaFloat(menu_metadata[l][see][i][23]).strip() != ""):
						genre = genre + " / " + AmIaFloat(menu_metadata[l][see][i][23]).strip()
						if (AmIaFloat(menu_metadata[l][see][i][24]).strip() != ""): genre = genre + " / " + AmIaFloat(menu_metadata[l][see][i][24]).strip()
					cast = AmIaFloat(menu_metadata[l][see][i][27]).rstrip('"').lstrip('"').strip()
					synopsis = AmIaFloat(menu_metadata[l][see][i][28]).rstrip('"').lstrip('"').strip()
					edit_type = AmIaFloat(menu_metadata[l][see][i][32]).rstrip('"').lstrip('"').strip().lower()
					if (edit_type != ""):
						if (edit_type in __EditTypeMap): edit_type = __EditTypeMap[edit_type]
						else:
							print edit_type.encode('utf-8') + " Edit type not found for " + title.encode('utf-8')
							exit(1)
					content_provider = AmIaFloat(menu_metadata[l][see][i][35]).rstrip('"').lstrip('"').strip()
					source_filepath = AmIaFloat(menu_metadata[l][see][i][38]).rstrip('"').lstrip('"').strip()
					if (AmIaFloat(menu_metadata[l][see][i][29]).rstrip('"').lstrip('"') != ""):
						synopsis = synopsis + "</span><br/><span style=\"font-weight:normal;font-size:13pt\">" + AmIaFloat(menu_metadata[l][see][i][29]).rstrip('"').lstrip('"')
					if (not subcategories.has_key(subcategory)):
						subcategories[subcategory] = ""
						subcategory_itemcount[subcategory] = 0
					if (len(subcategory_itemcount) > (len(cataList[l][c]) - all_videos_yes)):
						print "The are more sub-categories for " + AmIaFloat(cataList[menuLangENG][c][0][0]).strip().encode('ascii', 'ignore') + " in the " + directory_lang[l].strip().upper() + " menu than is listed in the Overview"
						exit(1)
					synop_basefile = AmIaFloat(cataList[l][c][(len(subcategory_itemcount) - 1)][6]).strip()
					if (episode != "" or english_episode != ""): synop_basefile = "TVSYNOPBASE"
					subcategory_type = AmIaFloat(cataList[l][c][(len(subcategory_itemcount) - 1)][5]).strip().lower()
					if (subcategory.strip() != ""):
						subcategory_itemcount[subcategory] += 1
						if (AmIaFloat(cataList[l][c][0][4]).strip() == "no-sub"):
							print "You have no-sub listed in the Overview for " + AmIaFloat(cataList[menuLangENG][c][0][0]).strip().encode('ascii', 'ignore') + " for the " + directory_lang[l].strip().upper() + " menu \n And you have a subcategory listed on menu-item " + english_title.encode('ascii', 'ignore') + " - " + english_episode.encode('ascii', 'ignore')
							exit(1)
					else:
						if (AmIaFloat(cataList[l][c][0][4]).strip() != "no-sub"):
							print "You have no subcategory listed on menu-item " + english_title.encode('ascii', 'ignore') + " - " + english_episode.encode('ascii', 'ignore')+ " \n But you have don't no-sub listed in the Overview for " + cataList[menuLangENG][c][0][0].strip().encode('ascii', 'ignore') + " for the " + directory_lang[l].strip().upper() + " menu"
							exit(1)
					if (subcategory_type == "music"):
						subcategory_itemcount[subcategory] = 0
						subcategories[subcategory] += ((indent+2) * "\t") + "<actionGroup>\n"
						indent += 2
						subcategories[subcategory] += ((indent+1) * "\t") + "<title>" + play_text[l].strip() + "</title>\n"
						WriteMusicCat(title.lower())
						indent -= 2
						subcategories[subcategory] += ((indent+2) * "\t") + "</actionGroup>\n"
					elif (subcategory_type == "games"):
						if (source_filepath == ""):
							print "Filename for " + english_title.encode('ascii', 'ignore') + " in " + AmIaFloat(cataList[menuLangENG][c][0][0]).strip() + " for the " + directory_lang[l].strip().upper() + " menu is missing."
							exit(1)
						indent += 1
						Games(directory_lang[l].strip())
						GetSynop(directory_lang[l].strip(), subcategory_type)
						indent -= 1
					else:
						if (__QA.lower() == "qa2"):
							video_filename_langs = GetFileNameLanguages(menu_metadata[menuLangENG][see][i])
							if (source_filepath == ""): video_filepath = GetVideoFileName(video_dir, 6, 5, 38)
							else: video_filepath = source_filepath.strip()
							video_splits = video_filepath.split("/")
							video_filename = video_splits[-1].replace(".enc","")
							if (video_filepath != "MISSINGVIDEO"):
								if (not video_filepath in rsync_video_list): rsync_video_list.append(video_filepath)
							else: 
								fvid.write(english_title + dash + english_episode + " in " + cataList[menuLangENG][c][0][0].strip().encode('ascii', 'ignore') + " for the " + directory_lang[l].strip().upper() + " menu. Expecting " + holder_new + " title:\n")
								fvid.write(TitleToFilename(english_title.replace("'", "").lower().title()) + dash + TitleToFilename(english_episode.replace("'", "").lower().title()) + date + edit_type + video_filename_langs + ".mkv\n\n")
						else: video_filename = "MISSINGVIDEO"
						if (video_filename != "MISSINGVIDEO"): readXL[l].get_sheet(see + 6).write(i + 1, 38, video_filepath)
						MenuItem(menu_metadata[l][see][i], directory_lang[l].strip(), AmIaFloat(cataList[l][c][0][7]).strip())
						GetImage(english_title, english_episode, image_directory)
						GetSynop(directory_lang[l].strip(), subcategory_type)
				if (AmIaFloat(cataList[l][c][0][4]).strip() != "no-sub" and len(subcategory_itemcount) < (len(cataList[l][c]) - all_videos_yes)):
						print "The are less sub-categories for " + AmIaFloat(cataList[menuLangENG][c][0][0]).strip().encode('ascii', 'ignore') + " in the " + directory_lang[l].strip().upper() + " menu than is listed in the Overview"
						exit(1)
				if (AmIaFloat(cataList[l][c][0][4]).strip() == "no-sub"): WriteToMml(writeMe)
				else:
					WriteGenresToMml(subcategories, AmIaFloat(cataList[l][c][0][4]).strip(), len(subcategory_itemcount))
					if(all_videos == "yes"):
						if (category_type == "tv"): all_text = all_videos_text[l].strip()
						else: all_text = all_movies_text[l].strip()
						WriteAllToMml(all_movies, AmIaFloat(cataList[l][c][len(subcategory_itemcount)][4]).strip())
				f.write((indent * "\t") + "</menuitem>\n")
			elif (category_type == "music" or category_type == "books"):
				f.write(((indent+1) * "\t") + "<icon>/content/menu/images/icons/" + AmIaFloat(cataList[l][c][0][3]).strip() + ".png</icon>\n")
				f.write(WriteMusicCat(category_type))
				f.write((indent * "\t") + "</menuitem>\n")
			elif (category_type == "internet"):
				WriteInternetCat()
			elif (category_type == "magazine"):
				writeMe = {}
				itemcount = 0
				f.write(((indent+1) * "\t") + "<icon>/content/menu/images/icons/" + AmIaFloat(cataList[l][c][0][3]).strip() + ".png</icon>\n")
				for i in range(0,len(menu_metadata[l][see])):
					itemcount += 1
					title = AmIaFloat(menu_metadata[l][see][i][7]).rstrip('"').lstrip('"').strip().replace("#","@")
					episode = AmIaFloat(menu_metadata[l][see][i][8]).rstrip('"').lstrip('"').strip().replace("#","@")
					english_title = AmIaFloat(menu_metadata[l][see][i][5]).rstrip('"').lstrip('"').strip().replace("#","@")
					english_episode = AmIaFloat(menu_metadata[l][see][i][6]).rstrip('"').lstrip('"').strip().replace("#","@")
					GetImage(english_title, english_episode, image_directory)
					WriteMagazineCat()
				WriteToMml(writeMe)
				f.write((indent * "\t") + "</menuitem>\n")
			elif (category_type == "ads" and os.path.exists(__Airline_OutputDir + "config" + __Demo + "/" + TitleToFilename(AmIaFloat(cataList[menuLangENG][c][0][0].split('(')[0]).strip() + str(l + 1)) + ".txt")):
				synop_basefile = AmIaFloat(cataList[l][c][0][6]).strip()
				ad_english_category = AmIaFloat(cataList[menuLangENG][c][0][0]).split('(')[0].strip()
				BulkAds(ad_english_category, directory_lang[l].strip())
			elif (category_type == "survey"):
				writeMe = {}
				itemcount = 1
				f.write(((indent+1) * "\t") + "<icon>/content/menu/images/icons/" + AmIaFloat(cataList[l][c][0][3]).strip() + ".png</icon>\n")
				GetImage(TitleToFilename(AmIaFloat(cataList[menuLangENG][c][0][0]).split('(')[0]).strip(), "", image_directory)
				WriteSurveyCat(AmIaFloat(cataList[menuLangENG][c][0][0]).split('(')[0].strip())
				WriteToMml(writeMe)
				f.write((indent * "\t") + "</menuitem>\n")
			else:
				writeMe = {}
				f.write(((indent+1) * "\t") + "<icon>/content/menu/images/icons/" + AmIaFloat(cataList[l][c][0][3]).strip() + ".png</icon>\n")
				for i in range(0,len(menu_metadata[l][see])):
					itemcount += 1
					title = AmIaFloat(menu_metadata[l][see][i][4]).strip()
					if (category_type == "podcasts"):
						GetImage(title, song, image_directory)
						Podcasts(AmIaFloat(cataList[l][c][0][4]).strip().lower())
					elif (category_type == "games"):
						title = AmIaFloat(menu_metadata[l][see][i][4]).rstrip('"').lstrip('"').strip().replace("#","@")
						english_title = AmIaFloat(menu_metadata[l][see][i][3]).rstrip('"').lstrip('"').strip().replace("#","@")
						english_episode = ""
						synopsis = AmIaFloat(menu_metadata[l][see][i][5]).rstrip('"').lstrip('"').strip().replace("#","@")
						if (AmIaFloat(menu_metadata[l][see][i][6]) != ""):
							synopsis = synopsis + "</span><br/><span style=\"font-weight:normal;font-size:13pt\">" + AmIaFloat(menu_metadata[l][see][i][6]).rstrip('"').lstrip('"')
						synop_basefile = AmIaFloat(cataList[l][c][0][6]).strip()
						source_filepath = AmIaFloat(menu_metadata[l][see][i][8]).rstrip('"').lstrip('"').strip()
						if (source_filepath == ""):
							print "Filename for " + english_title.encode('ascii', 'ignore') + " in " + AmIaFloat(cataList[menuLangENG][c][0][0]).strip() + " for the " + directory_lang[l].strip().upper() + " menu is missing."
							exit(1)
						Games(directory_lang[l].strip())
						GetImage(english_title , english_episode, image_directory)
						GetSynop(directory_lang[l].strip(), AmIaFloat(cataList[l][c][0][5]).strip())
					else:
						new_holdover = AmIaFloat(menu_metadata[l][see][i][3]).rstrip('"').lstrip('"').strip().replace("#","@")
						song = AmIaFloat(menu_metadata[l][see][i][5]).rstrip('"').lstrip('"').strip().replace("#","@")
						english_title = AmIaFloat(menu_metadata[l][see][i][7]).rstrip('"').lstrip('"').strip().replace("#","@")
						english_episode = AmIaFloat(menu_metadata[l][see][i][8]).rstrip('"').lstrip('"').strip().replace("#","@")
						source_filepath = AmIaFloat(menu_metadata[l][see][i][10]).rstrip('"').lstrip('"').strip()
						dash = "-"
						flag = "a"
						edit_type = ""
						if (__QA.lower() == "qa2"):
							video_filename_langs = "ENG"
							if (source_filepath == ""): video_filepath = GetVideoFileName(musicvideo_dir, 8, 7, 10)
							else: video_filepath = source_filepath.strip()
							video_splits = video_filepath.split("/")
							video_filename = video_splits[-1].replace(".enc","")
						else: video_filename == "MISSINGVIDEO"
						GetImage(title, song, image_directory)
						if (video_filename != "MISSINGVIDEO"): readXL[l].get_sheet(see + 6).write(i + 1, 10, video_filepath)
						ad_list = GetAdList("", menu_metadata[l][see][i][6])
						NoSynopItem(title + " - " + song, english_title + " - " + english_episode, AmIaFloat(cataList[l][c][0][5]).strip().lower())
				WriteToMml(writeMe)
				flag = "f"
				f.write((indent * "\t") + "</menuitem>\n")
		if (len(menu_lang_text) > 1): f.write(((indent-2) * "\t") + "</menuitem>\n")
	f.write("</menuitem>\n")
	f.close()
	fvid.close()
	for i in range(len(readXL)):
		os.remove(ctr_filename[i][0])
		time.sleep(4)
		readXL[i].save(ctr_filename[i][0])
	if (len(__MissingFiles) > 0): 
		print "Missing Files:"
		for i in __MissingFiles:
			print i
		exit(1)
	else: print "Good news, no issues! Have a victory cup of coffee!"
	if (__QA.lower() == "qa2"):
		for i in range(len(rsync_video_list)):
			rsync_file = rsync_video_list[i].split("/")
			rsync_cmd = "rsync -avh --progress " + rsync_video_list[i] + " " + __OutputDir + "/videos/" + rsync_file[-1].replace(".enc", "")
			if (os.path.exists(rsync_video_list[i])): 
				os.system(rsync_cmd)
				time.sleep(4)
			else: ferr.write("Video file does not exists for " + rsync_video_list[i] + "\n")
	time.sleep(4)
	if (music_directory != ""):
		music_source_path = "172.16.40.24:/root/Music/" + __Year + "/" + __Month + "/" + music_directory + "/"
		rsync_cmd = "rsync -avh --progress --delete --exclude '*.xls*' " + music_source_path + " " + __OutputDir + "/audio/"
		if (os.path.exists("root@" + music_source_path)): os.system(rsync_cmd)
		else: ferr.write("Music directory does not exist at source: " + music_source_path + "\n")
	else: ferr.write("No music directory listed\n")
	ferr.close()