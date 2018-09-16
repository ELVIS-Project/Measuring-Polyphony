# -*- coding: utf-8 -*-

# author:  Sam Howes  <samuel.howes@mail.mcgill.ca>

"""
This script generates a list of sonority types according to Fuller (1986) and
Hartt (2010) from the CSV output of the vertical interval indexer. It measures
all intervals against the lowest sounding note and labels sonorities according
to the intervals they contain. It aggregates results from however many CSV files
are passed as arguments, e.g., 4vv_sonorities.py decens_24.csv portio_36.csv
"""

import sys, csv

numP = 0
numM = 0
numI = 0
numB = 0
numD = 0
numR = 0
numT = 0

if len(sys.argv) == 1:
	print('\n> Please specify a file(s)')

agg = input('\nWould you like to aggregate results? (y/n)\n>')

for arg in sys.argv[1:]:

	rows = [] # a list of the rows in the CSV file
	sonorities = [] # a list of the sonorities in each row (as strings)
	results = [] # a list of the results represented as letters (P, M, I, D, R)

	# get rows
	with open(arg) as csvfile:
		readCSV = csv.reader(csvfile, delimiter = ',')
		
		for row in readCSV:
			if row[0] != 'Indexer' and row[0] != 'Parts' and row[0] != '':
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
				s = [r[0]]

			# if voice 2 has a note
			else:
				if   '-' in r[3]:
					s = [r[0], r[3]]
				elif '-' in r[1]:
					s = [r[0], r[1]]
				else:
					s = [r[1], r[3]]

		# if all four voices have notes
		elif r[2] != 'Rest' and r[4] != 'Rest' and r[5] != 'Rest':
			if   '-' in r[5]:
				s = [r[1], r[3], r[5]]
			elif '-' in r[4]:
				s = [r[0], r[3], r[4]]
			else:
				s = [r[2], r[4], r[5]]

		# if voice 3 has a note and at least one of the other 3 voices has a rest
		else:
			if   '-' in r[5] and 'Rest' in r[1]:
				s = [r[3], r[5]]
			elif '-' in r[5] and 'Rest' in r[3]:
				s = [r[1], r[5]]
			elif '-' in r[4] and 'Rest' in r[5]:
				s = [r[0], r[4]]
			elif '-' in r[4] and 'Rest' in r[0]:
				s = [r[3], r[4]]
			else:
				s = [r[2], r[4], r[5]]

		sonorities.append(s)

	# get results
	for s in sonorities:

		ss = str(s)

		if ss == 'Rest':
			results.append('R')

		elif any(x in ss for x in ['d', 'A', '2', '7', '4']):
			results.append('D')

		elif '5' in ss and '6' in ss: # the only special case
			results.append('D')

		elif '3' in ss and '6' in ss:
			results.append('B')

		elif ('3' in ss or '6' in ss) and not ('5' in ss or '8' in ss):
			results.append('I')

		elif '3' not in ss and '6' not in ss:
			results.append('P')

		else:
			results.append('M')

	# tally results
	numP = numP + results.count('P')
	numM = numM + results.count('M')
	numI = numI + results.count('I')
	numB = numB + results.count('B')
	numD = numD + results.count('D')
	numR = numR + results.count('R')
	numT = numT + len(results)

	# print unaggregated results
	if agg == 'n':
		print('----------------------------------------')
		print(arg)
		print('----------------------------------------')
		print('Perfect = ' + str(results.count('P')))
		print('Mixed = ' + str(results.count('M')))
		print('Imperfect = ' + str(results.count('I')))
		print('Doubly Imperfect = ' + str(results.count('B')))
		print('Dissonant = ' + str(results.count('D')))
		print('Rest = ' + str(results.count('R')))
		print('----------------------------------------')
		print('TOTAL = ' + str(len(results)))
		print('----------------------------------------\n')

# print aggregated results
if agg == 'y':
	print('----------------------------------------')
	print('Results for ' + str(len(sys.argv) - 1) + ' files')
	print('----------------------------------------')
	print('Perfect = ' + str(numP))
	print('Mixed = ' + str(numM))
	print('Imperfect = ' + str(numI))
	print('Doubly Imperfect = ' + str(numB))
	print('Dissonant = ' + str(numD))
	print('Rest = ' + str(numR))
	print('----------------------------------------')
	print('TOTAL = ' + str(numT))
	print('----------------------------------------')