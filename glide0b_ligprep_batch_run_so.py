# coding:utf-8

import os,sys,glob,re
import psutil   ## this is far better than using os.system, os.popen, subprocess, with ps aux. 
import time
from glide0b_ligprep_batch_lib_so import *
def main():
	os.chdir(base)
	if not os.path.exists('glide_ctrl_file'):
		os.system("cp /home/admin/lib_so_for_open_use/glide_ctrl_file ./")
	input("note: must be sdf filetype\nplease modify the ligprep parameters in glide_ctrl_file, then enter !")		
	## run the two for in loop. 
	os.chdir(base)
	NJOBS_ligprep, HOST, sleep_time_ligprep, forcefield_ligprep,max_cpu_percent, EPIK_METAL_BINDING_ligprep = read_glide_ctrl_file()
	### below the is excellent. match the desired title, and sdf or maegz, but not record the later
	pat_lig = re.compile("(.*?)\.sdf")     
	if len(glob.glob('*.sdf')) == 0: print('no sdf ligand file in current fold');return
	for lig in glob.glob('*.sdf'):
		if lig.startswith('ligprep'): print('will escapte this ligprep sdf file: {lig}'.format(lig=lig)); continue
		while True:
			xx_percent = float(psutil.cpu_percent())
			print(' current psutil.cpu_percent(), max_cpu_percent = ', xx_percent, max_cpu_percent)
			if xx_percent < float(max_cpu_percent):					
				print('job allowed, cpu_percent not exceed {}'.format(max_cpu_percent))
				break
			else:
				print('job NOT allowed, cpu_percent EXCEED {}, 1.5 min later will try again'.format(max_cpu_percent))
				time.sleep(90)   ## 600 seconds, 10 minutes
			print('about to process lig:{lig} '.format(lig=lig))
		mat_lig = re.findall(pat_lig, lig)
		print('mat_lig, pat_lig, lig = ', mat_lig, pat_lig, lig)
		lig_base = mat_lig[0].replace('-out','').replace('_out','')    ## remove  'out'
		"""
		if forcefield_ligprep == 'opls3':	ligprep_fold = 'ligprep_{lig_base}'.format(lig_base=lig_base)
		elif forcefield_ligprep == 'opls2005':	ligprep_fold = 'ligprep_{lig_base}_op05'.format(lig_base=lig_base)
		"""
		ligprep_fold = 'ligprep_{}{}{}'.format(lig_base,dic_for_name_ff[forcefield_ligprep],dic_for_name_EPIK_METAL[EPIK_METAL_BINDING_ligprep])
		os.chdir(base)
		if os.path.exists(ligprep_fold):print("the ligprep fold: {} already exists".format(ligprep_fold));continue			
		os.mkdir(ligprep_fold)
		os.system("cp {lig} {ligprep_fold}/ligprep_{lig_base}.sdf".format(lig=lig,ligprep_fold=ligprep_fold,lig_base=lig_base))
		ligprep_inp_file, OUT_MAE_file = write_ligprep_inp_file_and_run_cmd(ligprep_fold,lig_base,lig)
		print('job: {ligprep_inp_file} has just started'.format(ligprep_inp_file=ligprep_inp_file))
		xx_sleep_time = int(sleep_time_ligprep) if sleep_time_ligprep != '' else 60
		print('will sleep for {} seconds'.format(str(xx_sleep_time)));time.sleep(xx_sleep_time)  ## need to stop for a while
			
	print('all pending job have been started, please using schdg maestro to monitor the status of these jobs')
	print('next copy the OUT_MAE_file, del the ligprep fold, and del get ready glide-gride file and \nrun cmd:  _glide1_batch ')
	return
if __name__ == "__main__":
	main()


