#!/usr/bin/python

"""
Remove noise
USAGE: python rmNoise.py testing_corpus new_corpus
"""

import sys
import string
import re

out = open(sys.argv[2],'w')
#out2 = open(sys.argv[3],'w')

# reading geographic names

with open (sys.argv[1],'r') as infile:
	lines = infile.read().splitlines()

def removeX (xstring):
	return re.sub('\$.+?\$', '', xstring)
	

def replaceX (xstring, tag):	
	return re.sub('\$.+?\$', tag, xstring)

for ln in lines:
	
	ln = ln.strip()
	
	# Only tag the lines which start with <l>
	if ln[:3] == '<l>':

		#Spelling rules
		# Replace s,e-li- with sze-li-???						
		if ' sze-li' in ln:
			# make a list of words and check the index:
			ln_lst = ln.split();
			for index, word in enumerate(ln_lst):
				if 'sze-li$' in word or 'sze-li-' in word:
					#if ln_lst[index][-3:] == '$X$' or ln_lst[index][-3:] == '$u$' or ln_lst[index][-3:] == '$x$':
					#if '$' not in ln_lst[index-1]:
						#out.write(removeX(ln_lst[index])+'\n')
					ln_lst[index] = replaceX(ln_lst[index], '$PN$')
			ln = ' '.join(ln_lst)
						
		# Later combine this!!
		if ' s,e-li' in ln:
			# make a list of words and check the index:
			ln_lst = ln.split();
			for index, word in enumerate(ln_lst):
				if 's,e-li$' in word or 's,e-li-' in word:
					#if ln_lst[index][-3:] == '$X$' or ln_lst[index][-3:] == '$u$' or ln_lst[index][-3:] == '$x$':
					#if '$' not in ln_lst[index-1]:
						#out.write(removeX(ln_lst[index])+'\n')
					ln_lst[index] = replaceX(ln_lst[index], '$PN$')	
			ln = ' '.join(ln_lst)
								
		# Determinatives that are names
		# {gar} 99.66% on 577 occurrence, {d} 88.61% on 19,423
		for deter in ['{gar}', '{d}']:
			if deter in ln:
				# make a list of words and check the index:
				ln_lst = ln.split();
				for index, word in enumerate(ln_lst):
					if deter in word:
						#if ln_lst[index][-3:] == '$X$' or ln_lst[index][-3:] == '$u$' or ln_lst[index][-3:] == '$x$':
							#if '$' not in ln_lst[index]:
							#out.write(removeX(ln_lst[index])+'\n')
						ln_lst[index] = replaceX(ln_lst[index], '$PN$')			
				ln = ' '.join(ln_lst)
							
		# Determinatives that are not names ~0%
		# {u2}[plant] 2.5% on 186, {gi}[reed] 0.33% on 352, {ansze}[horse], {dug}[vessel], 
		# {ku6}[fish], {kusz}[leather], {lu2}[men], {munus}[females], {na4}[stone], {ninda}[bread]
		# {sar}[vegetable], {tug2}[garments], {sza}[pig], {uruda}[copper], {zabar}[bronze]
		
		# trading goods
		for deter in ['{dug}', '{u2}', '{gi}', '{ansze}', '{gu2}', '{im}', '{ku6}', '{kasz}', '{kusz}', '{na4}', '{ninda}', '{sza', '{tug2', '{udu', '{uruda', '{zabar}' ]:
			if deter in ln:
				# make a list of words and check the index:
				ln_lst = ln.split();
				for index, word in enumerate(ln_lst):
					if deter in word:
						#if ln_lst[index][-3:] == '$X$' or ln_lst[index][-3:] == '$u$' or ln_lst[index][-3:] == '$x$':
							#if '$' not in ln_lst[index]:
							#non_name = replaceX(ln_lst[index], '$TRAD$')
							#out2.write(removeX(ln_lst[index])+'\n')
						ln_lst[index] = replaceX(ln_lst[index], '$TRD$')
				ln = ' '.join(ln_lst)
		
							
		# Others: river
		for deter in ['{i7}']:
			if deter in ln:
				# make a list of words and check the index:
				ln_lst = ln.split();
				for index, word in enumerate(ln_lst):
					if deter in word:
						#if ln_lst[index][-3:] == '$X$' or ln_lst[index][-3:] == '$u$' or ln_lst[index][-3:] == '$x$':
							#if '$' not in ln_lst[index]:
							#non_name = replaceX(ln_lst[index], 'WN')
							#out2.write(removeX(ln_lst[index])+'\n')
						ln_lst[index] = replaceX(ln_lst[index], '$WN$')
				ln = ' '.join(ln_lst)
		
																					
		# Others: human stuff?
		for deter in ['{lu2}', '{munus}']:
			if deter in ln:
				# make a list of words and check the index:
				ln_lst = ln.split();
				for index, word in enumerate(ln_lst):
					if deter in word:
						#if ln_lst[index][-3:] == '$X$' or ln_lst[index][-3:] == '$u$' or ln_lst[index][-3:] == '$x$':
							#if '$' not in ln_lst[index]:
							#non_name = replaceX(ln_lst[index], 'GEN')
							#out2.write(removeX(ln_lst[index])+'\n')
						ln_lst[index] = replaceX(ln_lst[index], '$GEN$')
				ln = ' '.join(ln_lst)
		
		
		# mu x-sze3
		if ' mu$W$' in ln:
			# make a list of words and check the index:
			ln_lst = ln.split();
			for index, word in enumerate(ln_lst):
				if word == 'mu$W$':
					# Question: is it possible to have some words in between? e.g. mu ku6 al-us2-sa-sze3
					#if ln_lst[index+1][-8:] == '-sze3$X$' or ln_lst[index+1][-8:] == '-sze3$u$' or ln_lst[index+1][-8:] == '-sze3$x$':
					#if '-sze3$' in ln_lst[index+1] and '$' not in ln_lst[index+1]:
						#out.write(removeX(ln_lst[index+1])+'\n')
					ln_lst[index+1] = replaceX(ln_lst[index+1], '$PN$')
					ln_lst[index] = replaceX(ln_lst[index], '$YER$')
			ln = ' '.join(ln_lst)
		
		
		# 1(dize) PN
		if ' 1(disz)$n$' in ln:
			# make a list of words and check the index:
			ln_lst = ln.split();
			for index, word in enumerate(ln_lst):
				if word == '1(disz)$n$' and ln_lst[index-1] == '<l>':
					#if ln_lst[index+1][-3:] == '$X$' or ln_lst[index+1][-3:] == '$u$' or ln_lst[index+1][-3:] == '$x$':
					#if '$' not in ln_lst[index+1]:
						#out.write(removeX(ln_lst[index+1])+'\n')
					ln_lst[index+1] = replaceX(ln_lst[index+1], '$PN$')
			ln = ' '.join(ln_lst)
		
						
		# PN PF
		# Add szidim as a PF, which is tagged as $X$ 
		if '$PF$' in ln:
			# make a list of words and check the index:
			ln_lst = ln.split();
			for index, word in enumerate(ln_lst):
				if '$PF$' in word:
					#if ln_lst[index-1][-3:] == '$X$' or ln_lst[index-1][-3:] == '$u$' or ln_lst[index-1][-3:] == '$x$':
					#if '$' not in ln_lst[index-1]:
						#out.write(removeX(ln_lst[index-1])+'\n')
					ln_lst[index-1] = replaceX(ln_lst[index-1], '$PN$')
			ln = ' '.join(ln_lst)
		
						
		# ki x-ta
		if ' ki$W$' in ln:
			# make a list of words and check the index:
			ln_lst = ln.split();
			for index, word in enumerate(ln_lst):
				if word == 'ki$W$':# and ln_lst[index+1] != '</l>':
					# Same question: is it possible to have some words in between? 
					#if ln_lst[index+1][-6:] == '-ta$X$' or ln_lst[index+1][-6:] == '-ta$u$' or ln_lst[index+1][-6:] == '-ta$x$':
					#if '-ta$' in ln_lst[index+1] and '$' not in ln_lst[index+1]:
						#out.write(removeX(ln_lst[index+1])+'\n')
					ln_lst[index+1] = replaceX(ln_lst[index+1], '$PN$')
					ln_lst[index] = replaceX(ln_lst[index], '$PLA$')
			ln = ' '.join(ln_lst)
		
		
		# dumu PN
		if ' dumu$W$' in ln:
			# make a list of words and check the index:
			ln_lst = ln.split();
			for index, word in enumerate(ln_lst):
				if word == 'dumu$W$':
					#if ln_lst[index+1][-3:] == '$X$' or ln_lst[index+1][-3:] == '$u$' or ln_lst[index+1][-3:] == '$x$':
					#if '$' not in ln_lst[index+1]:
						#out.write(removeX(ln_lst[index+1])+'\n')
					ln_lst[index+1] = replaceX(ln_lst[index+1], '$PN$')
					ln_lst[index] = replaceX(ln_lst[index], '$SON$')
			ln = ' '.join(ln_lst)
		
		
		# PN zi-ga
		if ' zi-ga$W$' in ln:
			# make a list of words and check the index:
			ln_lst = ln.split();
			for index, word in enumerate(ln_lst):
				if word == 'zi-ga$W$':
					#if ln_lst[index-1][-3:] == '$X$' or ln_lst[index-1][-3:] == '$u$' or ln_lst[index-1][-3:] == '$x$':
					#if '$' not in ln_lst[index-1]:
						#out.write(removeX(ln_lst[index-1])+'\n')
					ln_lst[index-1] = replaceX(ln_lst[index-1], '$PN$')
					ln_lst[index] = replaceX(ln_lst[index], '$TAK$')
			ln = ' '.join(ln_lst)
		
		
		# PN i3-dab5
		if ' i3-dab5$W$' in ln:
			# make a list of words and check the index:
			ln_lst = ln.split();
			for index, word in enumerate(ln_lst):
				if word == 'i3-dab5$W$':
					#if ln_lst[index-1][-3:] == '$X$' or ln_lst[index-1][-3:] == '$u$' or ln_lst[index-1][-3:] == '$x$':
					#if '$' not in ln_lst[index-1]:
						#out.write(removeX(ln_lst[index-1])+'\n')
					ln_lst[index-1] = replaceX(ln_lst[index-1], '$PN$')
					ln_lst[index] = replaceX(ln_lst[index], '$TAK$')
			ln = ' '.join(ln_lst)
		
		
		# PN szu ba-ti
		if ' szu$W$ ba-ti$W$' in ln:
			# make a list of words and check the index:
			ln_lst = ln.split();
			for index, word in enumerate(ln_lst):
				if word == 'szu$W$' and ln_lst[index+1] == 'ba-ti$W$':
					#if ln_lst[index-1][-3:] == '$X$' or ln_lst[index-1][-3:] == '$u$' or ln_lst[index-1][-3:] == '$x$':
					#if '$' not in ln_lst[index-1]:
						#out.write(removeX(ln_lst[index-1])+'\n')
					ln_lst[index-1] = replaceX(ln_lst[index-1], '$PN$')
					ln_lst[index] = replaceX(ln_lst[index], '$GIV$')
					ln_lst[index+1] = replaceX(ln_lst[index+1], '$BATI$')
			ln = ' '.join(ln_lst)
		out.write(ln+' \n')
	else:
		out.write(ln+'\n')
