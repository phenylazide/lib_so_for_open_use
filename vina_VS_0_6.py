# coding: utf-8
import os,sys,glob,re,random
import multiprocessing 
#note: this version will only use mol2 filetype for ligands
#base=os.getcwd()
print('usage is: one arg is chosen options from [prepare_pdbqt,check_mol2,move_ligands,VS,whole,VS_ledock,whole_ledock,VS_smina,whole_smina,[batch_num]\nnote:[batch_num] is optional,if missing default is 25\nnew function: _vina randomdelmol2 0.9 ## random del mol2file in mol2 fold, 0.9 means 90%\n and if _vina randomdelmol2 local_fold 0.9 : this will del 90% files in the specific local_fold')
base = '/home/phzd/dock_flat'
reverse_base = '/home/phzd/dock_flat/reverse_VS'
reverse_JOBS = '/home/phzd/dock_flat/reverse_JOBS'
os.chdir(base)
if not os.path.exists('ligands'):
	os.makedirs('ligands')
	print('please input your ligands, will try cp ligands from the [mol2] fold')
	if not os.path.exists('mol2'):
		print('no [ligands] fold was found, neither [mol2] fold was found') 
		sys.exit("error: no ligand was found!")

prepare_ligand4 = '/home/phzd/MGLTools-1.5.6/bin/python /home/phzd/MGLTools-1.5.6/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_ligand4.py'

def prepare_pdbqt(batch):
	os.chdir(base)
	os.system('cp mol2/* ligands/')
	pool = multiprocessing.Pool(batch)
	for f in glob.glob('ligands/*.mol2'):  # 
		file_base = f[len('ligands/'):-5]   
		#print('file_base=',file_base)
		#os.system('{} -l {} -A hydrogens'.format(prepare_ligand4,f))
		if not os.path.exists('ligands/{}.pdbqt'.format(file_base)):
			arg = '{0} -l {1} -A hydrogens -F -o ligands/{2}.pdbqt'.format(prepare_ligand4,f,file_base)
			pool.apply_async(os.system,(arg, ))
			#os.system('{0} -l {1} -A hydrogens -o ligands/{2}.pdbqt'.format(prepare_ligand4,f,file_base))
		#print('success processing ligand {}'.format(f))
	pool.close()
	pool.join()	
	print('job prepare_pdbqt done') 
	return

#def prepare_mol2(batch):
def check_mol2_fold():
	"""
	#os.chdir(base+'/pdb')
	#os.system('/usr/bin/obabel *.pdb -O *.mol2')
	os.chdir(base)
	if not os.path.exists('mol2'):
		os.makedirs(base+'/mol2')
		print('NO mol2 fold was found') 
	#os.system('mv pdb/*.mol2 mol2/')
	print('mol2 fold was found here') 
	"""
	os.chdir(base)
	if not os.path.exists('mol2'):
		sys.exit("error: NO mol2 fold was found for ligands!")
	elif len(glob.glob('mol2/*.mol2')) ==0:
		sys.exit("error: mol2 fold was found, but has NO ligands here!")
	number = len(glob.glob('mol2/*.mol2'))
	firstligand = glob.glob('mol2/*.mol2')[0]
	lastligand = glob.glob('mol2/*.mol2')[-1]
	print('mol2 files are ready to dock, contains {} ligands\nthe fist ligand is: {}\nthe last ligand is: {} '.format(number,firstligand,lastligand))
	return
"""
def single_vina(r_base,ligand_ab_path,l_base):
	os.chdir(base)
	os.system('/bin/bash vina_Single_process.sh {} {} {}'.format(r_base,ligand_ab_path,l_base))
	return
"""

