
import codecs, os.path, sys, re, shutil, time, getpass, os, distutils, random, io, glob, xlrd, xlwt, glob, unicodedata, difflib, xlutils
from xlrd import open_workbook
from xlutils.copy import copy

reload(sys)

# Globals
if (os.path.isdir("C:\\Users\\" + getpass.getuser() + "\\Dropbox\\Content Share\\QA Sheets")):
	__CTR_dir = "C:\\Users\\" + getpass.getuser() + "\\Dropbox\\Content Share\\QA Sheets"
elif (os.path.isdir("C:\\Users\\" + getpass.getuser() + "\\Dropbox (digEcor)\\Content Share\\QA Sheets")):
	__CTR_dir = "C:\\Users\\" + getpass.getuser() + "\\Dropbox (digEcor)\\Content Share\\QA Sheets"
else:
	print "ERROR path does not exist: C:\\Users\\" + getpass.getuser() + "\\Dropbox (digEcor)\\Content Share\\QA Sheets"
	exit()	
#Uncomment for testing!!!
#__CTR_dir = "C:\\Users\\Richard\\Dropbox (digEcor)\\Content Share\\anthonysmenu\\Menuing\\thatana\\source"
	
__OutputDir = ""
__LanguageMap = {	'English' : 'ENG',
					'English/Japanese' : 'EAJ',
					'Japanese/English' : 'JAE',
					'Arabic' : 'ARA',
					'Arabic' : 'ARB',
					'Dutch' : 'DUT',
					'Russian' : 'RUS',
					'German' : 'GER',
					'English/German' : 'EAG',
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
					'Indonesian' : 'IND',
					'Indonesia' : 'IND',
					'Engels' : 'ENE',
					'Nederlands' : 'NED',
					'Nonverbal' : '',
					'Vietnamese' : 'VIE',
					'Bosnian' : 'BOS',
					'Thai' : 'THA',
					'Mandarin' : 'MAN',
					'Mandalin' : 'MAN',
					'Cantonese' : 'CAN',
					'Thai' : 'THA'}
					
__AirlineMap = {	'ANA' : 'ana',
					'GFA' : 'gulfair',
					'AFL' : 'aeroflot',
					'KQA' : 'kenya',
					'NAO' : 'northamerican',
					'CSN' : 'chinasouthern',
					'ETH' : 'ethiopian',
					'SCX' : 'sun-country',
					'RAM' : 'ram',
					'FJL' : 'fijiair'}
					
sys.setdefaultencoding('utf-8')

	
def strip_accents(input_str):
    nkfd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

	
def TitleToFilename(file):
	retVal = file.strip().encode('utf-8')
	retVal = retVal.replace("&", "And")
	#retVal = strip_accents(retVal)
	retVal = re.sub(r'[\W]', r"", retVal)
	tList = list(retVal)
	retVal = "".join(tList)
	return retVal.encode('utf-8')

def GetLangs(place):
	langList = "_"
	for i in range(9, 15):
		if (rename_excel_list[sheet][place][i].strip() != ""):
			lang = rename_excel_list[sheet][place][i].strip().encode('utf-8')
			lang = re.sub(r'[\W]', r"", lang)
			if (lang in __LanguageMap):
				langList += __LanguageMap[lang]
			else:
				print lang + " Language code not found for " + title.encode('utf-8')
				return "fault"
	if (rename_excel_list[sheet][place][16].strip() != ""):
		lang = rename_excel_list[sheet][place][16].strip()
		langList += "_" + __LanguageMap[lang]
		if (rename_excel_list[sheet][place][17].strip() != ""):
			lang = rename_excel_list[sheet][place][17].strip()
			langList += __LanguageMap[lang]
	if (rename_excel_list[sheet][place][18].strip() != ""):
		langList += "_"
	for j in range(18, 21):
		if (rename_excel_list[sheet][place][j].strip() != ""):
			lang = rename_excel_list[sheet][place][j].strip().encode('utf-8')
			lang = re.sub(r'[\W]', r"", lang)
			if (lang in __LanguageMap):
				langList += __LanguageMap[lang].lower()
			else:
				print lang + " Language code not found for " + title.encode('utf-8')
	return langList

def BuildListFromExcel(filename):
	readXL = open_workbook(filename)
	writeXL = []
	for sheet in readXL.sheets():
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

def EditCTR(sheet, row, col, value):
	for i in range(len(ctr_filename)):
		if (os.path.exists(ctr_filename[i])):
			ctr_xl = open_workbook(ctr_filename[i], formatting_info=True)
		else:
			print "Excel sheet does not exist: " + ctr_filename[i]
			exit()
		write_ctr_xl = copy(ctr_xl)
		write_ctr_xl.get_sheet(sheet).write(row, col, value)
		os.remove(ctr_filename[i])
		write_ctr_xl.save(ctr_filename[i])
	
def AmIaFloat(float_or_not):
	if (isinstance( float_or_not, float )): 
		float_or_not = str(int(float_or_not))
	return float_or_not.strip()
	
