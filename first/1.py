# -*- coding: utf-8 -*-

import os
import sys
import collections

def count_bigrams(lang_dir_files):
	bigrams_dictionary = {}

	for lang in lang_dir_files.keys():
		bigrams_dictionary[lang] = {}
		bigrams = {}

		for fl in lang_dir_files.get(lang):
			f = open(fl, mode = "r", encoding="utf-8")
			content_f = f.read()
			f.close()
			i = 0
			while i <= (len(content_f) - 2):
				bigram = content_f[i:i+2]
				bigram = bigram.lower()
				if ('\n' not in bigram and '\r' not in bigram):
					if bigram in bigrams:
						bigrams[bigram] =  bigrams[bigram] + 1
					else:
						bigrams[bigram] = 1
				i = i + 1

		bigrams_dictionary[lang] = bigrams		

	#f = open("results.json", "w") 
	#json.dump(bigrams, f)
	#f.close()
	return(bigrams_dictionary)

# folder_path = '/Users/mandja96/Downloads/public/set/0/corpus'
def list_of_files(folder_path):
	lang_names = os.listdir(folder_path)
	if('.DS_Store' in lang_names):
		lang_names.remove('.DS_Store')
	
	directory_files = {}

	for i in lang_names:
		folder_path_new = os.path.abspath(os.path.join(folder_path, i))

		directory_files[i] = []
		list_of_files = []
		for(dirpath, dirnames, filenames) in os.walk(folder_path_new):
			for file in filenames:
				if(file != '.DS_Store'):
					list_of_files += [os.path.join(dirpath, file)]

		directory_files[i] = list_of_files	
	
	return(directory_files)

def task_1_print(result):
	for key in sorted(result):
		# print first 5 most frequent
		# sort result[key]
		
		val = result[key]
		o_val = collections.OrderedDict(sorted(val.items(), key = lambda x:(-x[1],x[0])))

		i = 0
		items = list(o_val.items())
		while i < 5:
			print('{0},{1},{2}'.format(key, items[i][0], items[i][1]))
			i = i + 1
			
if __name__ == "__main__":
	folder_path = input()
	folder_path = folder_path.strip()

	lang_dir_files = list_of_files(folder_path)
	result = count_bigrams(lang_dir_files)

	task_1_print(result)
	#print(result)