def single_vina(r_base,ligand_ab_path,l_base):
	os.chdir(base)
	pdb_fold='{}/execte/{}'.format(base,r_base)
	bash_lines= "echo Processing ligand {2}	&& \
							/usr/local/bin/vina --config {3}/config_linux.txt --ligand {1} --out {3}/out/{2}_out.pdbqt --log {3}/out/{2}_log.txt --cpu 2 && \
							echo success vinaed ligand {2} && \
							mv {1} {4}/ligands_docked/".format(r_base,ligand_ab_path,l_base,pdb_fold,base)
	os.system(bash_lines)
	return

def single_qvina(r_base,ligand_ab_path,l_base):
	os.chdir(base)
	pdb_fold='{}/execte/{}'.format(base,r_base)
	bash_lines= "echo Processing ligand {2}	&& \
							/usr/local/bin/qvina --config {3}/config_linux.txt --ligand {1} --out {3}/out_qvina/{2}_out.pdbqt --log {3}/out_qvina/{2}_log.txt --cpu 2 && \
							echo success vinaed ligand {2} && \
							mv {1} {4}/ligands_docked/".format(r_base,ligand_ab_path,l_base,pdb_fold,base)
	os.system(bash_lines)
	return

def single_smina(r_base,ligand_ab_path,l_base):
	os.chdir(base)
	pdb_fold='{}/execte/{}'.format(base,r_base)
	bash_lines= "echo Processing ligand {2}	&& \
							/usr/local/bin/smina --config {3}/config_linux.txt --ligand {1} --out {3}/out_smina/{2}_sm.pdb --log {3}/out_smina/{2}_sm.txt --cpu 2 && \
							echo success sminaed ligand {2} && \
							mv {1} {4}/ligands_docked/".format(r_base,ligand_ab_path,l_base,pdb_fold,base)
	os.system(bash_lines)
	return

def single_ledock(pdb_base,ligand,l_base,i_th_number):
	os.chdir(pdb_base + '/le_flat')
	#os.system('/bin/bash ledock_Single_ligand.sh {} {} {}'.format(ligand,l_base,i_th_number))
	# the i_th ligand's dock.in file;
	# {} is list which has only one file name.
	# in dock.in file,change ligands to i_th
	bash_lines = "echo Processing receptor {3} with ligand {0}, the number is: {2} && \
								cp ../ledock.in {2}.in &&  	\
								echo {0} > {2} &&         \
								sed -i 's/ligands/{2}/g' {2}.in && \
								ledock {2}.in && \
								echo success ledocked ligand {0} && \
								rm -rf {2}.in {2} && \
								mv {0} ../ligands_ledocked/ && \
								mv {1}.dok ../out_ledock/".format(ligand,l_base,i_th_number,pdb_base)
	os.system(bash_lines)
	return

def move_ligands(batch = 10): 
	os.chdir(base)
	os.system('cp {0}/ligands/*.pdbqt {0}/ligands_undocked/'.format(base))
	l_list = glob.glob('/home/phzd/dock_flat/ligands_undocked/*.pdbqt')
	print('l_list = ',l_list)
	if l_list == []:
		return
	if batch == 1:
		if not os.path.exists('ligands_undocked/0'):
			os.makedirs('ligands_undocked/0')		
		os.system('mv ligands_undocked/*.pdbqt ligands_undocked/0/')
		return
	if batch > 1:
		os.chdir('/home/phzd/dock_flat/ligands_undocked/')
		for _i in range(0,batch+1):
			if not os.path.exists(str(_i)):
				os.makedirs(str(_i))
	file_Nu = len(l_list)
	undocked_fold = '/home/phzd/dock_flat/ligands_undocked/'
	_i = 0
	pool = multiprocessing.Pool(batch)
	for i,l in enumerate(l_list):
		if i <= int(file_Nu*(_i+1)/batch):  ## classify here, _i is fold and fold controller
			arg = 'mv {} {}{}'.format(l,undocked_fold,str(_i))
			#os.system('mv {} {}{}'.format(l,undocked_fold,str(_i)))  ## all use ab path
			pool.apply_async(os.system,(arg, ))
		else:                     ## if larger than,then increase _i, i.e. move to next fold
			_i += 1
	pool.close()
	pool.join()
	os.system('mv *.pdbqt {}{}'.format(undocked_fold,str(_i+1)))  ## left over all moved the last fold
	return 

