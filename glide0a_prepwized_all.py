#coding:utf-8
import os,glob,sys
import time
import shutil,psutil
##==================== input parameters below ==============
prepwizard='/opt/schrodinger2017-4/utilities/prepwizard -rehtreat -fillsidechains -watdist 0 -samplewater -minimize_adj_h -delwater_hbond_cutoff 3 -rmsd 0.3 -f 3 -HOST localhost:72'   # -fillloops   -ph PH  -captermini   ### -HOST localhost:72  seems very important when deal with multi files
### has tried several times on 4ZTM_A, 5T8O_A;  _glide01_align_prep and _glide0a_prepwized_all no diff
### but -fillloops seems poor than without this.
desire_prep_file_types = ['pdb']  #['pdb','maegz']
#default_WATDIST ='5'  ## 5A
#default_DELWATER_HBOND_CUTOFF = '3'
max_cpu_percent = 50
##====================== end input parameters ===============
print("note: will only process the pdb files in current fold, NOT accept maegz file as input")
base=os.getcwd()
os.chdir(base)
tmp_fold = 'prepwized_tmp'
if not os.path.exists(tmp_fold): os.mkdir(tmp_fold)
for file_ext in desire_prep_file_types:
	cp_patten = ' '.join(['*.'+i for i in desire_prep_file_types])
	os.system('cp {} {}/'.format(cp_patten,tmp_fold))

tmp_full_path = base + '/' + tmp_fold

all_preped_list = []
os.chdir(tmp_full_path)
for file_ext in desire_prep_file_types:
	for f in glob.glob('*.{}'.format(file_ext)):
		while True:
			xx_percent = float(psutil.cpu_percent())
			print(' current psutil.cpu_percent(), max_cpu_percent = ', xx_percent, max_cpu_percent)
			if xx_percent < float(max_cpu_percent):					
				print('job allowed, cpu_percent not exceed {}'.format(max_cpu_percent))
				break
			else:
				print('job NOT allowed, cpu_percent EXCEED {}, 10 Seconds later will try again'.format(max_cpu_percent))
				time.sleep(10)   ## 600 seconds, 10 minutes
		file_base = f.split('.')[0]
		cmd = "{prepwizard} {f} {file_base}_preped.{file_ext}".format(prepwizard=prepwizard,f=f,file_base=file_base,file_ext=file_ext) ### -rehtreat, will remove original H
		print(' starting preped file: {} ... '.format(f))		
		print("cmd  = ", cmd + ' & ')
		#os.system(cmd + ' & ')   ## seem [(no need) or (can NOT use)] &, might cause other file generate same preped.pdb
		os.system(cmd)
		time.sleep(0.5)
		all_preped_list.append("{file_base}_preped.{file_ext}".format(file_base=file_base,file_ext=file_ext))


## check if all preped files are done
working_list = [x for x in all_preped_list]
while True:
	all_done = False
	os.chdir(tmp_full_path)	
	for f in working_list:
		if os.path.exists(f):
			print('done with file: {}'.format(f))
			shutil.copyfile(f,'../'+f);os.chdir(tmp_full_path)	
			working_list.remove(f);all_done = True;continue
		else:
			all_done = False;print('file: {} was not done, will check again soom'.format(f))
			break
	if all_done == True: break
	time.sleep(10)
print('all preped are done')

## again move, make sure all moved
os.chdir(tmp_full_path)	
print('current fold is : {}'.format(os.getcwd()))
print('glob.glob("*_preped.*") = ', glob.glob("*_preped.*"))

#for f in glob.glob("*_preped.*"):
	#print('current fold is : {}'.format(os.getcwd()))
	#shutil.copyfile(f,'../')

preped_list_txt = ' '.join(all_preped_list)
os.system("cp {} ../".format(preped_list_txt))  
print('all preped have been moved in current fold,list is: {}'.format(preped_list_txt))	

os.chdir(base)

