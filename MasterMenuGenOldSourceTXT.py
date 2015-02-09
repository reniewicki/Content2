# coding=utf-8

import codecs, os.path, sys, re, shutil, time, getpass, os, distutils, random
reload(sys)

# GenerationDir - the directory that contains the library directories
__GenerationDir = "C:\\Users\\" + getpass.getuser() + "\\Dropbox\\Content Share\\"

# GraphicsLibDir - the directory containing all the graphics directories for items
__GraphicsLibDir = "Library-Graphics_ready\\"

# Globals
__MissingFiles = []

sys.setdefaultencoding('utf-8')

__LanguageMap = {	'English' : 'ENG',
					'Arabic' : 'ARA',
					'Arabic' : 'ARB',
					'Dutch' : 'DUT',
					'Russian' : 'RUS',
					'German' : 'GER',
					'Chinese' : 'CHI',
					'French' : 'FRE',
					'Parisian French' : 'PFR',
					'Canadian French' : 'CFR',
					'Japanese' : 'JAP',
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
					'Engels' : 'ENE',
					'Nederlands' : 'NED',
					'Vietnamese' : 'VIE',
					'Bosnian' : 'BOS',
					'Thai' : 'THA',
					'Mandarin' : 'MAN',
					'Mandalin' : 'MAN',
					'Cantonese' : 'CAN',
					'Thai' : 'THA'}

def titleToFilename(title):
	retVal = title.strip().encode('utf-8')
	retVal = retVal.replace("&", "And")
	retVal = retVal.replace("é", "e")
	retVal = re.sub(r'[\W]', r"", retVal)

	for i in range(0,len(retVal)-1):
		if (retVal[i] == " " and i < len(retVal)-2):
			tList = list(retVal)
			tList[i+1] = tList[i+1].upper()
			retVal = "".join(tList)
	retVal = retVal.replace(" ", "")
	return retVal.encode('utf-8')

def BuildList(filename):
	retList = {}
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
	
def WriteToMml(itemList):
	#keys = itemList.keys()
	f.write(((indent+1) * "\t") + "<itemcount> " + str(itemcount) + "</itemcount>\n")
	f.write(((indent+1) * "\t") + "<flag>" + flag + "</flag>\n")
	if (background == "yes"):
		f.write(((indent+1) * "\t") + "<image>bg-a3.png</image>\n")
	for i in range(0, len(itemList)):
		f.write(itemList[i])
		
def WriteGenresToMml(itemList, icon, allVideos):
	k = 0
	if(allVideos == "yes"):
		itemcount = (len(categoryKeys) + 1)
	else:
		itemcount = len(categoryKeys)
	r = 0
	for key in categoryKeys:
		if (len(key) < 1):
			itemcount += (categoryNumbers[key] - 1)
		else:
			continue
	f.write(((indent+1) * "\t") + "<itemcount> " + str(itemcount) + "</itemcount>\n")
	if (len(categoryKeys) < 2 or "poster" in icon):
		f.write(((indent+1) * "\t") + "<flag>" + flag + "</flag>\n")
	if (background == "yes"):
		f.write(((indent+1) * "\t") + "<image>bg-a3.png</image>\n")
	for key in categoryKeys:
		catSubText = ""
		if (l != menuLangENG):
			commentTitle = englishKeys[y][k] + " __ " + key
		else:
			commentTitle = key
		if ("(" in key and ")" in key):
			localTitle = key.split('(')[0].strip()
			catSubText = key.replace(key.split('(')[0],"",1).strip()
			catSubText = catSubText[1:-1]
		#elif (len(key) > 18):
		#	for i in range(1, 17):
		#		if (key[(18 - i)] == " "):
		else:
			localTitle = key
		if (len(key) > 1):
			f.write(((indent+1) * "\t") + "<menuitem> #" + commentTitle + "\n")
			f.write(((indent+2) * "\t") + "<title>" + localTitle + "</title>\n")
			if (catSubText != ""):
				f.write(((indent+2) * "\t") + "<subText>" + catSubText + "</subText>\n")
			if (icon.lower() == "random-poster"):
				for i in range(0, len(movieItemList[m])):
					if (movieItemList[m][i][4].rstrip('"').lstrip('"').strip().replace("#","@") == key):
						r = i
						break
				poster = titleToFilename(movieItemList[m][r][5].rstrip('"').lstrip('"').strip().replace("#","@") + movieItemList[m][r][6].rstrip('"').lstrip('"').strip().replace("#","@"))
				f.write(((indent+2) * "\t") + "<poster>/content/menu/images/interface/" + poster.lower() + ".png</poster>\n")
			elif (icon.lower() == "poster"):
				poster = titleToFilename(cataList[c][menuLangENG].strip() + englishKeys[y][k])
				GetImage(cataList[c][menuLangENG].strip(), englishKeys[y][k], imageDir)
				f.write(((indent+2) * "\t") + "<poster>/content/menu/images/interface/" + poster.lower() + ".png</poster>\n")
			else:
				if (icon.lower() == "icon"):
					icon = titleToFilename(cataList[c][menuLangENG].strip() + englishKeys[y][k])
				f.write(((indent+2) * "\t") + "<icon>/content/menu/images/icons/" + icon + ".png</icon>\n")
			if (not "digetunes" in itemList[key]):
				f.write(((indent+2) * "\t") + "<flag>f</flag>\n")
			if (categoryNumbers[key] > 0):
				f.write(((indent+2) * "\t") + "<itemcount>" + str(categoryNumbers[key]) + "</itemcount>\n")
			if (background == "yes"):
				f.write(((indent+2) * "\t") + "<image>bg-a3.png</image>\n")
			f.write(itemList[key])
			f.write(((indent+1) * "\t") + "</menuitem>\n")
			k += 1
	if (itemList.has_key("")):
		f.write(itemList[""])
		