def vs_vina(r,batch = 1): ## r represent receptor;
	os.chdir(base)
	#print('i have been here in vs_vina 1')
	#for r in glob.glob('/home/phzd/dock_flat/execte/*/receptor*.pdbqt'):  # 
	
	#r_base = r.strip('/home/phzd/dock_flat/execte/').rstrip('.pdbqt') 
	#r_base = r[len('/home/phzd/dock_flat/execte/'):len('/home/phzd/dock_flat/execte/')+4] # ID are all 4 letters
	pattern = re.compile('/home/phzd/dock_flat/execte/(.*?)/receptor')
	match = re.findall(pattern,r)
	r_base = match[0]
	print('r_base = ',r_base)
	out_fold = '/home/phzd/dock_flat/execte/{}/out'.format(r_base)
	if not os.path.exists(out_fold):
		os.makedirs(out_fold)
	pool = multiprocessing.Pool(processes = batch)
	for _i in range(batch+1):
		print('_i in range(batch+1): _i = ',_i)
		c_l_fold = '{}/ligands_undocked/{}'.format(base,str(_i))
		os.chdir(c_l_fold)
		for l in glob.glob('*.pdbqt'):
			l_base = l[:-6]
			#pattern1 = re.compile('/ligands_undocked/\d+/(.*?)\.pdbqt')
			#match1 = re.findall(pattern1,l)
			#l_base = match1[0]
			#l_base = l.strip(c_l_fold + '/').rstrip('.pdbqt')
			l_ab_path = '{}/{}'.format(c_l_fold,l)
			pool.apply_async(single_vina,(r_base,l_ab_path,l_base, ))  # args=(r_base,l_ab_path,l_base,)
	pool.close()
	pool.join()
	print('congrat!! all ligands and receptor have been docked')
	return

def vs_qvina(r,batch = 1): ## r represent receptor;
	os.chdir(base)
	pattern = re.compile('/home/phzd/dock_flat/execte/(.*?)/receptor')
	match = re.findall(pattern,r)
	r_base = match[0]
	print('r_base = ',r_base)
	out_fold = '/home/phzd/dock_flat/execte/{}/out_qvina'.format(r_base)
	if not os.path.exists(out_fold):
		os.makedirs(out_fold)
	pool = multiprocessing.Pool(processes = batch)
	for _i in range(batch+1):
		print('_i in range(batch+1): _i = ',_i)
		c_l_fold = '{}/ligands_undocked/{}'.format(base,str(_i))
		os.chdir(c_l_fold)
		for l in glob.glob('*.pdbqt'):
			l_base = l[:-6]
			#pattern1 = re.compile('/ligands_undocked/\d+/(.*?)\.pdbqt')
			#match1 = re.findall(pattern1,l)
			#l_base = match1[0]
			#l_base = l.strip(c_l_fold + '/').rstrip('.pdbqt')
			l_ab_path = '{}/{}'.format(c_l_fold,l)
			pool.apply_async(single_qvina,(r_base,l_ab_path,l_base, ))  # args=(r_base,l_ab_path,l_base,)
	pool.close()
	pool.join()
	print('congrat!! all ligands and receptor have been docked')
	return

def whole(batch):	### not finished
	os.chdir(base)
	for f in ['ligands','ligands_docked','ligands_undocked',]:
		if not os.path.exists(f):
			fold = '{}/{}'.format(base,f)
			os.makedirs(fold)	
	prepare_pdbqt(batch)
	os.chdir(base)
	for r in glob.glob('/home/phzd/dock_flat/execte/*/receptor*.pdbqt'):
		move_ligands(batch)
		vs_vina(r,batch)

