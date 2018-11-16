# coding:utf-8
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
import argparse
import os, sys, glob, re
import pybel
import pandas as pd
if sys.version_info.major==2:
	reload(sys)
	sys.setdefaultencoding('utf-8')
#===============================================================
print('uasage:\nexample 1: this_module.py [xx_cmpd_list.txt|.csv [xx_top_num   will auto detect *.sdf file')
print('similar function as _csv_select_sdf, the diff is: this is split, and rm duplicated')
print('so this is suitable for final selection and clustering, because including rm dup')
#-----------input parameters below------------

dic_sdf_fold_ab_path = {'chemdiv':'/run/media/phzd/sda/@cmpds/@sgl_sdfs/chemdiv','specs':'/run/media/phzd/sda/@cmpds/@sgl_sdfs/specs_sdf','TCMSP':'/run/media/phzd/sda/@cmpds/@sgl_sdfs/TCMSP','TCMTW':'/run/media/phzd/sda/@cmpds/@sgl_sdfs/TCMTW'}
#------------end input parameter----------

from glide4b_splitSdf_fetchSdf_lib_so import *
def main():
	os.chdir(base)
	parser = argparse.ArgumentParser(description='split and fetchSdf')

	parser.add_argument('-f','--files',nargs='*',default=[],
    help="input files lists, can be viod. If viod, will use *.txt|csv|xlsx")
		  
	parser.add_argument('-split','--split_sdfs',nargs='*',default=[],
    help="specify sdf files want to split; this will inactivate -fold")
    
	parser.add_argument('-fold','--fold_single_sdfs',nargs='*',default=[],
    help="choice of single sdfs fold: chemdiv,specs,TCMSP; default is: '' ")   
  
	parser.add_argument('-top','--top_num',type=int,default=1000, help="top_num, default is 1000")

	parser.add_argument('-choose_score', '---choose_score',action='store_true', default=False,
	help="-choose_score, will cause raw_input of scores to incorporate,defualt is False, which use incorp all")    
    
	args = parser.parse_args()
	files = args.files; split_sdfs = args.split_sdfs
	fold_single_sdfs = args.fold_single_sdfs; top_num = args.top_num; choose_score = args.choose_score
	if_all_score = False	if choose_score else True
	if len(files) == 0: files = glob.glob('*.txt') + glob.glob('*.csv') 
	if len(files) == 0: raise IOError('no txt|csvfile was found')	
	if len(split_sdfs) > 0: 
		fold_single_sdfs = ['sdf']
		for sdf_filename in split_sdfs:split_sdf_by_title(sdf_filename)   ## split file
	if len(fold_single_sdfs) == 0: fold_single_sdfs = ['sdf']
	
	for txt_csv_filename in files:
		for sdf_fold in fold_single_sdfs:	
			#write_the_toplist_and_copy(txt_csv_filename, sdf_fold, top_num)
			write_the_toplist_and_copy(txt_csv_filename, sdf_fold, top_num, if_all_score)

if __name__ == '__main__':
	main()
