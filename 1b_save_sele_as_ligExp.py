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
	cmd.select("Ions", "((resn PO4) | (resn SO4) | (resn ZN) | (resn CA) | (resn MG) | (resn CL)) & hetatm") 
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

cmd.extend("save_sele_as_ligExp",save_sele_as_ligExp)

