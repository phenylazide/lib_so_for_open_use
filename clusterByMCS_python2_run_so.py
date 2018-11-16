#coding:utf-8
from __future__ import print_function
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdFMCS
import functools
import os,sys,time
from clusterByMCS_python2_lib_so import *
def main():
	start_time = time.time()
	cutoff = 0.618
	try:
		molformat = sys.argv[1].split('.')[1]
		molIn = sys.argv[1]
		if len(sys.argv) > 2:
			cutoff = float(sys.argv[2])
	except:
		print('Usage: python ClusterByMCS.py format[smi|sdf|mol2] FileIn cutoff(optional)')
		sys.exit(0)

	output = open('clusters.smi', 'w')
	output2 = open('clusters.csv', 'w')
	output2.write('file,smiles_rdkit,!Cluster\n')
	mols = []
	if molformat == 'sdf':
		xmols = Chem.SDMolSupplier(molIn)
		for mol in xmols:
			if mol is None:
				continue
			mols.append(mol)

	elif molformat == 'smi':
		mols = ReadSmiles(molIn)
	elif molformat == 'mol2':
		mols = ReadMol2(molIn)
	else:
		print()
		print('************************Error messages************************')
		print('Unsupported file format:', molformat)
		print('Supported formats are: sdf | smi | mol2')
		print()
	clusters = ClusterByMCS(mols, cutoff)
	f = open('clusters_report', 'w')
	f.write('\nClustering by Maximum Common Substructure (MCS) with a cutoff value of %0.3f\n' % cutoff)
	f.write('--------------------------------------------------------------------------------------\n')
	singleton = 0
	for i in range(len(clusters)):
		if len(clusters[i]) > 1:
			f.write(Chem.MolToSmiles(Chem.MolFromSmarts(rdFMCS.FindMCS(clusters[i]).smartsString)) +' in ' + str(len(clusters[i])) + ' molecules\n')
		else:
			singleton += 1
		for mol in clusters[i]:
			output.write('{} {} !Cluster: {}\n'.format(Chem.MolToSmiles(mol, isomericSmiles=True), mol.GetProp('_Name'), str(i + 1)))
			output2.write('{},{},{}\n'.format(mol.GetProp('_Name'),Chem.MolToSmiles(mol,isomericSmiles=True),  str(i + 1)))
			
	output.close();output2.close()
	f.write('\n~~~~~~~~~Summary~~~~~~~~~\n')
	f.write('Total molecules: {}\n'.format(str(len(mols))))
	f.write('Clusters: {} with {} being singleton\n'.format(str(len(clusters)), str(singleton)))
	f.write('\n')
	f.write('--------------------------------------------------------------------------------------\n')
	f.close()
	end_time = time.time()
	total_time = end_time - start_time
	print("All done master, used {} times".format(total_time))

if __name__ == '__main__':
	main()

