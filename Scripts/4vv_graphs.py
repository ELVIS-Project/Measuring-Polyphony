# -*- coding: utf-8 -*-

"""
This script creates graphical representations of four-voice textures.
It uses the csv output of the vertical interval indexer. It shades perfect
and mixed sonorities (according to Fuller (1986)) dark and light grey,
respectively. Dissonant sonorities are shaded with the function hatch_2
and imperfect sonorities are shaded with hatch_1. Rests are displayed as
white bands.
"""

import csv
from PIL import Image, ImageColor

fileName = raw_input('\nEnter file name\n>')

rows = [] # a list of the rows in the CSV file
sonorities = [] # a list of the sonorities in each row (as strings)
textures = [] # a list of the textures of each of the sonorities
results = [] # a list of the results represented as letters

colP = (65, 65, 65)
colM = (160, 160, 160)
colR = (255, 255, 255)
colours = {'R': colR, 'P': colP, 'RRP': colP, 'RPR': colP, 'PRR': colP, 'M': colM,}

with open(fileName) as csvfile:
	readCSV = csv.reader(csvfile, delimiter = ',')
	for row in readCSV:

		# skip the first three rows that don't have any data
		if row[0] != 'Indexer' and row[0] != 'Parts' and row[0] != '':

			# append everything but the offset number (as a list)
			rows.append(row[-6:])

# get sonorities
for r in rows:

	# if 3 or more voices have rests
	if r.count('Rest') > 5:
		s = ['Rest']

	# if voice 3 has a rest
	elif r[2] == r[4] == r[5] == 'Rest':
		
		# if voice 2 also has a rest
		if r[1] == r[3] == 'Rest':
			if   '-' in r[0]:
				s = [r[0][-2:]]
			else:
				s = [r[0]]

		# if voice 2 has a note
		else:
			if   '-' in r[3]:
				s = [r[0], r[3][-2:]]
			elif '-' in r[1]:
				s = [r[0][-2:], r[1][-2:]]
			else:
				s = [r[1], r[3]]

	# if all four voices have notes
	elif r[2] != 'Rest' and r[4] != 'Rest' and r[5] != 'Rest':
		if   '-' in r[5]:
			s = [r[1], r[3], r[5][-2:]]
		elif '-' in r[4]:
			s = [r[0], r[3][-2:], r[4][-2:]]
		else:
			s = [r[2], r[4], r[5]]

	# if voice 3 has a note and at least one of the other voices has a rest
	else:
		if   '-' in r[5] and 'Rest' in r[1]:
			s = [r[3], r[5][-2:]]
		elif '-' in r[5] and 'Rest' in r[3]:
			s = [r[1], r[5][-2:]]
		elif '-' in r[4] and 'Rest' in r[5]:
			s = [r[0], r[4][-2:]]
		elif '-' in r[4] and 'Rest' in r[0]:
			s = [r[3][-2:], r[4][-2:]]
		else:
			s = [r[2], r[4], r[5]]

	sonorities.append(s)

#get textures
for s in sonorities:

	if len(s) == 3:
		if   s[0] == 'Rest' and s[1] != 'Rest' and s[2] != 'Rest':
			t = ['R', 'N', 'N', 'N']

		elif s[0] != 'Rest' and s[1] == 'Rest' and s[2] != 'Rest':
			t = ['N', 'R', 'N', 'N']

		elif s[0] != 'Rest' and s[1] != 'Rest' and s[2] == 'Rest':
			t = ['N', 'N', 'R', 'N']

		elif s[0] == s[1] == 'Rest' and s[2] != 'Rest':
			t = ['R', 'R', 'N', 'N']

		elif s[0] == s[2] == 'Rest' and s[1] != 'Rest':
			t = ['R', 'N', 'R', 'N']

		elif s[1] == s[2] == 'Rest' and s[0] != 'Rest':
			t = ['N', 'R', 'R', 'N']

		else:
			t = ['N', 'N', 'N', 'N']

	elif len(s) == 2:
		if   s[0] != 'Rest' and s[1] != 'Rest':
			t = ['N', 'N', 'N', 'R']

		elif s[0] == 'Rest':
			t = ['R', 'N', 'N', 'R']

		elif s[1] == 'Rest':
			t = ['N', 'R', 'N', 'R']

	else:
		if   s[0] == 'Rest':
			t = ['R', 'R', 'R', 'R']
		else:
			t = ['N', 'N', 'R', 'R']

	textures.append(t)

# get results
for s in sonorities:

	ss = str(s)

	if ss == 'Rest':
		results.append('R')

	elif any(x in ss for x in ['d', 'A', '2', '7', '4']):
		results.append('D')

	elif '3' not in ss and '6' not in ss:
		results.append('P')

	elif '1' not in ss and '5' not in ss and '8' not in ss:
		results.append('I')

	elif '5' in ss and '6' in ss: # the only special case
		results.append('D')

	else:
		results.append('M')

print(results)

# make the graph
# making a graph of the results
size = ((len(results)*22), 100)
img = Image.new('RGB', size, 'white')

def draw_black_line(img, X2):
	"draws a black line"
	for x in range(X2, (X2 + 2)):
		for y in range(0, 100):
			img.putpixel((x, y), ImageColor.getcolor('black', 'RGB'))
	return None

def draw_band(img, X1, Y1, X2, Y2):
	"fills in the specified band with solid colour"
	for x in range(X1, X2):
		for y in range(Y1, Y2):
			img.putpixel((x, y), colours[results[i]])
	return None

def draw_hatch_1(img, X1, Y1, X2, Y2):
	"draws a horizontal hatch pattern"
	k = 0
	for y in range(Y1, Y2):
		for x in range(X1, X2):
			if k % 5 == 0:
				img.putpixel((x, y), ImageColor.getcolor('black', 'RGB'))
		k = k + 1
	return None

def draw_hatch_2(img, X1, Y1, X2, Y2):
	"draws a diagonal hatch pattern"
	m = 0
	for y in range(Y1, Y2):
		for x in range(X1, X2):
			if m % 7 == 0:
				img.putpixel((x, y), ImageColor.getcolor('black', 'RGB'))
			m = m + 1
	return None

i = 0
while i < len(results):

	j = 0
	while j < 4:

		X1 = i*22
		Y1 = j*25
		X2 = X1 + 20
		Y2 = Y1 + 25

		if textures[i][j] == 'N':

			if  results[i] == 'D':
				draw_hatch_2(img, X1, Y1, X2, Y2)
			elif results[i] == 'I':
				draw_hatch_1(img, X1, Y1, X2, Y2)
			else:
				draw_band(img, X1, Y1, X2, Y2)
		
		j = j + 1

	draw_black_line(img, (i*22 + 20))
	
	i = i + 1

img.save(str(fileName[:-4]) + '.png')