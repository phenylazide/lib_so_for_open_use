source activate deepchem
for f in glide*.csv; do 
	f_base=`basename $f .csv` 
	(python /home/phzd/g09E/script/vina_pre_process_data_0_2.py $f
	python /home/phzd/g09E/script/score_anal_plt_0_3.py -f ${f_base}.txt) & 
	##  apply ( cmd1; cmd2) &  
done
wait