def whole_qvina(batch):	### not finished
	os.chdir(base)
	for f in ['ligands','ligands_docked','ligands_undocked',]:
		if not os.path.exists(f):
			fold = '{}/{}'.format(base,f)
			os.makedirs(fold)	
	prepare_pdbqt(batch)
	os.chdir(base)
	for r in glob.glob('/home/phzd/dock_flat/execte/*/receptor*.pdbqt'):
		move_ligands(batch)
		vs_qvina(r,batch)

def write_single_vina_jobfile(vina_jobfilename,target_name,r_base,ligand_ab_path,l_base):
	os.chdir(base)
	f = open('reverse_JOBS/'+ vina_jobfilename,'w')
	pdb_fold='{}/reverse_VS/{}/{}'.format(base,target_name,r_base)
	bash_lines= "echo Processing ligand {2} with receptor {3}	&& \
	/usr/local/bin/vina --config {3}/config_linux_reverse.txt --ligand {1} --out {3}/out_reverse/{2}_out.pdbqt --log {3}/out_reverse/{2}_log.txt --cpu 2 && \
	echo success vinaed ligand {2} with receptor {3} && \
	mv {4}/reverse_JOBS/{5} {4}/reverse_JOBS/finished".format(r_base,ligand_ab_path,l_base,pdb_fold,base,vina_jobfilename)
	f.write(bash_lines)
	f.close()
	print('success write {} with {} as {} file'.format(r_base,l_base,vina_jobfilename))
	return vina_jobfilename

def write_single_qvina_jobfile(vina_jobfilename,target_name,r_base,ligand_ab_path,l_base):
	os.chdir(base)
	f = open('reverse_JOBS/'+ vina_jobfilename,'w')
	pdb_fold='{}/reverse_VS/{}/{}'.format(base,target_name,r_base)
	bash_lines= "echo Processing ligand {2} with receptor {3}	&& \
	/usr/local/bin/qvina --config {3}/config_linux_reverse.txt --ligand {1} --out {3}/out_qvina_reverse/{2}_out.pdbqt --log {3}/out_qvina_reverse/{2}_log.txt --cpu 2 && \
	echo success qvinaed ligand {2} with receptor {3} && \
	mv {4}/reverse_JOBS/{5} {4}/reverse_JOBS/finished".format(r_base,ligand_ab_path,l_base,pdb_fold,base,vina_jobfilename)
	f.write(bash_lines)
	f.close()
	print('success write {} with {} as {} file'.format(r_base,l_base,vina_jobfilename))
	return vina_jobfilename

def revere_vs_preparation(batch = 1,vina_qvina='vina'): 
## 1 preparation: 
## 1.0 prepare prepare_pdbqt
	prepare_pdbqt(batch)
## 1.1 prepare receptor list, searching all the receptor*.pdbqt, then 
	os.chdir(reverse_base)
	target_name_and_r_base_lists = []
	pattern = re.compile('(\w+)/(.*?)/receptor') # re.compile('/home/phzd/dock_flat/reverse_VS/(\w+)/(.*?)/receptor')
	for r in glob.glob('*/*/receptor*.pdbqt'):
		match = re.findall(pattern,r)
		if match:target_name_and_r_base_lists.append(match)
	print('target_name_and_r_base_lists =',target_name_and_r_base_lists)
## 1.2 make this 'out_reverse' fold, ## 1.3 modify config_linux.txt to config_linux_reverse.txt
	for t_r in target_name_and_r_base_lists:
		target_name, r_base = t_r[0]
		out_reverse_fold = '{}/{}/out_reverse'.format(target_name, r_base)
		out_qvina_reverse_fold = '{}/{}/out_qvina_reverse'.format(target_name, r_base)
		pdb_fold = '{}/{}'.format(target_name, r_base)
		if not os.path.exists(out_reverse_fold):           
			os.makedirs(out_reverse_fold)
		if not os.path.exists(out_qvina_reverse_fold):           
			os.makedirs(out_qvina_reverse_fold)
