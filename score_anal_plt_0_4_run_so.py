# coding:utf-8
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals

import argparse
#===============================================================
import os,sys,glob,re
import pandas as pd
import matplotlib.pyplot as plt 
from scipy.stats import ttest_ind;from scipy.stats import linregress;from sklearn.linear_model import LinearRegression;from sklearn.metrics import roc_curve, roc_auc_score
import numpy,math

if sys.version_info.major==2:
	reload(sys)
	sys.setdefaultencoding('utf-8')
from score_anal_plt_0_4_lib_so import *
def main():
	parser = argparse.ArgumentParser(
		  description='score hist scatter roc anal')
		  
	parser.add_argument(
    '-a','--actions',
    nargs='*',
    default=[],
    help="Choice:('hist' or 'plt'), ('scatter' or 'score'),(roc or ROC),'vina','grep',default is [] which will do 'plt','score', if 'vina','grep' might bugs")
		  
	parser.add_argument(
    '-f','--files',
    nargs='*',
    default=[],
    help="input files lists, can be viod. If viod, will use glob.glob('*.txt')")
    
	parser.add_argument(
    '-rd','--X_range_downlimit',    
    type=int,
    default=-9999,
    help='X_range_downlimit')

	parser.add_argument(
    '-ru','--X_range_uplimit',
    type=int,
    default=-9999,
    help='X_range_uplimit')

	parser.add_argument(
    '-cols','--column_num_or_names',
    nargs='*',
    default=[''],
    help="column_num_or_name list, choice might be: r_i_docking_score r_i_glide_gscore vina ledock etc\n also can be numbers: such as: 1 2 3;default is [''] which will use df.columns[1] only")

	args = parser.parse_args()
	files = args.files; actions = args.actions;print('files, actions = ', files, actions)
	X_range_downlimit = args.X_range_downlimit; X_range_uplimit = args.X_range_uplimit
	column_num_or_names = args.column_num_or_names
	
	if 'vina' in actions:
		X_range = default_X_range
		set_column_num_or_name =''
		fetch_vina_ledock_smina()
		plt_dis_all_result_for_vina_ledock(analysis_fold,X_range,set_column_num_or_name)
		eva_score_all_result_for_vina_ledock(analysis_fold,set_column_num_or_name)
		return

	if len(actions) ==0: actions = ['plt', 'score']
	if 'grep' in actions: fetch_vina_ledock_smina()
	
	def set_X_range(xx_txt):		
		if (X_range_downlimit == -9999) and (X_range_uplimit == -9999): 
			if 'mmgbsa' in xx_txt: return (-70, 0)
			else: return default_X_range
		downlimit = X_range_downlimit if X_range_downlimit != -9999 else -14
		uplimit = X_range_uplimit if X_range_uplimit != -9999 else 0	
		return (downlimit,uplimit)		
	
	if len(files) ==0: files = glob.glob('*.txt');print('files = ', files)
	for xx_txt in files: 
		X_range = set_X_range(xx_txt);print('X_range = ', X_range)
		for set_column_num_or_name in column_num_or_names:
			if ('hist'in actions) or ('plt'in actions) : plt_hist_one_txt(xx_txt,X_range,set_column_num_or_name)
			if ('roc'in actions) or ('ROC'in actions) :print('here');ROC_one_txt_new(xx_txt,set_column_num_or_name)
			if ('scatter'in actions) or ('score' in actions):
				eva_score_one_result(xx_txt,set_column_num_or_name)
				""" 
				try:eva_score_one_result(xx_txt)
				except:	print('error: failed to eva_score_one_result for :: {}'.format(xx_txt))
				"""
	return

if __name__=='__main__':
	main()
                
