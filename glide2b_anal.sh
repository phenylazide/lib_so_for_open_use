source activate deepchem
for f in glide*.csv; do 
	f_base=`basename $f .csv` 
	(python /home/admin/lib_so_for_open_use/vina_pre_process_data_0_2_run_so.py $f
	python /home/admin/lib_so_for_open_use/score_anal_plt_0_4_run_so.py -f ${f_base}.txt) & 
	##  apply ( cmd1; cmd2) &  
done
wait