if __name__ == "__main__":

	
	if (len(sys.argv) != 4):
		print "Usage: RenameScript.py <ext type> <airline ID> <year-month ex: 2014-09>"
		print "Looks for files with ext-type (.png or .mkv) in respective"
		print "directories to rename. Directories must have a FileNames.txt"
		print "For .mkv, will look for files in directories on hard-drive, (ex: CurrentANA)"
		exit()
	ext = sys.argv[1]
	airlineID = sys.argv[2]
	airlineID = airlineID.upper()
	ctr_date = sys.argv[3]
	
	if (airlineID in __AirlineMap):
		airline_name = __AirlineMap[airlineID]
	else:
		print "ERROR: Airline ID not found for " + airlineID
		print "Airline ID: ANA, GFA, AFL, KQA, NAO, CSN, TFL, AHY, ETH, SCX, RAM, FJL"
		exit()
		
	if ((ext != ".png") and (ext != ".mkv")):
		print "Usage: anaRenameScript.py (.png or .mkv)"
		exit()
	
	ctr_eng_filename = __CTR_dir + "/CTR_" + airline_name + "_" + ctr_date + "_eng.xls"
	ctr_filename = glob.glob(__CTR_dir + "/CTR_" + airline_name + "_" + ctr_date + "*.xls")
	
	if (os.path.exists(ctr_eng_filename)):
		rename_excel_list = BuildListFromExcel(ctr_eng_filename)
	else:
		print "There is no CTR for " + airlineID
		exit()
	
	if ((ext == ".png") and (airlineID == "ANA")):
		if (os.path.isdir("C:\\Users\\" + getpass.getuser() + "\\Dropbox (digEcor)\\Content Share\\Library-Graphics_ready\\" + airline_name + "\\")):
			__GenerationDir = "C:\\Users\\" + getpass.getuser() + "\\Dropbox (digEcor)\\Content Share\\Library-Graphics_ready\\" + airline_name + "\\"
		elif (os.path.isdir("C:\\Users\\" + getpass.getuser() + "\\Dropbox\\Content Share\\Library-Graphics_ready\\" + airline_name + "\\")):
			__GenerationDir = "C:\\Users\\" + getpass.getuser() + "\\Dropbox\\Content Share\\Library-Graphics_ready\\" + airline_name + "\\"
		else:
			print "ERROR path does not exist: C:\\Users\\" + getpass.getuser() + "\\Dropbox (digEcor)\\Content Share\\Library-Graphics_ready\\" + airline_name + "\\"
			exit ()
		#Uncomment for testing!!!
		#__GenerationDir = "C:\\Users\\" + getpass.getuser() + "\\Dropbox\\Content Share\\Library-Graphics_ready\\testing\\"
	elif (ext == ".mkv"):
		if (os.path.isdir("F:\\Current" + airlineID + "\\")):
			__GenerationDir = "F:\\Current" + airlineID + "\\"
		elif (os.path.isdir("E:\\Current" + airlineID + "\\")):
			__GenerationDir = "E:\\Current" + airlineID + "\\"
		elif (os.path.isdir("D:\\Current" + airlineID + "\\")):
			__GenerationDir = "D:\\Current" + airlineID + "\\"
		else:
			print "ERROR: \Current" + airlineID + " directory not found in D:\\, E:\\ or F:\\"
			exit()
	else: 
		print "Usage: Only renames .png files for ANA"
		exit()
		
	__MissingFiles = []

	fileNames = []
	cataList = []
	sheet = 5 #for some reason there are 2 hidden sheets
	
	for x in range(5, len(rename_excel_list[sheet])):
		overviews = rename_excel_list[sheet][x]
		del overviews[0]
		cataList.append(overviews)
	
	if (airlineID != "ANA"): date = ""
	else:
		datecode = xlrd.xldate_as_tuple(rename_excel_list[(sheet + 1)][1][2], 0)
		date = "-" + '%s-%s-%s' % (datecode[1], datecode[2], datecode[0])
	
	for j in range(0, len(cataList)):
		if (len(cataList[j][0]) > 0):
			sheet += 1
			if (cataList[j][5] == "movies" or cataList[j][5] == "tv"):
				for k in range(1, len(rename_excel_list[sheet])):
					mainTitle = AmIaFloat(rename_excel_list[sheet][k][5])
					episode = AmIaFloat(rename_excel_list[sheet][k][6])
					languages = ""
					if (ext == ".mkv"):
						col_plus = 2
						col = 36
						currentFileName = AmIaFloat(rename_excel_list[sheet][k][col]).replace(".mkv", "").replace(".png", "").replace(".jpg", "").replace(".mpg", "")
						languages = GetLangs(k)
						if (episode != ""):
							title = TitleToFilename(mainTitle.lower().title()) + "-" + TitleToFilename(episode.lower().title())
						else:
							title = TitleToFilename(mainTitle.lower().title())
						filebase = airlineID + "-" + title + date + languages
						currentFileName2 = AmIaFloat(rename_excel_list[sheet][k][(col+1)])
						if (currentFileName2 != ""): 
							print "Manually change files " + currentFileName.encode('ascii', 'ignore') + ext + " and " + currentFileName2.encode('ascii', 'ignore') + ext + "\nto " + airlineID + "-" + title + date + " with appropriate languages!"
							continue
					else:
						col_plus = 1
						col = 40
						currentFileName = AmIaFloat(rename_excel_list[sheet][k][col]).replace(".mkv", "").replace(".png", "").replace(".jpg", "").replace(".mpg", "")
						filebase = TitleToFilename(mainTitle + " " + episode) + date
					if(os.path.exists(__GenerationDir + currentFileName.strip() + ext) and languages != "fault"):
						if(os.path.exists(__GenerationDir + filebase + ext)):
							filebase = filebase + str(random.randint(0,99))
						os.rename((__GenerationDir + currentFileName.strip() + ext),(__GenerationDir + filebase + ext))
						#EditCTR(sheet, k, (col + col_plus), filebase)
					else:
						if(os.path.exists(__GenerationDir + filebase + ext)):
							x = 1
							#EditCTR(sheet, k, (col + col_plus), filebase)
						else: __MissingFiles.append(currentFileName.strip() + ext)

	print "Missing Files:"
	for missing in __MissingFiles:
		print missing