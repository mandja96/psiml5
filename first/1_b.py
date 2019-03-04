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

			l_content = len(content_f)
			while i <= (l_content - 2):
				bigram = content_f[i:i+2]
				bigram = bigram.lower()

				if ('\n' not in bigram and '\r' not in bigram):
					if bigram in bigrams:
						bigrams[bigram] =  bigrams[bigram] + 1
					else:
						bigrams[bigram] = 1

				i = i + 1

		bigrams_dictionary[lang] = bigrams
	return(bigrams_dictionary)

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
			
def slice_line(input_line):
	new_list = []
	for i in range(0, len(input_line)-1):
		new_list.append(input_line[i:i+2])

	return new_list

def probabilities(sliced, result):
	new_dict = {}
	total_probability = 0

	for key, value in result.items():
		p = 1
		sum_lang = sum(result[key].values())
		if key not in new_dict:
			new_dict[key] = 0

		for i in sliced:
			if(i not in result[key]):
				p = 0
				break
			else:
				p = p * result[key][i] / sum_lang

		new_dict[key] = p	
		total_probability = total_probability + p

	for key in new_dict:

		if(total_probability):
			new_dict[key] = new_dict[key] / total_probability 				
	
	return(new_dict)

def task_2_print(result_prob):
	for k in sorted(result_prob):
		print('{0},{1}'.format(k, result_prob[k]))

def	read_sequence(file_path):
	with open(file_path, encoding = "utf-8") as f:
		lines = f.read().splitlines()

	for l in lines:
		sliced = slice_line(l.lower())
		result_prob = probabilities(sliced, result)
		task_2_print(result_prob)
		
if __name__ == "__main__":
	folder_path = input()
	folder_path = folder_path.strip() 

	file_path = input()
	file_path = file_path.lstrip()

	lang_dir_files = list_of_files(folder_path)
	result = count_bigrams(lang_dir_files)

	task_1_print(result)
	
	read_sequence(file_path)	


