# coding:utf-8

import os,sys,glob,re
import psutil   ## this is far better than using os.system, os.popen, subprocess, with ps aux. 
import time
from glide0c_redock_ligExp_lib_so import *
def main():
	os.chdir(base)
	if not os.path.exists('glide_ctrl_file'):
		os.system("cp /home/phzd/g09E/schrdg/glide_ctrl_file ./")
	input("Reminder: please modify parameters in glide_ctrl_file, then enter !")		
	## run the two for in loop. 
	os.chdir(base)
	NJOBS,HOST,POSTDOCK_NPOSE,PRECISION,max_cpu_percent,sleep_time = read_glide_ctrl_file()
	pat_grid = re.compile("glide-grid_(\w+.*?\w+)\.zip")
	if len(glob.glob('*grid*/ligExp*.sdf')) == 0: print('no ligExp*.sdf in grid folds');return
	if len(glob.glob('*grid*/glide-grid_*.zip')) == 0: print('no receptor in grid folds');return
	for PRECISION in ['XP', 'SP', 'HTVS']:
		os.chdir(base)
		for grid_zip in glob.glob("glide-grid*/glide-grid_*.zip"):
			os.chdir(base)
			#grid_zip_tail = grid_zip.split('/')[1]
			grid_fold, grid_zip_tail = grid_zip.split('/')
			for lig in glob.glob(grid_fold +'/ligExp*.sdf'):
				os.chdir(base)
				while True:
					xx_percent = float(psutil.cpu_percent())
					print(' current psutil.cpu_percent(), max_cpu_percent = ', xx_percent, max_cpu_percent)
					if xx_percent < float(max_cpu_percent):					
						print('job allowed, cpu_percent not exceed {}'.format(max_cpu_percent))
						break
					else:
						print('job NOT allowed, cpu_percent EXCEED {}, 10 Seconds later will try again'.format(max_cpu_percent))
						time.sleep(10)   ## 600 seconds, 10 minutes
				print('about to process lig:{lig} with receptor:{grid_zip}'.format(lig=lig,grid_zip=grid_zip))
				lig_base = lig.split('/')[1].split('.')[0]    ## remove  'out'
				mat_grid = re.findall(pat_grid, grid_zip_tail)
				grid_base = mat_grid[0]	
				print('grid_base = ',grid_base)
				print('mat_grid, pat_grid, grid_zip = ', mat_grid, pat_grid, grid_zip_tail)
				glide_fold = 'glide-dock_{PRECISION}_{grid_base}_{lig_base}'.format(PRECISION=PRECISION,grid_base=grid_base,lig_base=lig_base)
				if os.path.exists(grid_fold + '/' + glide_fold):continue			
				if not os.path.exists(grid_fold + '/' + glide_fold):os.makedirs(grid_fold + '/' + glide_fold)
				glide_in_file = write_glide_in_file_in_grid_fold_and_run_cmd(grid_fold,glide_fold,grid_zip,lig,PRECISION)
				print('job: {glide_in_file} has just started'.format(glide_in_file=glide_in_file))
			
	print('all redock jobs have started, master! after run finished, \nyou might need to run: _glide0d_report_rmsd_for_redock')
	return
if __name__ == "__main__":
	main()
