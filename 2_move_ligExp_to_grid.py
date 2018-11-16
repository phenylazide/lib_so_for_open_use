import os,glob,re
import shutil


print('usage:just this_module.py  , no args need')
pat_lig = re.compile('ligExp_(\w+)')
pat_grid = re.compile('glide-grid_(\w+)')
for lig in glob.glob('*.sdf'):
	sdf_base = lig.split('.')[0]
	mat_lig = re.findall(pat_lig,sdf_base)
	print('sdf_base, mat_lig = ', sdf_base, mat_lig)
	sdf_ID = mat_lig[0]
	if sdf_ID =='': print('something with lig: {}, will escape this lig'.format(sdf_ID));continue
	for grid in glob.glob('glide-grid_*'):
		mat_grid = re.findall(pat_grid, grid)
		if mat_grid[0] == sdf_ID:
			shutil.move(lig,'{}/{}'.format(grid,lig))
			print('done move with lig: {}'.format(lig))
			break
print('next cmd might be: _glide0c_redock_ligExp')
