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
			
def WriteToMml(itemList):
	f.write(((indent+1) * "\t") + "<itemcount> " + str(itemcount) + "</itemcount>\n")
	for i in range(0, len(itemList)):
		f.write(itemList[i])
	
def MenuItem(splits, menuLang, videoType):
		itemAddon = ""
		langCount = 0
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
		for j in range(0, 6):
			if (splits[langTabPlace + j].strip() != ""):
				langCount += 1
			else:
				break
		itemAddon += ((indent+2) * "\t") + "<menuitem> #" + commentTitle + "\n"
		itemAddon += ((indent+3) * "\t") + "<title>" + title + localEpisode + "</title>\n"
		if (langCount > 1):
			itemAddon += ((indent+3) * "\t") + "<itemcount>" + str(langCount) + "</itemcount>\n"
		else:
			itemAddon += ((indent+3) * "\t") + "<click>2</click>\n"
		itemAddon += ((indent+3) * "\t") + "<image>/content/menu/images/interface/" + titleToFilename(englishTitle + englishEpisode) + ".png" + " </image>\n"
		itemAddon += ((indent+3) * "\t") + "<text>/content/menu/text/" + videoType + "/" + menuLang + "/" + titleToFilename(englishTitle) + titleToFilename(localEnglishEpisode) + ".txt</text>\n"
		if (splits[langTabPlace + 1].strip() != ""):
			for i in range(0, 6):
				langSelect = "-a " + str(i)
				if (splits[langTabPlace + i].strip() != ""):
					itemAddon += ((indent+3) * "\t") + "<menuitem>\n"
					itemAddon += ((indent+4) * "\t") + "<title>" + splits[langTabPlace + i].strip() + "</title>\n"
					itemAddon += ((indent+4) * "\t") + "<click>2</click>\n"
					itemAddon += ((indent+4) * "\t") + "<action>!play_video " + langSelect + " /content/videos/MISSINGVIDEO </command>\n"
					itemAddon += ((indent+3) * "\t") + "</menuitem>\n"
		else:
			itemAddon += ((indent+3) * "\t") + "<action>!play_video /content/videos/MISSINGVIDEO </command>\n"
		itemAddon += ((indent+2) * "\t") + "</menuitem>\n"
		categories[category] += itemAddon
		allMovies[title] += itemAddon
		writeMe[(itemcount - 1)] = itemAddon

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
	
def GetImage(localTitle, localEpisode, directory):
	if(not os.path.exists(__OutputDir + "/menu/images/interface/")):
		os.makedirs(__OutputDir + "/menu/images/interface/")
	Imagefilebase = titleToFilename(localTitle)
	ImageFullfilebase = titleToFilename(localTitle + localEpisode)
	if(os.path.exists(__GenerationDir + __GraphicsLibDir + directory + "\\" + ImageFullfilebase + ".png")):
		shutil.copy((__GenerationDir + __GraphicsLibDir + directory + "\\" + ImageFullfilebase + ".png"), __OutputDir + "/menu/images/interface/")
	elif(os.path.exists(__GenerationDir + __GraphicsLibDir + directory + "\\" + Imagefilebase + ".png")):
		shutil.copy((__GenerationDir + __GraphicsLibDir + directory + "\\" + Imagefilebase + ".png"), __OutputDir + "/menu/images/interface/"  + ImageFullfilebase + ".png")
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
	
def Games(menuLang):
	itemAddon = ""
	if ("spider" in englishTitle.lower()):
		gameTitle = "Spider"
	else:
		gameTitle = englishTitle
	itemAddon += ((indent+2) * "\t") + "<menuitem> #" + englishTitle + "\n"
	itemAddon += ((indent+3) * "\t") + "<title>" + title + "</title>\n"
	itemAddon += ((indent+3) * "\t") + "<action>/content/games/fdg" + titleToFilename(gameTitle) + "/start_game.sh</action>\n"
	itemAddon += ((indent+3) * "\t") + "<image>/content/menu/images/interface/" + titleToFilename(englishTitle) + ".png" + "</image>\n"
	itemAddon += ((indent+3) * "\t") + "<text>games/" + titleToFilename(englishTitle) + ".txt" + "</text>\n"
	itemAddon += ((indent+2) * "\t") + "</menuitem>\n"
	writeMe[(itemcount - 1)] = itemAddon
	categories[category] += itemAddon
	
