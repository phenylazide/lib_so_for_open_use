#coding: utf-8
import os,sys,glob,re
import shutil
base=os.getcwd()
os.chdir(base)

print('usage: this_module.py [xx_pdb_ID_remove_list [xx_not_so_good_fold')

def remove_grid_fold_according_removefile(remove_pre_list_file,not_so_good_fold):
	os.chdir(base)
	if not os.path.exists(not_so_good_fold): os.mkdir(not_so_good_fold)
	## remove_pre_list to remove_ID_list	
	f = open(remove_pre_list_file,'r')
	remove_pre_list_txt = f.read()
	remove_pre_list = remove_pre_list_txt.split('\n')
	#pat_remove_ID = re.compile('(?:HTVS|SP|XP)_(\w+)')
	#mat_remove_ID = re.findall(pat_remove_ID, remove_pre_list_txt)
	#remove_ID_list = mat_remove_ID
	remove_ID_list = remove_pre_list
	pat_grid = re.compile('glide-grid_(\w+)')
	for grid in glob.glob('glide-grid_*'):
		mat_grid = re.findall(pat_grid, grid)
		if mat_grid[0] in remove_ID_list:
			shutil.move(grid,'{}/'.format(not_so_good_fold))
			print('done move with grid: {}'.format(grid))

def main():
	try: 
		args = sys.argv[1:]
	except: 
		print('no args was found')
	remove_pre_list_file = 'remove_list'
	not_so_good_fold = 'not_so_good'
	if len(args) > 0:	
		if args[0].startswith('-h') or args[0].startswith('-help') or args[0].startswith('--help'): return	
	if len(args) > 0: remove_pre_list_file = args[0]
	if len(args) > 1: not_so_good_fold = args[1]
	if not os.path.exists(remove_pre_list_file): 
		print('no remove_pre_list_file was found')
		remove_pre_list_file = input('please input the remove_file then Enter\n')
	remove_grid_fold_according_removefile(remove_pre_list_file,not_so_good_fold)
	
if __name__ == '__main__':
	main()
