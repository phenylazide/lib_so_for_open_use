# coding:utf-8
import os,sys
import pandas as pd
print('this module is major for pre-process schrodinger resulting csv file\nfunctions: \n1.groupmin_sort score;\n2. groupmin_sort LE;\n3.remove duplicate of REOS; \n4.fetchcol. this maybe applicable to txt_file')
print('tpypical usage:_vinaanaylpre [optional] [req: xxx.xlsx | xxx.csv | xxx.txt] \n optinal can be: le,,REOS,REOSTitle(title),fetchcol\n')
print("examples: 1. _vinapre xx.csv\n2. _vinapre le[LE] le_xx.csv\n3. _vinapre REOS[title] xx.csv\n4. _vinapre fetchcol 2 xx.csv\n_vinapre fetchcol 'Title' xx.csv")
if sys.version_info.major==2:
	reload(sys)
	sys.setdefaultencoding('utf-8')
from vina_pre_process_data_0_2_lib_so import *
def main():
	try:
		args = sys.argv[1:]
		print('args = ', args)
	except:
		print('no file input was found')
		
	if len(args) > 0:	
		if args[0].startswith('-h') or args[0].startswith('-help') or args[0].startswith('--help'): return		
		
		
	if len(args) == 1:
		a_file = args[0]
		groupmin_sort_only_csv_xlsx_column2(a_file)
		return
	if len(args) == 2:
		if ('le' ==args[0]) or ('LE' == args[0]):
			#print('fetch here')
			a_file = args[1]
			groupmin_sort_only_csv_xlsx_column3_for_le(a_file)
			return
		if 'REOS' in args[0] or 'reos' in args[0]:
			a_file = args[1]
			df = remove_sort_duplicate_after_REOS(a_file)
			if 'title' in args[0] or 'Title' in args[0]:
				write_only_one_cloumn(df,'Title',a_file)
			return
	if len(args) == 3:
		if 'fetchcol' in args[0]:   ## actully is same funcation as shell script awk print ..
			a_file = args[2]
			if args[1].isdigit():    ## using isdigit() to judgy the input args type
				print('args[1] is a number: {}'.format(args[1]))
				col_num = int(args[1])
				df,file_base = pd_read_file(a_file)	 
				write_only_one_cloumn_by_col_num(df,col_num,a_file)
				return 
			else:
				df,file_base = pd_read_file(a_file)	 
				col_name = args[1]				
				write_only_one_cloumn(df,col_name,a_file)		
				return	
					
	print('something wrong in input, or add new functions here')
if __name__ =='__main__':
	main()


