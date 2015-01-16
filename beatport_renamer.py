import stagger
import os
import urllib.request
import json

from stagger.id3 import *

# gets a list of files from the folder this script is located in
dirList=os.listdir(os.getcwd())

# goes through the whole list of files. If the file is an mp3 it renames it and updates id3 tags
for fname in dirList:

	# gets the last 3 letters of the file name
	fileType = fname[fname.__len__()-3:fname.__len__()].lower()
	
	if fileType == "mp3":
		# read ID3
		tag = stagger.read_tag(fname)
		
		# extract track ID from filename
		trackID = fname;
		while not(trackID.isdigit()):
			trackID = trackID[0:trackID.__len__()-1]
			
		# query beatport
		trackData = urllib.request.urlopen("http://api.beatport.com/catalog/tracks?id=" + str(trackID) + "&format=json&v=1.0").read()
		
		# artist names
		result = json.loads(trackData.decode("utf8"))
		artistList = result['results'][0]['artists']
		artist = artistList[0]['name']
		
		if len(artistList) > 1:
			for i in range(1, len(artistList)):
				artist = artist + ", " + artistList[i]['name']
		
		# track name
		trackName = result['results'][0]['name']
		
		# mix name
		mixName = result['results'][0]['mixName']
		
		# bpm
		bpm = str(result['results'][0]['bpm'])
		
		# key
		keyNode = result['results'][0]['key']['camelot']
		key = str(keyNode['number']) + keyNode['letter']
		
		# construct final file name
		finalName = artist + " - " + trackName + " (" + mixName + ").mp3"
		
		# write tags
		tag.comment = key + " - " + bpm
		tag[TBPM] = bpm
		tag[TKEY] = key
		tag.write(fname)
		
		# rename file
		os.rename(fname, finalName)
		
		# print track
		print("Modified: " + artist + " - " + trackName + " (" + mixName + ")")

input("Done. Press any key to exit...")