def WriteAllToMml(itemList, icon, AllTitle):
	keys = itemList.keys()
	keys.sort()
	f.write(((indent+1) * "\t") + "<menuitem> #All Movies\n")
	f.write(((indent+2) * "\t") + "<title>" + AllTitle + "</title>\n")
	if (icon.lower() == "random-poster"):
		r = randint(0, len(movieItemList[m]))
		poster = titleToFilename(movieItemList[m][r][1].rstrip('"').lstrip('"').strip().replace("#","@") + movieItemList[m][r][2].rstrip('"').lstrip('"').strip().replace("#","@"))
		f.write(((indent+2) * "\t") + "<poster>/content/menu/images/interface/" + poster.lower() + ".png</poster>\n")
	elif (icon.lower() == "poster"):
		poster = titleToFilename(cataList[c][menuLangENG].strip() + englishKeys[y][k])
		GetImage(cataList[c][menuLangENG].strip(), "AllMovies", imageDir)
		f.write(((indent+2) * "\t") + "<poster>/content/menu/images/interface/" + poster.lower() + ".png</poster>\n")
	else:
		if (icon.lower() == "icon"):
			icon = titleToFilename(cataList[c][menuLangENG].strip() + englishKeys[y][k])
		f.write(((indent+2) * "\t") + "<icon>/content/menu/images/icons/" + icon + ".png</icon>\n")
	f.write(((indent+2) * "\t") + "<flag>f</flag>\n")
	f.write(((indent+2) * "\t") + "<itemcount>" + str(itemcount) + "</itemcount>\n")
	if (background == "yes"):
		f.write(((indent+2) * "\t") + "<image>bg-a3.png</image>\n")
	for key in keys:
		f.write(itemList[key])
	f.write(((indent+1) * "\t") + "</menuitem>\n")
	
def WriteMusicCat(digetunes):
	itemAddon = ""
	itemAddon += ((indent+1) * "\t") + "<action>\n"
	itemAddon += ((indent+2) * "\t") + "<command>!digetunes --music-subdir=" + digetunes + "</command>\n"
	itemAddon += ((indent+1) * "\t") + "</action>\n"
	categories[category] += itemAddon
	return itemAddon
	
def WriteInternetCat():
	f.write(((indent+1) * "\t") + "<icon>/content/menu/images/icons/" + cataList[c][p].strip() + ".png</icon>\n")
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
	
