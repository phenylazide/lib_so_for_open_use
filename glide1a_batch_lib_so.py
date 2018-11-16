# coding:utf-8

import os,sys,glob,re
import psutil   ## this is far better than using os.system, os.popen, subprocess, with ps aux. 
import time
import check_fold
if not check_fold.check_path():print('?? unkonwn error');sys.exit(1)
base=os.getcwd()
os.chdir(base)
print('usage: ?? ')
### ============== input parameters below =============


### =============== end input parameters ================
"""
>>> import psutil
>>> psutil.cpu_count()
72
>>> psutil.cpu_percent()
12.3
"""


def read_glide_ctrl_file():
	"""
	-NJOBS: 40
	-HOST localhost:72
	POSTDOCK_NPOSE   10
	PRECISION   SP
	max_cpu_percent 50
	"""
	f = open('glide_ctrl_file','r')
	txt = f.read()
	f.close()
	pat1 = re.compile('-NJOBS: *(\d+)')
	pat2 = re.compile('-HOST *(localhost:\d+)')
	pat3 = re.compile('POSTDOCK_NPOSE +(\d+)')
	pat3a = re.compile('POSES_PER_LIG +(\d+)')	
	pat4 = re.compile('PRECISION +([A-Z]+)')
	pat5 = re.compile('max_cpu_percent +(\d+)')	
	pat6 = re.compile('sleep_time *= *(\d+)')	
	pat7 = re.compile('MAXATOMS +(\d+)')
	pat8 = re.compile('MAXROTBONDS +(\d+)')
	NJOBS = re.findall(pat1,txt)[0]
	HOST = re.findall(pat2,txt)[0]
	POSTDOCK_NPOSE = re.findall(pat3,txt)[0]
	POSES_PER_LIG = re.findall(pat3a,txt)[0]
	PRECISION = re.findall(pat4,txt)[0]
	max_cpu_percent = re.findall(pat5,txt)[0]
	sleep_time = re.findall(pat6,txt)[0]
	MAXATOMS = re.findall(pat7,txt)[0]
	MAXROTBONDS = re.findall(pat8,txt)[0]
	return NJOBS,	HOST, POSTDOCK_NPOSE,POSES_PER_LIG,PRECISION, max_cpu_percent, sleep_time, MAXATOMS, MAXROTBONDS
		
	
def write_glide_in_file_and_run_cmd(glide_fold,grid_zip,lig):
	NJOBS,	HOST, POSTDOCK_NPOSE,POSES_PER_LIG,PRECISION, max_cpu_percent, sleep_time, MAXATOMS, MAXROTBONDS = read_glide_ctrl_file()
	print('NJOBS,HOST,POSTDOCK_NPOSE, POSES_PER_LIG, PRECISION,max_cpu_percent,sleep_time = ', NJOBS,HOST,POSTDOCK_NPOSE,POSES_PER_LIG,PRECISION,max_cpu_percent,sleep_time)
	glide_full_path = base + '/' + glide_fold
	glide_in_file = glide_fold + '.in'
	os.chdir(glide_full_path)
	if os.path.exists(glide_in_file): return
	POSES_PER_LIG_txt = "POSES_PER_LIG   {}\n".format(POSES_PER_LIG) if int(POSES_PER_LIG) > 1 else ''
	glide_in_txt = "\
CALC_INPUT_RMS   True\n\
GRIDFILE   {x_base}/{grid_zip}\n\
KEEP_SUBJOB_POSES   False\n\
LIGANDFILE   {x_base}/{lig}\n\
MAXATOMS   {MAXATOMS}\n\
MAXROTBONDS   {MAXROTBONDS}\n\
{POSES_PER_LIG_txt}POSTDOCK_NPOSE   {POSTDOCK_NPOSE}\n\
PRECISION   {PRECISION}\n\
WRITEREPT   True".format(x_base=base,grid_zip=grid_zip,lig=lig,POSTDOCK_NPOSE=POSTDOCK_NPOSE,POSES_PER_LIG_txt=POSES_PER_LIG_txt, PRECISION=PRECISION,MAXATOMS=MAXATOMS, MAXROTBONDS=MAXROTBONDS)

