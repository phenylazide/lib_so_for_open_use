import os,glob,sys
from pymol import cmd
#====== input parameters here ======
x_chains = ['A'] 
## ====== end input parameters =====

base=os.getcwd()
print('base =',base)

os.chdir(base)
if not os.path.exists('splitted_pdbs'):
	os.mkdir('splitted_pdbs')
#for f in glob.glob('????.pdb'):	
for f in glob.glob('*.pdb'):	
	pdb_file = f	
	f = f[:-4]
	path = '{}/{}.pdb'.format(base,f)
	if os.path.exists(path):		
		cmd.delete('*')
		cmd.load(path, quiet=0)
		for x_chain in cmd.get_chains():
			print('x_chain = ',x_chain)
			cmd.select('sele', 'chain {}'.format(x_chain))
			new_file = '{}_{}.pdb'.format(f,x_chain)
			new_path = '{}/splitted_pdbs/{}'.format(base,new_file)
			print('new_file,new_path =',new_file,new_path)
			print('path,new_path,f,pdb_file =',path,new_path,f,pdb_file)
			cmd.save(new_path,'((sele))')	

os.chdir(base)
for f in glob.glob('????.cif'):	
	pdb_file = f	
	f = f[:-4]
	path = '{}/{}.cif'.format(base,f)
	if os.path.exists(path):		
		cmd.delete('*')
		cmd.load(path, quiet=0)
		for x_chain in cmd.get_chains():
			print('x_chain = ',x_chain)
			cmd.select('sele', 'chain {}'.format(x_chain))
			new_file = '{}_{}.pdb'.format(f,x_chain)
			new_path = '{}/splitted_pdbs/{}'.format(base,new_file)
			print('new_file,new_path =',new_file,new_path)
			print('path,new_path,f,pdb_file =',path,new_path,f,pdb_file)
			cmd.save(new_path,'((sele))')	

print('done split pdb chains!\nNOET:!!!!! please check splitted_pdbs fold, and DELETE THE SHORT CHIANS according pdb file size\n after that, Then: run _glide01_align_prep')




