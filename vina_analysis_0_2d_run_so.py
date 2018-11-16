# coding:utf-8
#===============================================================
## 1. usage: _vinaanal [option]  [txt_file]  ##
## no args  will get all txt file, plt all and score all.  pltmmgbsa also include [this will expand X_range=(-70,0)
# option are: [empty, grep, plt, score, allgrep, allpltscore]
# txt_file are: [empty, all, txt_file]
## 2. functions:  
# a). grep *log.txt > result_ID_inhibtor_vina.txt; grep *.dok > result_ID_decoy_vina.txt; 
# b). use pd process, and use plt make pictures.
# c). use score to make scatter pictures
# note: anal txt_file can be in any fold; but grep will only grisp result to to analysis_fold
## note: compare with version 0.2,this 0.2b try to include TCMPOS and TCMNEG part.
import os,sys,glob,re
import pandas as pd
#import matplotlib.mlab as mlab    
import matplotlib.pyplot as plt 
from scipy.stats import ttest_ind
from scipy.stats import linregress
from sklearn.linear_model import LinearRegression
import numpy,math
import time
from vina_analysis_0_2d_lib_so import *
def main():
	try:
		args = sys.argv[1:]
		print('args = sys.argv[1:] = ',args)
	except:
		print('usage is: ????')
		print('no args was found, will fetch all, and plot all')
	if len(args) > 0:	
		if args[0].startswith('-h') or args[0].startswith('-help') or args[0].startswith('--help'): return		
		
	if args == []:
		fetch_vina_ledock_smina()
		#time.sleep(0.05)
		plt_dis_all_result()
		eva_score_all_result()
		return
	if len(args)==1:
		if ('all' == args[0]) or ('alltxt' == args[0]) or ('pltscore' == args[0]) or ('all' in args[0] and 'pltscore' in args[0]):
			plt_dis_all_result()
			eva_score_all_result()					
		if 'grep' == args[0] or ('all' in args[0] and 'grep' in args[0]):
			fetch_vina_ledock_smina()		
			return		
		if 'plt' == args[0] or ('all' in args[0] and 'plt' in args[0]):
			plt_dis_all_result()	
			return
		if 'score' == args[0] or ('all' in args[0] and 'score' in args[0]):
			eva_score_all_result()	
			return			
	if len(args)==2:
		if 'mmgbsa' in args[0]:
			global X_range
			X_range=(-70,0) ## 	
		if 'plt' in args[0]:
			if 'all' == args[1]:
				plt_dis_all_result()
				return
			txt_file=args[1]  ## plot distribution
			plt_dis_one_result(txt_file)
		if 'score' in args[0]:
			if 'all' == args[1]:
				eva_score_all_result()
				return
			txt_file=args[1]
			eva_score_one_result(txt_file)
		if ('plt' in args[0]) or ('score' in args[0]):
			if 'all' == args[1]:
				plt_dis_all_result()
				eva_score_all_result()
				return
			txt_file=args[1]
			plt_dis_one_result(txt_file)
			return		
if __name__=='__main__':
	main()
                
