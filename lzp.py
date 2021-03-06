"""lvp - A loose implementation of Lempel-Ziv compression, for use in determining song complexity/repetition.
VERSION 0.1.0

This program is based off of a blog post by Colin Morris titled "Are Pop Lyrics Getting More Repetitive?" 
<https://pudding.cool/2017/05/song-repetition/>. 
In the blog post Mr. Morris used his own version of the LZ algorithm to determine how repetitive a song is. 
I have taken my own interpretation of this idea and implemented it in this program.

This program was requested by, and created for, Cliff Stumme aka "The Pop Song Professor". 

Copyright (C) 2018, Ian S. Pringle
License GNULv3+: GNU GPL Version 3 or later <https://github.com/pard68/lzp/blob/master/LICENSE>
This is free software: you are free to change and redistribute it.
There is NO warranty."""

'''
--------------------------
New Code
--------------------------
'''
import re
import string

#@dataclass
#class lyrics:
#	lyrics: str
#	location: list
#	annotation: list

original_file_name = ""

def read_from_file(file_name):
	global original_file_name
	original_file_name = file_name
	with open(file_name, 'r') as string:
		string = string.read()
		return string

def write_to_file(string):
	global original_file_name
	with open("comp_%s" % original_file_name, 'w') as output_file:
		output_file.write("%s" % string)

def compare(a, b):
	return a == b

def parse_(string):			#Creates an array of locations in string. Line starts and ends, and verses
	lyrics = []
	line = []
	lineStart = 0
	loc = 0
	
	for char in string:
		prevChar = string[loc-1]
		if char is "\n" and prevChar is "\n":
			pass
		else:
			nextChar = string[loc+1]
			if char is "\n" and nextChar is not "\n":
				lineEnd = loc
				line.append([lineStart, lineEnd])
				lineStart = lineEnd + 1
			elif char is "\n" and nextChar is "\n":
				lineEnd = loc
				line.append([lineStart, lineEnd])
				lineStart = lineEnd + 2
				lyrics.append(line)
				line =[]
		loc += 1
	return lyrics

def verse_start(array, verse):
	return array[verse][0][0]

def verse_end(array, verse):
	return array[verse][-1][-1]

def compare_verses(string, array, numberOfVerses):
	while numberOfVerses >= 0:
		startVerse = 0
		endVerse = numberOfVerses
		while endVerse < len(array):
			start = verse_start(array, startVerse)
			end = verse_end(array, endVerse)
			target = string[start:end]
			comparison = string.find(target, end)
			while comparison != -1:
				string = replace(string, compress(start, end), comparison, comparison + (end - start))
				array = parse_(string)
				comparison = string.find(target, comparison + 1)
			startVerse += 1
			endVerse += 1
		return compare_verses(string, array, numberOfVerses - 1)
	return string, array

def get_half(string, array):
	return int(len(array) / 2 - len(array) / 2 % 2) - 1

def compare_lines(string, array, numberOfLines, verseNumber):
	while numberOfLines >= 0:
		startLine = 0
		if numberOfLines - 1 < 0:
			endLine = numberOfLines
		else:
			endLine = numberOfLines - 1
		while endLine < len(array[verseNumber]):
			start = line_start(array, verseNumber, startLine)
			end = line_end(array, verseNumber, endLine)
			target = string[start:end]
			comparison = string.find(target, end)
			while comparison != -1:
				string = replace(string, compress(start, end), comparison, comparison + (end - start))
				array = parse_(string)
				comparison = string.find(target, comparison + 1)
			startLine += 1
			endLine += 1
		return compare_lines(string, array, numberOfLines - 1, verseNumber)
	return string, array

def line_start(array, verseNumber, startLine):
	return array[verseNumber][startLine][0]

def line_end(array, verseNumber, endLine):
	return array[verseNumber][endLine][-1]

def compare_words(string, array):
	verseNum = 0
	lineNum = 0
	
	for verse in array:
		for line in verse:
			words = parse_words(string, array, verseNum, lineNum)
			
	return string, array

def parse_words(string, array, verse, line):
	words = []
	lineStart = array[verse][line][0]
	lineEnd = array[verse][line][-1]
	wordStart = lineStart
	loc = 0
	
	for char in string[lineStart:lineEnd]:
		if char is " ":
			wordEnd = loc
			words.append([wordStart, wordEnd])
			wordStart = wordEnd + 1
		loc += 1
	return words

def compress(start, end):
	compression = '{%s:%s}' % (start, end)
	return compression

def replace(string, new, loc_start, loc_end):
	string = string[:loc_start] + new + string[loc_end:]
	return string

stringLyrics = read_from_file('lyrics_full.txt')

arrayLyrics = parse_(stringLyrics)
stringLyrics, arrayLyrics = compare_verses(stringLyrics, arrayLyrics, get_half(stringLyrics, arrayLyrics))

verseNumber = 0
for verse in arrayLyrics:
	stringLyrics, arrayLyrics = compare_lines(stringLyrics, arrayLyrics, len(verse), verseNumber)
	verseNumber += 1

compare_words(stringLyrics, arrayLyrics)

print(stringLyrics)