def MenuItem(splits, menuLang, videoType, itemSubText, missingVideo):
		itemAddon = ""
		if (len(episode) > 0):
			localEpisode = " - " + episode
			localEnglishEpisode = " - " + englishEpisode
		else:
			localEpisode = ""
			localEnglishEpisode = ""
		if (l != menuLangENG):
			commentTitle = englishTitle + localEnglishEpisode + " __ " + title + localEpisode
		else:
			commentTitle = englishTitle + localEnglishEpisode
			
		itemAddon += ((indent+2) * "\t") + "<menuitem> #" + commentTitle + "\n"
		itemAddon += ((indent+3) * "\t") + "<title>" + title + localEpisode + "</title>\n"
		if (itemSubText != "" and (duration.strip() != "" or rating.strip() != "")):
			itemSubText = itemSubText.replace("$DURATION", duration.strip())
			itemSubText = itemSubText.replace("$RATING", rating.strip())
			itemSubText = itemSubText.replace("$LANGUAGE", languageList.strip())
			itemAddon += ((indent+3) * "\t") + "<subText>" + itemSubText + "</subText>\n"
		itemAddon += ((indent+3) * "\t") + "<poster>/content/menu/images/interface/" + titleToFilename(englishTitle + englishEpisode).lower() + datecode + ".png" + " </poster>\n"
		itemAddon += ((indent+3) * "\t") + "<text>/content/menu/text/" + videoType + "/" + menuLang + "/" + titleToFilename(englishTitle + englishEpisode) + ".txt</text>\n"
		itemAddon += ((indent+3) * "\t") + "<actionGroup>\n"
		itemAddon += ((indent+4) * "\t") + "<title>" + playText[l].strip() + "</title>\n"
		itemAddon += ((indent+4) * "\t") + "<action>\n"
		if (splits[langTabPlace + 1].strip() != "" or splits[langTabPlace + 8] != ""):
			itemAddon += ((indent+5) * "\t") + "<command>play_video %1 -f DejaVuSans:20 -t \"" + title + localEpisode + "\"" + adList + " /content/videos/" + missingVideo + " </command>\n"
			if(splits[langTabPlace + 1] != ""):
				itemAddon += ((indent+5) * "\t") + "<argument>\n"
				itemAddon += ((indent+6) * "\t") + "<title>" + selectLangText[l].strip() + "</title>\n"
				for x in range(langTabPlace, langTabPlace + 6):
					if (splits[x].strip() != ""):
						secondLanguage = splits[x]
						itemAddon += ((indent+7) * "\t") + "<selection>\n"
						itemAddon += ((indent+8) * "\t") + "<title>"+ secondLanguage + " " + audioText[l].strip() + "</title>\n"
						languagenumber = unicode(x - langTabPlace)
						itemAddon += ((indent+8) * "\t") + "<value>-a " + languagenumber + "</value>\n"
						itemAddon += ((indent+7) * "\t") + "</selection>\n"
					else :
						continue
				if (splits[langTabPlace + 8] == ""):
					itemAddon += ((indent+5) * "\t") + "</argument>\n"
					itemAddon += ((indent+4) * "\t") + "</action>\n"
					itemAddon += ((indent+3) * "\t") + "</actionGroup>\n"
					itemAddon += ((indent+2) * "\t") + "</menuitem>\n"
				else:
					itemAddon += ((indent+5) * "\t") + "</argument>\n"
			if (splits[langTabPlace + 8].strip() != ""):
				itemAddon += ((indent+5) * "\t") + "<argument>\n"
				itemAddon += ((indent+6) * "\t") + "<title>" + selectSubText[l].strip() + "</title>\n"
				for u in range(langTabPlace + 8, langTabPlace + 10):
					if (splits[u].strip() != ""):
						itemAddon += ((indent+7) * "\t") + "<selection>\n"
						itemAddon += ((indent+8) * "\t") + "<title>"+ splits[u] + " " + subtitleText[l].strip() + "</title>\n"
						subtitlenumber = unicode(u - (langTabPlace + 8))
						itemAddon += ((indent+8) * "\t") + "<value>-u " + subtitlenumber + "</value>\n"
						itemAddon += ((indent+7) * "\t") + "</selection>\n"
					else :
						continue
				itemAddon += ((indent+7) * "\t") + "<selection>\n"
				itemAddon += ((indent+8) * "\t") + "<title>" + noneText[l].strip() + "</title>\n"
				itemAddon += ((indent+8) * "\t") + "<value> </value>\n"
				itemAddon += ((indent+7) * "\t") + "</selection>\n"
				itemAddon += ((indent+5) * "\t") + "</argument>\n"
				itemAddon += ((indent+4) * "\t") + "</action>\n"
				itemAddon += ((indent+3) * "\t") + "</actionGroup>\n"
				itemAddon += ((indent+2) * "\t") + "</menuitem>\n"
		else :
			itemAddon += ((indent+5) * "\t") + "<command>play_video -t \"" + title + localEpisode + "\"" + adList + " /content/videos/" + missingVideo + " </command>\n"
			itemAddon += ((indent+4) * "\t") + "</action>\n"
			itemAddon += ((indent+3) * "\t") + "</actionGroup>\n"
			itemAddon += ((indent+2) * "\t") + "</menuitem>\n"
		categories[category] += itemAddon
		allMovies[title] += itemAddon
		writeMe[(itemcount - 1)] = itemAddon

def GetVideoFileName(languages):
	filebase = ""
	localTitle = englishTitle.replace("'", "").lower().title() + englishEpisode.replace("'", "").lower().title()
	filebase = airlineID.upper() + "-" + titleToFilename(localTitle) + datecode + languages + ".mkv"
	
	return filebase
	
def GetFileNameLanguages(localSplits):
	langList = ""
	lang = ""
	if (localSplits[langTabPlace].strip() != ""):
		langList += "_"
	for i in range(langTabPlace, langTabPlace + 6):
		if (localSplits[i].strip() != ""):
			lang = localSplits[i].strip()
			if (lang in __LanguageMap):
				langList += __LanguageMap[lang]
			else:
				print lang + " Language code not found for " + title.encode('utf-8')
	if (localSplits[langTabPlace + 7].strip() != ""):
		lang = localSplits[langTabPlace + 7].strip()
		langList += "_" + __LanguageMap[lang]
	if (localSplits[langTabPlace + 8].strip() != ""):
		langList += "_"
	for j in range(langTabPlace + 8, langTabPlace + 11):
		if (localSplits[j].strip() != ""):
			lang = localSplits[j].strip().encode('utf-8')
			lang = re.sub(r'[\W]', r"", lang)
			if (lang in __LanguageMap):
				langList += __LanguageMap[lang].lower()
			else:
				print lang + " Language code not found for " + title.encode('utf-8')
	return langList

def GetLanguages(localSplits, langStart, langFin, subStart, subFin):
	localLang = ""
	localSub = ""
	for x in range(langStart, langFin):
		if (localSplits[x].strip() != ""):
			localLang = localLang + ", " + localSplits[x]
	if (localLang != ""):
		localLang = localLang[2:]
	for g in range(subStart, subFin):
		subList = localSplits[g].strip()
		if (subList.strip() != ""):
			if (localSub.strip() == ""):
				localSub = " (" + subList.strip()
			else:
				localSub = localSub + ", " + subList.strip()
	if (localSub.strip() != ""):
		localSub = localSub + " " + subtitleText[l].strip() + ")"
	languageList = localLang + localSub
	return languageList
	
def GetBulkFiles(ext, input, output):
	if(not os.path.exists(__OutputDir + "/menu/" + output + "/")):
		os.makedirs(__OutputDir + "/menu/" + output + "/")
	if(os.path.exists(os.getcwd() + "\\config\\" + input + "\\")):
		sourceIcons = os.listdir(os.getcwd() + "\\config\\" + input + "\\")
		for files in sourceIcons:
			if files.endswith(ext):
				shutil.copy(os.getcwd() + "\\config\\" + input + "\\" + files,__OutputDir + "/menu/" + output + "/")
	else:
		__MissingFiles.append(os.getcwd()+ "config/" + input + "/ directory is missing")
			
