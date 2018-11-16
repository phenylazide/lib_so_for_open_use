# coding:utf-8

import os,sys,glob,re
import pybel
from multiprocessing import Pool
from glide2a_post_process_lib_so import *
def main():
	try:
		args = sys.argv[1:]
	except:
		print('no args was got, will using default batch method')
	os.chdir(base)
	if len(args) == 0:	
		glide_dock_post_process_batch()
		desired_properties = default_desired_properties
		schdg_glide_dock_sdf_to_csv_all(desired_properties)
		return
	if len(args) > 0:
		x_file = args[0]
		desired_properties = default_desired_properties
		glide_dock_single_maegz2sdf_2csv(x_file,desired_properties)
		return
	
if __name__ == "__main__":
	main()


