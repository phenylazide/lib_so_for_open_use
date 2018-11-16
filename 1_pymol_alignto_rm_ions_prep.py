# coding: utf-8
from __future__ import print_function
import os,glob,re
from pymol import cmd
import multiprocessing 
import psutil
#====== input parameters here ======
default_batch = 15
default_extending = 5.0
default_exhaustiveness = 8
default_ncpu = 2
vina_parameters_file = 'vina_parameters.txt'

## ====== end input parameters =====
print('this is pymol run module, including: load all pdb, align,removeions, save align pdb and preparewizard\nalso can use the cmd:  save_sele_as_ligExp')

base=os.getcwd()
print('base =',base)
os.chdir(base)

def removeions():
	cmd.select("Ions", "((resn PO4) | (resn SO4) | (resn ZN) | (resn CA) | (resn MG) | (resn CL) | (resn NA)) & hetatm") 
	cmd.remove("Ions")
	cmd.delete("Ions")
	return
	
def save_sele_as_ligExp(selection = 'sele'):
	([minX, minY, minZ],[maxX, maxY, maxZ]) = cmd.get_extent(selection)
	pdb_base = cmd.get_object_list(selection)[0]
	cmd.disable('*')
	cmd.enable('pdb_base',1)
	replace_list = ['_aligned_rm_ion','_aligned','_rm', '_ion','_preped']
	pdb_base_short = pdb_base
	for rep in replace_list: pdb_base_short = pdb_base_short.replace(rep,'')
	cmd.save('ligExp_' + pdb_base_short + ".sdf", 'sele', -1, 'sdf')
	cmd.delete('sele')
	#cmd.disable(pdb_base)
	cmd.delete(pdb_base)
	return
	
print('start loading all pdb file to pymol')
pdbs = glob.glob('*.pdb')
batch = len(pdbs) if len(pdbs) <= default_batch else default_batch
pool = multiprocessing.Pool(batch)
#obj_names = cmd.get_names("all")
for f in pdbs:	
	print('f=',f)
	pdb_file = f
	pdb_base = f[:-4]
	path = '{}/{}'.format(base,pdb_file)
	cmd.load(path, quiet=0)
pool.close()
pool.join()

print('about to alignto, zoom, and removions')
cmd.do('''alignto''')
cmd.do('''zoom''')
removeions()
cmd.remove('solvent')

print('about to save the aligned_rm_ion pdb')
aligned_rm_fold = 'aligned_rm_fold'
if not os.path.exists(aligned_rm_fold): os.mkdir(aligned_rm_fold)
obj_names = cmd.get_names("all")
batch = len(obj_names) if len(obj_names) <= default_batch else default_batch
pool = multiprocessing.Pool(batch)
for obj in obj_names:
	print('obj=',obj)
	if '_01' == obj: continue   ## don't know how come is _01
	pdb_base = obj
	save_ab_path = '{}/{}/{}.pdb'.format(base,aligned_rm_fold,pdb_base)
	cmd.save(save_ab_path, pdb_base, -1, 'pdb')
pool.close()
pool.join()
cmd.delete('*')


## preparewizard
os.chdir(aligned_rm_fold)
command = 'python /home/phzd/g09E/schrdg/glide0a_prepwized_all.py'
os.system(command)

preped_fold = '../preped_fold'
if not os.path.exists(preped_fold): os.mkdir(preped_fold)
command = 'mv *preped.pdb {}/'.format(preped_fold)
os.system(command)
os.chdir(preped_fold)
pdbs = glob.glob('*.pdb')
batch = len(pdbs) if len(pdbs) <= default_batch else default_batch
pool = multiprocessing.Pool(batch)
#obj_names = cmd.get_names("all")
for f in pdbs:	
	print('f=',f)
	pdb_file = f
	pdb_base = f[:-4]	
	cmd.load(pdb_file, quiet=0)
pool.close()
pool.join()

print('all job of load pdbs, alignto, removeions, preparewizard, load preped pdb have been done, master!\nNext you might need to check the fold: preped_fold, and select the each ligand, and command: save_sele_as_ligand')

cmd.extend("save_sele_as_ligExp",save_sele_as_ligExp)