def GetImage(localTitle, localEpisode, directory):
	if(not os.path.exists(__OutputDir + "/menu/images/interface/")):
		os.makedirs(__OutputDir + "/menu/images/interface/")
	if ("L10" in directory):
		if(not os.path.exists(__OutputDir + "/menu/images_L10/interface/")):
			os.makedirs(__OutputDir + "/menu/images_L10/interface/")
	Imagefilebase = titleToFilename(localTitle) + datecode
	ImageFullfilebase = titleToFilename(localTitle + localEpisode) + datecode
	if(os.path.exists(__GenerationDir + __GraphicsLibDir + directory + "\\" + ImageFullfilebase + ".png")):
		shutil.copy((__GenerationDir + __GraphicsLibDir + directory + "\\" + ImageFullfilebase + ".png"), __OutputDir + "/menu/images/interface/"  + ImageFullfilebase.lower() + ".png")
		if ("L10" in directory):
			shutil.copy((__GenerationDir + __GraphicsLibDir + directory + "\\" + ImageFullfilebase + ".png"), __OutputDir + "/menu/images_L10/interface/"  + ImageFullfilebase.lower() + ".png")
	elif(os.path.exists(__GenerationDir + __GraphicsLibDir + directory + "\\" + Imagefilebase + ".png")):
		shutil.copy((__GenerationDir + __GraphicsLibDir + directory + "\\" + Imagefilebase + ".png"), __OutputDir + "/menu/images/interface/"  + ImageFullfilebase.lower() + ".png")
		if ("L10" in directory):
			shutil.copy((__GenerationDir + __GraphicsLibDir + directory + "\\" + Imagefilebase + ".png"), __OutputDir + "/menu/images_L10/interface/"  + ImageFullfilebase.lower() + ".png")
	else:
		__MissingFiles.append(ImageFullfilebase + ".png")
		
def GetSynop(menuLang, videoType, synopBaseFile):
	if(not os.path.exists(__OutputDir + "/menu/text/" + videoType + "/" + menuLang + "/")):
		os.makedirs(__OutputDir + "/menu/text/" + videoType + "/" + menuLang + "/")
	filebase = titleToFilename(englishTitle + englishEpisode)
	if(os.path.exists(__OutputDir + "/config/" + synopBaseFile + ".txt")):
		BASE = codecs.open(__OutputDir + "/config/" + synopBaseFile + ".txt", 'r', 'utf-8').read()
		BASE = BASE.replace("$TITLE", title)
		BASE = BASE.replace("$EPISODE", episode)
		BASE = BASE.replace("$DURATION", duration)
		BASE = BASE.replace("$RATING", rating)
		BASE = BASE.replace("$LANGUAGE", languageList)
		BASE = BASE.replace("$GENRE", genre)
		BASE = BASE.replace("$CAST", cast)
		BASE = BASE.replace("$SYNOPSIS", synopsis)
		outFile = codecs.open(__OutputDir + "/menu/text/" + videoType + "/" + menuLang + "/" + filebase + ".txt", 'w+', 'utf-8')
		outFile.write(BASE)
		outFile.close()
	else:
		print synopBaseFile + ".txt does not exist in " + __OutputDir
		exit()
		
def GetLangText(i):
	configList[i] = configList[i].replace("’", "'")
	return configList[i].split('\t')
	
def Podcasts(image):
	itemAddon = ""
	itemAddon += ((indent+2) * "\t") + "<menuitem> #" + title + "\n"
	itemAddon += ((indent+3) * "\t") + "<title>" + title + "</title>\n"
	itemAddon += ((indent+3) * "\t") + "<poster>/content/menu/images/interface/" + image.lower() + ".png" + "</poster>\n"
	itemAddon += ((indent+3) * "\t") + "<actionGroup>\n"
	itemAddon += ((indent+4) * "\t") + "<title>" + playText[l].strip() + "</title>\n"
	itemAddon += ((indent+4) * "\t") + "<action>\n"
	itemAddon += ((indent+5) * "\t") + "<command>!digetunes -t \"" + title + "\" --book /content/audio/podcasts/" + titleToFilename(title) + " </command>\n"
	itemAddon += ((indent+4) * "\t") + "</action>\n"
	itemAddon += ((indent+3) * "\t") + "</actionGroup>\n"
	itemAddon += ((indent+2) * "\t") + "</menuitem>\n"
	writeMe[(itemcount - 1)] = itemAddon
	
def Games(menuLang):
	itemAddon = ""
	if ("spider" in englishTitle.lower()):
		gameTitle = "Spider"
	else:
		gameTitle = englishTitle
	itemAddon += ((indent+2) * "\t") + "<menuitem> #" + englishTitle + "\n"
	itemAddon += ((indent+3) * "\t") + "<title>" + title + "</title>\n"
	itemAddon += ((indent+3) * "\t") + "<poster>/content/menu/images/interface/" + titleToFilename(englishTitle).lower() + ".png" + "</poster>\n"
	itemAddon += ((indent+3) * "\t") + "<text>/content/menu/text/games/" + menuLang + "/" + titleToFilename(englishTitle) + ".txt" + "</text>\n"
	itemAddon += ((indent+3) * "\t") + "<actionGroup>\n"
	itemAddon += ((indent+4) * "\t") + "<title>" + playText[l].strip() + "</title>\n"
	itemAddon += ((indent+4) * "\t") + "<action>\n"
	itemAddon += ((indent+5) * "\t") + "<command>/content/games/fdg" + titleToFilename(gameTitle) + "/start_game.sh  -l " + menuLang + "/ </command>\n"
	itemAddon += ((indent+4) * "\t") + "</action>\n"
	itemAddon += ((indent+3) * "\t") + "</actionGroup>\n"
	itemAddon += ((indent+2) * "\t") + "</menuitem>\n"
	writeMe[(itemcount - 1)] = itemAddon
	categories[category] += itemAddon
	