#POSE_OUTTYPE   ligandlib_sd\n\

	f = open(glide_in_file, 'w')
	f.write(glide_in_txt)
	f.close()
	cmd = "/opt/schrodinger2017-4/glide {glide_in_file} -OVERWRITE -NJOBS {NJOBS} -HOST 'localhost:72' -TMPLAUNCHDIR -ATTACHED".format(glide_in_file=glide_in_file,NJOBS=NJOBS)
	os.system(cmd)
	return glide_in_file

def main():
	os.chdir(base)
	if not os.path.exists('glide_ctrl_file'):
		os.system("cp /home/phzd/g09E/schrdg/glide_ctrl_file ./")
	input("Reminder: please modify parameters in glide_ctrl_file, then enter !")		
	## run the two for in loop. 
	os.chdir(base)
	NJOBS,HOST,POSTDOCK_NPOSE,POSES_PER_LIG,PRECISION,max_cpu_percent,sleep_time,MAXATOMS,MAXROTBONDS = read_glide_ctrl_file()
	### below the is excellent. match the desired title, and sdf or maegz, but not record the later
	pat_lig = re.compile("ligprep_(\w+.*?\w+)\.(?:sdf|maegz)")     
	# ligprep_gsk3beta_chembl_IC50-out.maegz,   ligprep_xx-out.sdf
	#ligprep_irak4_first4_out.maegz, ligprep_irak4_first4_out.sdf
	pat_grid = re.compile("glide-grid_(\w+.*?\w+)\.zip")
	if len(glob.glob('ligprep_*.*')) == 0: print('no ligand in current fold');return
	for lig in glob.glob('ligprep_*.*'):    #ligprep_gsk3beta_chembl_IC50_new_FT-out.maegz
		os.chdir(base)
		if len(glob.glob('*grid*/glide-grid_*.zip')) == 0: print('no receptor in current fold');return
		for grid_zip in glob.glob("glide-grid*/glide-grid_*.zip"):
			grid_zip_tail = grid_zip.split('/')[1]
			# control cpu
			os.chdir(base)
			while True:
				xx_percent = float(psutil.cpu_percent())
				print(' current psutil.cpu_percent(), max_cpu_percent = ', xx_percent, max_cpu_percent)
				if xx_percent < float(max_cpu_percent):					
					print('job allowed, cpu_percent not exceed {}'.format(max_cpu_percent))
					break
				else:
					print('job NOT allowed, cpu_percent EXCEED {}, 0.5 min later will try again'.format(max_cpu_percent))
					time.sleep(30)   ## 600 seconds, 10 minutes
			print('about to process lig:{lig} with receptor:{grid_zip}'.format(lig=lig,grid_zip=grid_zip))
			mat_lig = re.findall(pat_lig, lig)
			#print('mat_lig, pat_lig, lig = ', mat_lig, pat_lig, lig)
			lig_base = mat_lig[0].replace('-REOS','').replace('_REOS','').replace('-out','').replace('_out','')    ## remove  'out'
			mat_grid = re.findall(pat_grid, grid_zip_tail)
			grid_base = mat_grid[0]	
			#print('mat_grid, pat_grid, grid_zip = ', mat_grid, pat_grid, grid_zip_tail)
			glide_fold = 'glide-dock_{PRECISION}_{grid_base}_{lig_base}'.format(PRECISION=PRECISION,grid_base=grid_base,lig_base=lig_base)
			if os.path.exists(glide_fold):continue			
			os.mkdir(glide_fold)
			glide_in_file = write_glide_in_file_and_run_cmd(glide_fold,grid_zip,lig)
			print('job: {glide_in_file} has just started'.format(glide_in_file=glide_in_file))
			xx_sleep_time = int(sleep_time) if sleep_time != '' else 60
			print('will sleep for {} seconds'.format(str(xx_sleep_time)));time.sleep(xx_sleep_time)  ## need to stop for a while
			
	print('all pending job have been started, please using schdg maestro to monitor the status of these jobs')
	print('next run cmd: _glide2 (i.e. _glide2a_post_process && _glide2b_anal) ')
	return
if __name__ == "__main__":
	main()