## 1.3 modify config_linux.txt to config_linux_reverse.txt
		bashline = "cp {0}/config_linux.txt {0}/config_linux_reverse.txt && sed -i 's/execte/reverse_VS\/{1}/g' {0}/config_linux_reverse.txt".format(pdb_fold,target_name)
		os.system(bashline)

## 1.4 write batch reverse_VS jobs
	os.chdir(base)   ## in dock_flat fold
	import time 
	date = time.strftime("%Y-%m-%d")
	reverse_JOBS_fold = 'reverse_JOBS'
	if not os.path.exists(reverse_JOBS_fold):           
		os.makedirs(reverse_JOBS_fold)
	reverse_JOBS_finished_fold = 'reverse_JOBS/finished'
	if not os.path.exists(reverse_JOBS_finished_fold):           
		os.makedirs(reverse_JOBS_finished_fold)
	i = 1
	for l in glob.glob('ligands/*.pdbqt'):
		l_base = l[8:-6]
		l_ab_path = '{}/{}'.format(base,l)
		for t_r in target_name_and_r_base_lists:
			target_name, r_base = t_r[0]
			vina_jobfilename = date + '-{:0>5}'.format(i) + '.reverse'
			if vina_qvina == 'vina':
				write_single_vina_jobfile(vina_jobfilename,target_name,r_base,l_ab_path,l_base)  ## applying this module
			elif vina_qvina == 'qvina':
				write_single_qvina_jobfile(vina_jobfilename,target_name,r_base,l_ab_path,l_base)
			i += 1
	return 

def run_single_reverse_VS(job):
	os.chdir(reverse_JOBS)
	os.system("bash {}".format(job))
	return

def reverse_VS_target_vina(batch,vina_qvina='vina'):
	os.chdir(base)
	if not os.path.exists('ligands'):
		print('no ligands fold was found')
		return
	revere_vs_preparation(batch,vina_qvina)   ### applying this key module
	if not os.path.exists('reverse_JOBS'):           
		print('no reverse_JOBS fold was found')
		return
	pool = multiprocessing.Pool(processes = batch)
	os.chdir(reverse_JOBS)
	for job_file in glob.glob('*.reverse'):
		pool.apply_async(run_single_reverse_VS,(job_file,))  # args=(r_base,l_ab_path,l_base,)
	pool.close()
	pool.join()
	print('congrat!! all ligands and receptor have been docked')
	return

def just_run_reverse_batch_file(batch):
	pool = multiprocessing.Pool(processes = batch)
	os.chdir(reverse_JOBS)
	for job_file in glob.glob('*.reverse'):
		pool.apply_async(run_single_reverse_VS,(job_file,))  # args=(r_base,l_ab_path,l_base,)
	pool.close()
	pool.join()
	print('congrat!! all ligands and receptor have been docked')
	return	
	
	
def vs_smina(r,batch = 1): ## r represent receptor;
	os.chdir(base)
	#print('i have been here in vs_vina 1')
	#for r in glob.glob('/home/phzd/dock_flat/execte/*/receptor*.pdbqt'):  # 
	
	#r_base = r.strip('/home/phzd/dock_flat/execte/').rstrip('.pdbqt') 
	#r_base = r[len('/home/phzd/dock_flat/execte/'):len('/home/phzd/dock_flat/execte/')+4] # ID are all 4 letters
	pattern = re.compile('/home/phzd/dock_flat/execte/(.*?)/receptor')
	match = re.findall(pattern,r)
	r_base = match[0]
	print('r_base = ',r_base)
	out_fold = '/home/phzd/dock_flat/execte/{}/out_smina'.format(r_base)
	if not os.path.exists(out_fold):
		os.makedirs(out_fold)
	pool = multiprocessing.Pool(processes = batch)
	for _i in range(batch+1):
		print('_i in range(batch+1): _i = ',_i)
		c_l_fold = '{}/ligands_undocked/{}'.format(base,str(_i))
		os.chdir(c_l_fold)
		for l in glob.glob('*.pdbqt'):
			l_base = l[:-6]
			#pattern1 = re.compile('/ligands_undocked/\d+/(.*?)\.pdbqt')
			#match1 = re.findall(pattern1,l)
			#l_base = match1[0]
			#l_base = l.strip(c_l_fold + '/').rstrip('.pdbqt')
			l_ab_path = '{}/{}'.format(c_l_fold,l)
			pool.apply_async(single_smina,(r_base,l_ab_path,l_base, ))  # args=(r_base,l_ab_path,l_base,)
	pool.close()
	pool.join()
	print('congrat!! all ligands and receptor have been docked')
	return