def NoSynopItem(localTitle, localEngTitle, dir):
	itemAddon = ""
	itemAddon += ((indent+2) * "\t") + "<menuitem> #" + localEngTitle + "\n"
	itemAddon += ((indent+3) * "\t") + "<title>" + localTitle + "</title>\n"
	itemAddon += ((indent+3) * "\t") + "<click>2</click>\n"
	itemAddon += ((indent+3) * "\t") + "<image>/content/menu/images/interface/" + titleToFilename(localEngTitle) + ".png" + "</image>\n"
	itemAddon += ((indent+3) * "\t") + "<action>!play_video /content/" + dir + "/MISSINGVIDEO </command>\n"
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
	dirLang = GetLangText(13)
	m = 0
	p = len(menuLangText)
	menuSubText = ""
	categoryENGKeys = []
	englishKeys = []

	GetBulkFiles(".png", "images", "images")

	f.write("<menuitem> #Main Menu\n")
	f.write("\t<title>Main Menu</title>\n")
	if (len(menuLangText) > 1):
		f.write("\t<itemcount>" + str(len(menuLangText)) + "</itemcount>\n")
	for l in range(0, len(menuLangText)):
		indent = 1
		y = 0
		if (len(menuLangText) > 1):
			f.write("\t<menuitem>#" + menuLangText[l].strip() + "\n")
			f.write((indent * "\t") + "<title>" + menuLangText[l].strip() + "</title>\n")
			indent += 1
		f.write((indent * "\t") + "<itemcount>" + str(len(cataList)) + "</itemcount>\n")
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
			if (cataList[c][(p)].strip().lower() == "movies" or cataList[c][(p)].strip().lower() == "tv"):
				subList = ""
				categories = {}
				categoryNumbers = {}
				allMovies = {}
				writeMe = {}
				itemcount = 0
				langTabPlace = 5
				categoryKeys = []
				for i in range(0,len(movieItemList[m])):
					itemcount += 1
					category = movieItemList[m][i][0].strip()
					if(len(category) < 1):
						indent -= 1
					if (not categories.has_key(category)):
						categories[category] = ""
						categoryNumbers[category] = 0
						categoryKeys.append(category)
					title = movieItemList[m][i][3].rstrip('"').lstrip('"').strip().replace("#","@")
					episode = movieItemList[m][i][4].rstrip('"').lstrip('"').strip().replace("#","@")
					englishTitle = movieItemList[m][i][1].rstrip('"').lstrip('"').strip().replace("#","@")
					englishEpisode = movieItemList[m][i][2].rstrip('"').lstrip('"').strip().replace("#","@")
					
					if (not allMovies.has_key(title)):
						allMovies[title] = ""
					duration = movieItemList[m][i][21].strip()
					if (durationText[l] != "" and duration != ""):
						duration = durationText[l].strip() + " " + duration + " " + min[l].strip()
					elif (duration != ""):
						duration = duration + " " + min[l].strip()
					rating = movieItemList[m][i][20].strip()
					if (ratingText[l] != "" and rating != ""):
						rating = ratingText[l].strip() + " " + rating
					languageList = GetLanguages(movieItemList[m][i], langTabPlace, (langTabPlace + 6), (langTabPlace + 7), (langTabPlace + 11))
					if (languageText[l] != ""):
						languageList = languageText[l].strip() + " " + languageList
					genre = movieItemList[m][i][17].strip()
					if (movieItemList[m][i][18].strip() != ""):
						genre = genre + " / " + movieItemList[m][i][18].strip()
						if (movieItemList[m][i][19].strip() != ""):
							genre = genre + " / " + movieItemList[m][i][19].strip()
					cast = movieItemList[m][i][22].rstrip('"').lstrip('"').strip()
					synopsis = movieItemList[m][i][23].rstrip('"').lstrip('"').strip()
					if (movieItemList[m][i][24].rstrip('"').lstrip('"') != ""):
						synopsis = synopsis + "</span><br/><span style=\"font-weight:normal;font-size:13pt\">" + movieItemList[m][i][24].rstrip('"').lstrip('"')
					categoryNumbers[category] += 1
					if (episode != ""):
						synoptextBase = "TVSYNOPBASE"
					else:
						synoptextBase = cataList[c][(p+1)].strip()
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
						MenuItem(movieItemList[m][i], dirLang[l].strip(), cataList[c][(p)].strip())
						GetImage(englishTitle , englishEpisode, cataList[c][(p)].strip())
						GetSynop(dirLang[l].strip(), cataList[c][(p)].strip(), synoptextBase)
					if(len(category) < 1):
						indent += 1
				WriteToMml(writeMe)
				f.write((indent * "\t") + "</menuitem>\n")
			elif (cataList[c][(p)].strip().lower() == "music"):
				f.write(((indent+2) * "\t") + "<action>!digetunes</action>\n")
				f.write((indent * "\t") + "</menuitem>\n")
			elif (cataList[c][(p)].strip().lower() == "ads"):
				f.write(((indent+1) * "\t") + "<text>about_us.txt</text>\n")
				f.write((indent * "\t") + "</menuitem>\n")
			else:
				allMovies = {}
				itemcount = 0
				writeMe = {}
				for i in range(0,len(movieItemList[m])):
					itemcount += 1
					title = movieItemList[m][i][0].rstrip('"').lstrip('"').strip().replace("#","@")
					if (not allMovies.has_key(title)):
						allMovies[title] = ""
					if (cataList[c][(p)].strip().lower() == "games"):
						title = movieItemList[m][i][1].rstrip('"').lstrip('"').strip().replace("#","@")
						englishTitle = movieItemList[m][i][0].rstrip('"').lstrip('"').strip().replace("#","@")
						englishEpisode = ""
						synopsis = movieItemList[m][i][2].rstrip('"').lstrip('"').strip().replace("#","@")
						Games(dirLang[l].strip())
						GetImage(englishTitle , englishEpisode, "games")
						GetSynop(dirLang[l].strip(), cataList[c][(p)].strip(), cataList[c][(p+1)].strip())
					else:
						song = movieItemList[m][i][1].rstrip('"').lstrip('"').strip().replace("#","@")
						GetImage(title, song, cataList[c][(p)].strip().lower())
						NoSynopItem(title + " - " + song, title + song, cataList[c][(p)].strip().lower())
				WriteToMml(writeMe)
				f.write((indent * "\t") + "</menuitem>\n")
			m += 1
		if (len(menuLangText) > 1):
			f.write(((indent-2) * "\t") + "</menuitem>\n")
	f.write("</menuitem>\n")
	f.close()
	print "Missing Files:"
	for i in __MissingFiles:
		print i