def GetAdList(adOne, adTwo):
	ads = ""
	if (adOne != ""):
		if (airlineID != "alaska"):
			ads = " /content/ads/MISSINGAD"
		elif ("bankofamerica" in titleToFilename(adOne).lower()):
			ads = " /content/ads/ASA-BankOfAmerica-30sec_ENG.mkv"
		elif ("shoulder" in titleToFilename(adOne).lower()):
			ads = " /content/ads/ASA-UWMedicine-SportsMedicine-Shoulder30sec_ENG.mkv"
		elif ("travelhealth" in titleToFilename(adOne).lower()):
			ads = " /content/ads/UWTravelHealth_ENG.mkv"
		elif ("sleepclinic" in titleToFilename(adOne).lower()):
			ads = " /content/ads/ASA-HarborviewSleepClinic30_ENG.mkv"
		elif ("issaquah" in titleToFilename(adOne).lower()):
			ads = " /content/ads/ASA-UWMedicine-Issaquah_ENG.mkv"
		elif ("MS" in titleToFilename(adOne)):
			ads = " /content/ads/ASA-UWMedicine-MSCenter30Sec_ENG.mkv"
		elif ("crohns" in titleToFilename(adOne).lower()):
			ads = " /content/ads/ASA-UWChronsDisease-30s_ENG.mkv"
		elif ("midwife" in titleToFilename(adOne).lower()):
			ads = " /content/ads/ASA-UWMedicine-Midwives-2min_ENG.mkv"
		elif ("ravenna" in titleToFilename(adOne).lower()):
			ads = " /content/ads/ASA-UWMedicine-Ravenna_ENG.mkv"
		elif ("concussion" in titleToFilename(adOne).lower()):
			ads = " /content/ads/UWYouthConcussions30s_ENG.mkv"
		elif ("maui" in titleToFilename(adOne).lower()):
			ads = " /content/ads/MauiTour30s_ENG.mkv"
		elif ("belltown" in titleToFilename(adOne).lower()):
			ads = " /content/ads/ASA-UWMedicine-Belltown_ENG.mkv"
		elif ("running" in titleToFilename(adOne).lower()):
			ads = " /content/ads/ASA-UWMedicine-Running30s_ENG.mkv"
		elif ("sports" in titleToFilename(adOne).lower()):
			ads = " /content/ads/ASA-UWMedicine-Running30s_ENG.mkv"
		elif ("bariatric" in titleToFilename(adOne).lower()):
			ads = " /content/ads/ASA-UWMedicineBariatricMedicine30sec_ENG.mkv"
		elif ("expansion" in titleToFilename(adOne).lower()):
			ads = " /content/ads/ASA-UWMedicineExpansion30s_ENG.mkv"
		elif ("hernia" in titleToFilename(adOne).lower()):
			ads = " /content/ads/ASA-UWMedicine-Hernia30sec_ENG.mkv"
		elif ("uwart" in titleToFilename(adOne).lower()):
			ads = " /content/ads/HarborViewArtCenter30s_ENG.mkv"
		elif ("silver" in titleToFilename(adOne).lower()):
			ads = " /content/ads/SilverReefCasino-LittleThings_ENG.mkv"
		elif ("lincoln" in titleToFilename(adOne).lower()):
			ads = " /content/ads/ASA-Lincoln-30sec_ENG.mkv"
		elif ("spine" in titleToFilename(adOne).lower()):
			ads = " /content/ads/HarborviewSpine30s_ENG.mkv"
		else:
			__MissingFiles.append(adOne + " ad is missing")
			ads = " /content/ads/MISSINGAD"
	if (adTwo != ""):
		if (airlineID != "aeroflot"):
			ads += " /content/ads/MISSINGAD"
		else:
			if (adTwo != "" and adTwo.lower() != "none"):
				if (adTwo == "6"):
					aTwo == "06"
				ads += " /content/ads/AFL-Disclaimers8sec16x9-" + adTwo + "andUp_SIL.mkv"
	return ads
	
def BulkAds(adCat, menuLang):
	filebase = titleToFilename(adCat + str(l + 1))
	if (airlineID == "alaska"):
		GetBulkFiles(".txt", "images\\" + filebase + "\\" + menuLang, "text/" + filebase + "/" + menuLang)
	bulkAdList = BuildList(__OutputDir + "/config/" + filebase + ".txt")
	for i in range(0, len(bulkAdList)):
		item = bulkAdList[i].split('\t')
		for j in range(0, len(item)):
			if (item[j].strip() == ""):
				f.write("\t")
			else:
				f.write(item[j].strip())
		f.write("\n")
		
