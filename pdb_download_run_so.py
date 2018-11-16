# coding:utf-8
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals

import argparse
import os,sys,glob
import multiprocessing
import urllib
if sys.version_info.major==2:
	reload(sys)
	sys.setdefaultencoding('utf-8')

from pdb_download_lib_so import *
def main():
	parser = argparse.ArgumentParser(
		  description='score hist scatter roc anal')
		  
	parser.add_argument(
    '-a','--actions',
    nargs='*',
    default=[],
    help="Choice:'vina','grep', ('hist' or 'plt'), ('scatter' or 'score'),(roc or ROC) default is [] which will do 'plt','score', if 'vina' auto anal vina ledock result")
		  
	parser.add_argument(
    '-f','--file',
    type=str,
    default='',
    help="input pdb_ID_list or txt file containing pdb_ID_list. If viod, will use '*.txt[0]'")

	parser.add_argument(
    '-l','--list_pdb_ID',
    nargs='*',
    default=[],
    help="input pdb_ID_list")

	args = parser.parse_args()
	xx_file = args.file; list_pdb_ID = args.list_pdb_ID
	
	if len(list_pdb_ID) > 0: pdb_IDs = list_pdb_ID
	else:
		if xx_file == '':xx_file = glob.glob('*.txt')[0]
		lines = open(xx_file,'r').read().split('\n')
		pdb_IDs = [x.split(' ')[0] for x in lines]

	if len(pdb_IDs) == 0:
		if sys.version_info.major==2: pdb_IDs_str = raw_input('pdb_IDs_str is best sep with blank might be ,or ; or tab\n:')
		else:pdb_IDs_str=input('pdb_IDs_str is best sep with blank (might be ,or;)\n:')
		print('pdb_IDs_str = ', pdb_IDs_str)
		pdb_IDs_str = pdb_IDs_str.replace('\t',' ').replace(';',' ').replace(',',' ').replace('  ',' ').replace('  ',' ')
		print('after replacement the pdb_IDs_str = ', pdb_IDs_str)	
		pdb_IDs = pdb_IDs_str.split(' ')
	pool = multiprocessing.Pool(processes = batch)
	for p in pdb_IDs:
		pool.apply_async(download_single_pdb,(p, ))  # args=(r_base,l_ab_path,l_base,)
	pool.close()
	pool.join()	

if __name__ == '__main__':
	main()