def whole_smina(batch):	### not finished
	os.chdir(base)
	for f in ['ligands','ligands_docked','ligands_undocked',]:
		if not os.path.exists(f):
			fold = '{}/{}'.format(base,f)
			os.makedirs(fold)	
	prepare_pdbqt(batch)
	os.chdir(base)
	for r in glob.glob('/home/phzd/dock_flat/execte/*/receptor*.pdbqt'):
		move_ligands(batch)
		vs_smina(r,batch)

def vs_ledock(r,batch = 1): ## r represent receptor;
	os.chdir(base)
	#pattern = re.compile('/home/phzd/dock_flat/execte/(.*?)/rececptor')
	print('r = ',r)
	pattern = re.compile('/execte/(.*?)/f_vina')   # this is better than above one, becasue it is more flexible.
	match = re.findall(pattern,r)
	r_base = match[0]
	#r_base = r.strip('/home/phzd/dock_flat/execte/').restrip('f_vina_h.pdb')
	print('r_base = ',r_base)
	pdb_base = '{}/execte/{}'.format(base,r_base)
	os.chdir(pdb_base)
	for _f in ['le_flat','ligands_ledocked','out_ledock']:
		if not os.path.exists(_f):
			os.makedirs(_f)
	#os.system('cp {0}/mol2/*.mol2 le_flat/ && cp {0}/ledock_Single_ligand.sh le_flat/'.format(base))
	if len(glob.glob('le_flat/*.mol2')) == 0:  #judge whether le_flat has mol2 file. if no,copy mol2 from dock_flat/mol2/*.mol2
		os.system('cp {0}/mol2/*.mol2 le_flat/ '.format(base))  ## this is important,otherwise cannot stop and continue the work.
	os.chdir('le_flat')  
	pool = multiprocessing.Pool(processes = batch)
	i = 0
	for l in glob.glob('*.mol2'):
		l_base = l[:-5]
		pool.apply_async(single_ledock,(pdb_base,l,l_base, str(i)+'_th'))  # args=(r_base,l,l_base,)
		i += 1
	pool.close()
	pool.join()
	print('congrat!! all ligands with receptor {} have been docked'.format(r_base))
	return

def whole_ledock(batch):	
	check_mol2_fold()
	os.chdir(base)
	for r in glob.glob('/home/phzd/dock_flat/execte/*/f_vina_H.pdb'):
		vs_ledock(r,batch)

def random_del_mol2(mol2_fold,cut_off):	
	print('cut_off = ',cut_off)
	os.chdir(mol2_fold)
	for f in glob.glob('*.mol2'):
		if random.random()>cut_off:
			os.remove(f)
	
