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

NAMES = ['a-da-ga$W$',
         'szu-x-lum$u$',
         'lugal-x-a$X$',
         'bi-zag3$X$',
         'du-uk-sza-szum$X$',
         'ur-AN-x-x$u$',
         'nin-gi16-sa-ni$X$',
         'ha-bi2-ba-tum$X$',
         'nu-ra-tum$X$',
         'du6-lugal-x-tusz-a-ta$X$',
         'mu-ni-ma-kal$X$',
         'li-ha-mu-tar-re$X$',
         'hu-ma-x-x$X$',
         'a-du3-szu-x$X$',
         'geme2-{d}a-x$X$',
         'x-x-x$u$',
         'nigir-ka-gi-na$X$',
         'i-ti-esz18-dar$X$',
         'sza-lim-tu-ri$X$',
         'ba-ku-tum$X$',
         'bi2-za-tum$X$',
         'szu-sukkal$X$',
         'ba-la-lum$X$',
         'sza-at-x$X$',
         'x-esz18-dar$X$',
         'x-{d}suen$u$',
         'A-gi$X$',
         'szal2-mah$X$',
         'a-mur-{d}suen-sze3$X$',
         'nig2-mu-me-en-sze3$X$',
         'i-x-sze3$X$',
         'szu-x-sze3$X$',
         'nu-ur2-zu-sze3$X$',
         'en-kasz4$X$',
         'iri-na-ka$X$',
         '|PU3.SZA|-dingir$X$',
         'en-za-gu$X$', 
         'lu2-me-te-na$X$',
         'bu-ku-usz$X$',
         'nu-ur2-i3-li$X$',
         'a-hi-lum$X$',
         'geme2-szu-kin-x$u$',
         'x-usz-kal-la$X$',
         'PA-a-esz$X$',
         'sa6-ga-im-ta-e3$X$',
         'il3-szu-mu-da-ri6-iq$X$',
         'dan-ni$X$',
         'en-nig2-lul-la$X$',
         'NI-du-ki$X$',
         'ama-maszkim$X$',
         'ti-nig2-ba$X$',
         'ti-nig2-du10$X$',
         'u4-he2-su3-e$X$',
         'egir-szu-ba-ra-ad$X$',
         'nig2-nin-mu-mu-tum3$X$',
         'lu2-dingir-ra-kam$X$',
         'a-da-ti-ni$X$',
         'a-hi-ba-asz2-ti$X$',
         'da-ra$W$',
         'i-zu-ru-um$X$',
         '|PU3.SZA|-ra$X$',
         '|PU3.SZA|-da-gan$X$',
         'e2-ta-bi$X$',
         'tu-mi-na-a-u2$X$',
         'ur-{u2}|ZI&ZI.LAGAB|-ba$X$',
         'ma-al-lum$X$',
         'lu2-TAG-X$u$',
         'erim2-ze2-ze2-zi-na$X$',
         'lugal-igi-x$X$',
         'sza-lim-mi$X$',
         'me-kab-ta$X$',
         'mu-mu$W$',
         'ri-GIN2-si-mu-sza3$X$',
         'e2-dar-a$X$',
         'hi-me-me-ti$X$',
         'ba-ra-hu-ti$X$',
         'geme2-{d}nin-lil2$X$',
         'sza-lim-du-ri$X$',
         'zi-ip-ni-tum$X$',
         'im-ta-al-ku$X$',
         'du-szu-du-um$X$', 
         'szu-mi-id-dingir$X$',
         'dumu-amar-i3-li2$X$',  
         'in-x-x$u$',
         'ar-bi2-x$X$',
         'be-li2-tu-x$X$',
         'be-ti-im-x$u$',
         'me-{d}nin-x$X$',
         'szu-bu-bu-um$x$',
         'a-na-HI-kak-NI$X$',
         '|PU3.SZA|-i3-li2$X$',
         'lul-ki-du10-UR$X$',
         'ba-ti-mu$W$',
         'i-bu-ku-um$X$',
         'zi2-na-na$X$',
         'la-ma-sa6$X$',
         'nimgir-kaa-gi-na-ke4$X$',
         'sza-ra-at-ni-mu$X$',
         'ba-sag10$W$',
         'um-mi$X$',
         'tu-mi-na-a-u2$X$',
         'en3-mu-he2-tar-re$X$',
         'i-bi2-esz18-dar$X$',
         'HI-na-HAR$X$']

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

		for true_pn in NAMES:
			if true_pn in ln:
				# make a list of words and check the index:
				ln_lst = ln.split();
				for index, word in enumerate(ln_lst):
					if word == true_pn:
						ln_lst[index] = replaceX(ln_lst[index], '$PN$')
				ln = ' '.join(ln_lst)

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
							#non_name = replaceX(ln_lst[index], 'HUM')
							#out2.write(removeX(ln_lst[index])+'\n')
						ln_lst[index] = replaceX(ln_lst[index], '$HUM$')
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
					ln_lst[index] = replaceX(ln_lst[index], '$PLC$')
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