def NoSynopItem(localTitle, localEngTitle, dir):
	itemAddon = ""
	itemAddon += ((indent+2) * "\t") + "<menuitem> #" + localEngTitle + "\n"
	itemAddon += ((indent+3) * "\t") + "<title>" + localTitle + "</title>\n"
	itemAddon += ((indent+3) * "\t") + "<poster>/content/menu/images/interface/" + titleToFilename(localEngTitle).lower() + ".png" + "</poster>\n"
	itemAddon += ((indent+3) * "\t") + "<actionGroup>\n"
	itemAddon += ((indent+4) * "\t") + "<title>" + playText[l].strip() + "</title>\n"
	itemAddon += ((indent+4) * "\t") + "<action>\n"
	itemAddon += ((indent+5) * "\t") + "<command>play_video -t \"" + localTitle + "\"" + adList + " /content/" + dir + "/MISSINGVIDEO </command>\n"
	itemAddon += ((indent+4) * "\t") + "</action>\n"
	itemAddon += ((indent+3) * "\t") + "</actionGroup>\n"
	itemAddon += ((indent+2) * "\t") + "</menuitem>\n"
	writeMe[(itemcount - 1)] = itemAddon
	
if __name__ == "__main__":

	if (len(sys.argv) != 2):
		print "Usage: MasterMenuGen.py <outputdir>"
		print "  Uses a source files and generates the directory structure for "
		print "  the menu if those files are available in the generation dir."
		exit()

	__OutputDir = sys.argv[1]
	if (not os.path.exists(__OutputDir)):
		print "outputdir does not exist: " + __OutputDir
		exit()
	if (not os.path.isdir(__OutputDir)):
		print "outputdir is not a directory: " + __OutputDir
		exit()
	
	__OutputDir = os.path.abspath(__OutputDir)
	if (not os.path.exists(__OutputDir + "/menu/")):
		os.makedirs(__OutputDir + "/menu/")
	f = codecs.open(__OutputDir + "/menu/menugen.mml", 'w+', 'utf-8')
	
	#These should exist in the same place as output directory
	overviewList = BuildList(__OutputDir + "/source/Overview.txt")
	configList = BuildList(__OutputDir + "/config/config.txt")
	menuLangText = GetLangText(0)
	movieItemList = []
	menuLangENG = 0
	for i in range(0, len(menuLangText)):
		movieList = BuildList(__OutputDir + "/source/MovieList" + str(i + 1) + ".txt")
		ItemList = []
		if (menuLangText[i].strip().lower() == "english"):
			menuLangENG = i
		for j in range(0, len(movieList)):
			movieList[j] = movieList[j].replace("’", "'")
			if (movieList[j].strip() != ""):
				item = movieList[j].split('\t')
				ItemList.append(item)
			else:
				movieItemList.append(ItemList)
				ItemList = []
		movieItemList.append(ItemList)
		ItemList = []
	time.sleep(2)
	cataList = []
	for i in range(0, len(overviewList)):
		overviewList[i] = overviewList[i].replace("’", "'")
		overviews = overviewList[i].split('\t')
		cataList.append(overviews)
	
	playText = GetLangText(1)
	selectLangText = GetLangText(2)
	selectSubText = GetLangText(3)
	audioText = GetLangText(4)
	languageText = GetLangText(5)
	subtitleText = GetLangText(6)
	noneText = GetLangText(7)
	durationText = GetLangText(8)
	min = GetLangText(9)
	ratingText = GetLangText(10)
	AllMoviesTitle = GetLangText(11)
	AllVideosTitle = GetLangText(12)
	homepage = configList[15].strip()
	background = configList[14].strip().lower()
	dirLang = GetLangText(13)
	imageDir = configList[16].strip()
	calibration = configList[17].strip().lower()
	airlineID = movieItemList[0][0][1].strip().lower()
	m = 0
	p = (len(menuLangText)+1)
	flag = "f"
	menuSubText = ""
	categoryENGKeys = []
	englishKeys = []
	for i in range(0, len(cataList)):
		if (cataList[i][p+1].strip().lower() != "no-sub" and cataList[i][p+1].strip().lower() != ""):
			z = i + (menuLangENG * len(cataList))
			for x in range(0,len(movieItemList[z])):
				ENGcategory = movieItemList[z][x][4].strip()
				if (not ENGcategory in categoryENGKeys):
					categoryENGKeys.append(ENGcategory)
			englishKeys.append(categoryENGKeys)
			categoryENGKeys = []
	GetBulkFiles(".png", "images", "images")
	GetBulkFiles(".png", "images\\icons", "images/icons")
	if ("L10" in imageDir):
		GetBulkFiles(".png", "images", "images_L10")
		GetBulkFiles(".png", "images\\icons", "images_L10/icons")
	if (calibration == "yes"):
		GetBulkFiles(".png", "images\\calibration", "images/calibration")
	f.write("<menuitem> #Main Menu\n")
	f.write("\t<title>Main Menu</title>\n")
	if (len(menuLangText) > 1):
		f.write("\t<itemcount>" + str(len(menuLangText)) + "</itemcount>\n")
		if (background == "yes"):
			f.write("\t<image>bg-a1.png</image>\n")
	for l in range(0, len(menuLangText)):
		indent = 2
		y = 0
		if (len(menuLangText) > 1):
			f.write("\t<menuitem>#" + menuLangText[l].strip() + "\n")
			f.write((indent * "\t") + "<title>" + menuLangText[l].strip() + "</title>\n")
			indent += 1
		f.write((indent * "\t") + "<itemcount>" + str(len(cataList)) + "</itemcount>\n")
		if (background == "yes"):
			f.write((indent * "\t") + "<image>bg-a2.png</image>\n")
		if (airlineID == "aeroflot"):
			f.write((indent * "\t") + "<preAction>\n")
			f.write(((indent+1) * "\t") + "<command>play_video -unstoppable /content/ads/MISSINGAD </command>\n")
			f.write((indent * "\t") + "</preAction>\n")
		elif (airlineID == "gulf air"):
			f.write((indent * "\t") + "<preAction>\n")
			f.write(((indent+1) * "\t") + "<command>play_video /content/GFA-GulfAirIntroVideoV3WhiteLogo_ENG.mkv </command>\n")
			f.write((indent * "\t") + "</preAction>\n")
		elif (airlineID == "oai"):
			f.write((indent * "\t") + "<preAction>\n")
			f.write(((indent+1) * "\t") + "<command>!billboard /content/StartupWarningNA2.png 10</command>\n")
			f.write((indent * "\t") + "</preAction>\n")
		elif (calibration == "yes"):
			f.write((indent * "\t") + "<preAction>\n")
			f.write(((indent+1) * "\t") + "<command>/bin/calibrate</command>\n")
			f.write((indent * "\t") + "</preAction>\n")
		f.write((indent * "\t") + "<flag>t</flag>\n")
		for c in range(0, len(cataList)):
			if (l != menuLangENG):
				commentTitle = cataList[c][menuLangENG].strip() + " __ " + cataList[c][l].strip()
			else:
				commentTitle = cataList[c][l].strip()
			f.write((indent * "\t") + "<menuitem> #" + commentTitle + "\n")
			f.write(((indent+1) * "\t") + "<title>" + cataList[c][l].split('(')[0].strip() + "</title>\n")
			menuSubText = cataList[c][l].replace(cataList[c][l].split('(')[0],"",1).strip()
			menuSubText = menuSubText[1:-1]
			if (menuSubText != ""):
				f.write(((indent+1) * "\t") + "<subText>" + menuSubText + "</subText>\n")
			if (cataList[c][(p+2)].strip().lower() == "movies" or cataList[c][(p+2)].strip().lower() == "tv"):
				f.write(((indent+1) * "\t") + "<icon>/content/menu/images/icons/" + cataList[c][p].strip() + ".png</icon>\n")
				subList = ""
				categories = {}
				categoryNumbers = {}
				allMovies = {}
				writeMe = {}
				itemcount = 0
				catacount = 0
				langTabPlace = 9
				categoryKeys = []
				for i in range(0,len(movieItemList[m])):
					adList = GetAdList(movieItemList[m][i][29].strip(), movieItemList[m][i][30].strip())
					itemcount += 1
					category = movieItemList[m][i][4].strip()
					if(len(category) < 1):
						indent -= 1
					if (not categories.has_key(category)):
						categories[category] = ""
						categoryNumbers[category] = 0
						categoryKeys.append(category)
						catacount += 1
					if (airlineID == "ana"):
						datecode = "_" + movieItemList[m][i][2].strip().replace("/","-")
					else:
						datecode = ""
					title = movieItemList[m][i][7].rstrip('"').lstrip('"').strip().replace("#","@")
					episode = movieItemList[m][i][8].rstrip('"').lstrip('"').strip().replace("#","@")
					englishTitle = movieItemList[m][i][5].rstrip('"').lstrip('"').strip().replace("#","@")
					englishEpisode = movieItemList[m][i][6].rstrip('"').lstrip('"').strip().replace("#","@")
					
					if (not allMovies.has_key(title)):
						allMovies[title] = ""
					duration = movieItemList[m][i][25].strip()
					if (durationText[l] != "" and duration != ""):
						duration = durationText[l].strip() + " " + duration + " " + min[l].strip()
					elif (duration != ""):
						duration = duration + " " + min[l].strip()
					rating = movieItemList[m][i][24].strip()
					if (ratingText[l] != "" and rating != ""):
						rating = ratingText[l].strip() + " " + rating
					languageList = GetLanguages(movieItemList[m][i], langTabPlace, (langTabPlace + 6), (langTabPlace + 7), (langTabPlace + 11))
					if (languageText[l] != ""):
						languageList = languageText[l].strip() + " " + languageList
					genre = movieItemList[m][i][21].strip()
					if (movieItemList[m][i][22].strip() != ""):
						genre = genre + " / " + movieItemList[m][i][22].strip()
						if (movieItemList[m][i][23].strip() != ""):
							genre = genre + " / " + movieItemList[m][i][23].strip()
					cast = movieItemList[m][i][26].rstrip('"').lstrip('"').strip()
					synopsis = movieItemList[m][i][27].rstrip('"').lstrip('"').strip()
					if (movieItemList[m][i][28].rstrip('"').lstrip('"') != ""):
						synopsis = synopsis + "</span><br/><span style=\"font-weight:normal;font-size:13pt\">" + movieItemList[m][i][28].rstrip('"').lstrip('"')
					categoryNumbers[category] += 1
					if (category != ""):
						local_eng_cat = englishKeys[y][(catacount - 1)].lower()
					else:
						local_eng_cat = ""
					if (episode != ""):
						synoptextBase = "TVSYNOPBASE"
					elif (((airlineID == "ana") or (airlineID == "aeroflot")) and "movie" in local_eng_cat):
						synoptextBase = "SYNOPBASE"
					else:
						synoptextBase = cataList[c][(p+3)].strip()
					if ( englishEpisode.lower() == "digetunes"):
						categoryNumbers[category] = 0
						categories[category] += ((indent+2) * "\t") + "<actionGroup>\n"
						indent += 2
						categories[category] += ((indent+1) * "\t") + "<title>" + playText[l] + "</title>\n"
						WriteMusicCat(title.lower())
						indent -= 2
						categories[category] += ((indent+2) * "\t") + "</actionGroup>\n"
					elif ("Games" in category):
						indent += 1
						Games(dirLang[l].strip())
						synoptextBase = "GAMESSYNOPBASE"
						GetSynop(dirLang[l].strip(), "games", synoptextBase)
						indent -= 1
					else:
						if (airlineID == "ana" or airlineID == "gulf air"):
							if (l != menuLangENG):
								z = (m - (len(cataList)*l) + (menuLangENG * len(cataList)))
							else:
								z = m
							videoFileLangs = GetFileNameLanguages(movieItemList[z][i])
							videoFile = GetVideoFileName(videoFileLangs)
						else:
							videoFile = "MISSINGVIDEO"
						MenuItem(movieItemList[m][i], dirLang[l].strip(), cataList[c][(p+2)].strip(), cataList[c][(p+4)].strip(), videoFile)
						GetImage(englishTitle , englishEpisode, imageDir)
						GetSynop(dirLang[l].strip(), cataList[c][(p+2)].strip(), synoptextBase)
					if(len(category) < 1):
						indent += 1
				if (cataList[c][(p+1)].strip() == "no-sub"):
					WriteToMml(writeMe)
				else:
					WriteGenresToMml(categories, cataList[c][(p+1)].strip(), cataList[c][(p-1)].strip().lower())
					y += 1
					if(cataList[c][(p-1)].strip().lower() == "yes"):
						WriteAllToMml(allMovies, cataList[c][(p+1)].strip(), AllMoviesTitle[l].strip())
				f.write((indent * "\t") + "</menuitem>\n")
			elif (cataList[c][(p+2)].strip().lower() == "music"):
				digetunes = movieItemList[m][0][0].rstrip('"').lstrip('"').strip().lower().replace("#","@")
				f.write(((indent+1) * "\t") + "<icon>/content/menu/images/icons/" + cataList[c][p].strip() + ".png</icon>\n")
				f.write(WriteMusicCat(digetunes.lower()))
				f.write((indent * "\t") + "</menuitem>\n")
			elif (cataList[c][(p+2)].strip() == "net"):
				WriteInternetCat()
			elif (cataList[c][(p+2)].strip().lower() == "ads"):
				#if (homepage == "www.alaskaair.com"):
				BulkAds(cataList[c][0].split('(')[0].strip(), dirLang[l].strip())
				#else:
				#	for i in range(0,len(movieItemList[m])):
				#		itemcount += 1
				#		title = movieItemList[m][i][3].rstrip('"').lstrip('"').strip().replace("#","@")
				#		episode = movieItemList[m][i][4].rstrip('"').lstrip('"').strip().replace("#","@")
				#		englishTitle = movieItemList[m][i][1].rstrip('"').lstrip('"').strip().replace("#","@")
				#		englishEpisode = movieItemList[m][i][2].rstrip('"').lstrip('"').strip().replace("#","@")
				#		
				#		if (not allMovies.has_key(title)):
				#			allMovies[title] = ""
				#		flag = "a"
				#		GetImage(englishTitle, englishEpisode, imageDir)
				#		NoSynopItem(title, englishTitle, cataList[c][(p+2)].strip().lower())
				#	WriteToMml(writeMe)
			else:
				allMovies = {}
				itemcount = 0
				writeMe = {}
				f.write(((indent+1) * "\t") + "<icon>/content/menu/images/icons/" + cataList[c][p].strip() + ".png</icon>\n")
				for i in range(0,len(movieItemList[m])):
					itemcount += 1
					title = movieItemList[m][i][4].rstrip('"').lstrip('"').strip().replace("#","@")
					if (not allMovies.has_key(title)):
						allMovies[title] = ""
					if (cataList[c][(p+2)].strip().lower() == "podcasts"):
						GetImage(cataList[c][(p+1)].strip(), "", imageDir)
						Podcasts(cataList[c][(p+1)].strip())
					elif (cataList[c][(p+2)].strip().lower() == "games"):
						title = movieItemList[m][i][4].rstrip('"').lstrip('"').strip().replace("#","@")
						englishTitle = movieItemList[m][i][3].rstrip('"').lstrip('"').strip().replace("#","@")
						englishEpisode = ""
						synopsis = movieItemList[m][i][5].rstrip('"').lstrip('"').strip().replace("#","@")
						Games(dirLang[l].strip())
						GetImage(englishTitle , englishEpisode, "games")
						GetSynop(dirLang[l].strip(), cataList[c][(p+2)].strip(), cataList[c][(p+3)].strip())
					else:
						song = movieItemList[m][i][5].rstrip('"').lstrip('"').strip().replace("#","@")
						flag = "a"
						GetImage(title, song, imageDir)
						adList = GetAdList("", movieItemList[m][i][6].strip())
						NoSynopItem(title + " - " + song, title + song, cataList[c][(p+2)].strip().lower())
				WriteToMml(writeMe)
				flag = "f"
				f.write((indent * "\t") + "</menuitem>\n")
			m += 1
		if (len(menuLangText) > 1):
			f.write(((indent-2) * "\t") + "</menuitem>\n")
	f.write("</menuitem>\n")
	f.close()
	print "Missing Files:"
	for i in __MissingFiles:
		print i