def main():
	try:
		args = sys.argv[1:]
		print('args = sys.argv[1:] = ',args)
	except:
		print('usage is: one arg is chosen options from [split_sdf,prepare_pdbqt,move_ligands,VS,whole] \nsecond arg is: [batch_num] which is optional,if missing default is 25')
		pass
		return
		
	if 'split_sdf' in args[0]:  ## here used python2, cannot use import method
		L_file_name = args[1]
		S_name_field = args[2]
		os.system('python2 /home/phzd/dock_flat/script/for_split_files/split_sdf_to_mol2.py {} {}'.format(L_file_name,S_name_field))
		return		
	if len(args) == 1:
		if args[0] == 'prepare_pdbqt':
			prepare_pdbqt(20)
			return
		if args[0] == 'move_ligands':
			move_ligands(20)
			return
		if (args[0] == 'VS') or (args[0] == 'vs'):
			r = glob.glob('/home/phzd/dock_flat/execte/*/receptor*.pdbqt')[0]
			vs_vina(r,20)
			return
		if args[0] == 'whole':
			whole(int(20))
			return
		if 'check' in args[0] and 'mol2' in args[0]:
			check_mol2_fold()
			return
		if ('VS' in args[0]) and ('smina' in args[0]):
			r = glob.glob('/home/phzd/dock_flat/execte/*/receptor*.pdbqt')[0]
			vs_smina(r,40)
			return
		if args[0] == 'whole_smina':
			whole_smina(int(40))
		if ('VS' in args[0]) and ('ledock' in args[0]):
			r = glob.glob('/home/phzd/dock_flat/execte/*/f_vina*.pdb')[0]
			vs_ledock(r,40)
			return
		if args[0] == 'whole_ledock':
			whole_ledock(int(40))
			return
		else:
			print('input error or modify here to get new functions')
		return
	if len(args) == 2:
		if args[0] == 'whole':
			batch = int(args[1])
			whole(batch)
			return
		if (args[0] == 'VS') :
			r = glob.glob('/home/phzd/dock_flat/execte/*/receptor*.pdbqt')[0]
			batch = int(args[1])
			vs_vina(r,batch)
			return
		if args[0] == 'prepare_pdbqt':
			batch = int(args[1])
			prepare_pdbqt(batch)
			return
		if args[0] == 'move_ligands':
			batch = int(args[1])
			move_ligands(batch)
			return	
		if 'check' in args[0] and 'mol2' in args[0]:
			batch = int(args[1])
			check_mol2_fold()
			return
		if ('VS' in args[0]) and ('smina' in args[0]):
			r = glob.glob('/home/phzd/dock_flat/execte/*/receptor*.pdbqt')[0]
			batch = int(args[1])
			vs_smina(r,batch)
			return	
		if 'wholesmina' == args[0]:
			batch = int(args[1])
			whole_smina(batch)	
		if 'wholeqvina' == args[0]:
			batch = int(args[1])
			whole_qvina(batch)
		if ('VS' in args[0]) and ('ledock' in args[0]):
			r = glob.glob('/home/phzd/dock_flat/execte/*/f_vina*.pdb')[0]
			batch = int(args[1])
			vs_ledock(r,batch)
			return		
		if 'wholeledock' == args[0]:
			batch = int(args[1])
			whole_ledock(batch)
			return
		if 'random' in args[0] and 'delmol2' in args[0]:  ## random del file in mol2 fold
			mol2_fold = '/home/phzd/dock_flat/mol2'
			cut_off = 1-float(args[1])
			random_del_mol2(mol2_fold,cut_off)
			return
		if 'reverseVS' == args[0]:
			print('doing revers_VS')
			batch = int(args[1])
			reverse_VS_target_vina(batch)
			return
		if 'reverseVSqvina' == args[0]:
			print('doing revers_VS')
			batch = int(args[1])
			reverse_VS_target_vina(batch,'qvina')
			return

		if 'reversebatch' == args[0]:
			print('doing revers_VS')
			batch = int(args[1])
			just_run_reverse_batch_file(batch)
			return				
		else:
			print('input error or modify here to get new functions')
		return
	if len(args) == 3:
		if 'random' in args[0] and 'delmol2' in args[0]:  ## random del file in mol2 fold
			mol2_fold = '{}/{}'.format(base,args[1])
			cut_off = 1-float(args[2])
			random_del_mol2(mol2_fold,cut_off)
			return
	else:
		print('to see usage for detail')
		return
if __name__ == '__main__':
	main()


