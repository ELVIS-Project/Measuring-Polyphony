# -*- coding: utf-8 -*-

"""
This script creates graphical representations of three-voice textures.
It uses the csv output of the vertical interval indexer. It shades perfect
and mixed sonorities (according to Fuller (1986)) dark and light grey,
respectively. Dissonant sonorities are shaded with the function hatch_2
and imperfect sonorities are shaded with hatch_1. White bands indicate
rests or solos within the texture. CSV files should be passed as arguments
when executing the script, e.g., > 3vv_graphs.py hugo_12.csv nazarea_18.csv
"""

import sys, csv
from PIL import Image, ImageColor

colP = (65, 65, 65)
colM = (160, 160, 160)
colR = (255, 255, 255)
colours = {'R': colR, 'P': colP, 'RRP': colP, 'RPR': colP, 'PRR': colP, 'M': colM,}

SPECIAL_PERFECTS = [
	['P4', '-P5'],
	['-P5', 'P4']]

SPECIAL_IMPERFECTS = [
	['-P4', '-m6'],
	['-m6', '-P4'],
	['-P4', '-M6'],
	['-M6', '-P4'],
	['P4', '-m3'],
	['-m3', 'P4'],
	['P4', '-M3'],
	['-M3', 'P4']]

SPECIAL_DISSONANTS = [
	['P5', 'm6'],
	['m6', 'P5'],
	['P5', 'M6'],
	['M6', 'P5'],
	['-P5', '-m6'],
	['-m6', '-P5'],
	['-P5', '-M6'],
	['-M6', '-P5']]

if len(sys.argv) == 1:
	print('\n> Please specify a file(s)')

for arg in sys.argv[1:]:

	rows = [] # a list of the rows in the CSV file
	sonorities = [] # a list of the sonorities in each row (as strings)

	with open(arg) as csvfile:
		readCSV = csv.reader(csvfile, delimiter = ',')
		for row in readCSV:

			# skip the first three rows that don't have any data
			if row[0] != 'Indexer' and row[0] != 'Parts' and row[0] != '':

				# make a list of the rows
				if 'Rest' in row:
					rows.append(row[-3:])

				# if there are no rests, just use intervals above the lowest voice
				else:
					rows.append(row[-2:])

	for r in rows:

		if 'Rest' in r:
		
			# first two columns are rests (single interval between A & T)
			if r[0] == r[1] == 'Rest' and r[2] != 'Rest':
				if any(x in str(r) for x in ['d', 'A', '2', '7', '4']):
					sonorities.append('RRD')
				elif 'P' in str(r):
					sonorities.append('RRP')
				else:
					sonorities.append('RRI')

			# first and last columns are rests (single interval between S & T)
			elif r[0] == r[2] == 'Rest' and r[1] != 'Rest':
				if any(x in str(r) for x in ['d', 'A', '2', '7', '4']):
					sonorities.append('RDR')
				elif 'P' in str(r):
					sonorities.append('RPR')
				else:
					sonorities.append('RIR')

			# last two columns are rests (single interval between S & A)
			elif r[0] != 'Rest' and r[1] == r[2] == 'Rest':
				if any(x in str(r) for x in ['d', 'A', '2', '7', '4']):
					sonorities.append('DRR')
				elif 'P' in str(r):
					sonorities.append('PRR')
				else:
					sonorities.append('IRR')

			# all three columns are rests
			else:
				sonorities.append('R')

		# special cases
		elif r in SPECIAL_DISSONANTS:
			sonorities.append('D')
		elif r in SPECIAL_IMPERFECTS:
			sonorities.append('I')
		elif r in SPECIAL_PERFECTS:
			sonorities.append('P')

		# now what remain are full sonorities with no rests and no consonant fourths
		# dissonant first
		elif any(x in str(r) for x in ['d', 'A', '2', '7', '4']):
			sonorities.append('D')

	    # then perfect
		elif '3' not in str(r) and '6' not in str(r):
			sonorities.append('P')

		# then imperfect
		elif '1' not in str(r) and '5' not in str(r) and '8' not in str(r):
			sonorities.append('I')

		# finally mixed (all that's left)
		else:
			sonorities.append('M')

	print(sonorities)

	# making a graph of the sonorities
	size = (len(sonorities)*22, 99)
	img = Image.new('RGB', size, 'white')

	FULL = ['R', 'P', 'M', 'I', 'D']
	SA = ['PRR', 'IRR', 'DRR']
	ST = ['RPR', 'RIR', 'RDR']
	AT = ['RRP', 'RRI', 'RRD']

	DISS = ['D', 'RRD', 'RDR', 'DRR']
	IMP = ['I', 'RRI', 'RIR', 'IRR']

	def draw_black_line(img, X2):
		"draws a black line"
		for x in range(X2, (X2 + 2)):
			for y in range(0, 99):
				img.putpixel((x, y), ImageColor.getcolor('black', 'RGB'))
		return None

	def draw_band(img, X1, Y1, X2, Y2):
		"fills in the specified band with solid colour"
		for x in range(X1, X2):
			for y in range(Y1, Y2):
				img.putpixel((x, y), colours[sonorities[i]])
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
	while i < len(sonorities):

		if sonorities[i] in FULL:
			X1 = i*22
			Y1 = 0
			X2 = X1 + 20
			Y2 = 99
			split = False 
		elif sonorities[i] in SA:
			X1 = i*22
			Y1 = 0
			X2 = X1 + 20
			Y2 = 66
			split = False
		elif sonorities[i] in AT:
			X1 = i*22
			Y1 = 33
			X2 = X1 + 20
			Y2 = 99
			split = False
		else:
			X1 = i*22
			Y1 = 0
			X2 = X1 + 20
			Y2 = 33
			split = True

		if sonorities[i] in DISS:
			draw_hatch_2(img, X1, Y1, X2, Y2)
			draw_black_line(img, X2)

		elif sonorities[i] in IMP:
			draw_hatch_1(img, X1, Y1, X2, Y2)
			draw_black_line(img, X2)

		else:
			draw_band(img, X1, Y1, X2, Y2)
			draw_black_line(img, X2)
		
		if split:
			
			if sonorities[i] in DISS:
				draw_hatch_2(img, X1, Y1 + 66, X2, Y2 + 66)

			elif sonorities[i] in IMP:
				draw_hatch_1(img, X1, Y1 + 66, X2, Y2 + 66)

			else:
				draw_band(img, X1, Y1 + 66, X2, Y2 + 66)
		
		i = i + 1

	img.save(str(arg[:-4]) + '.png')