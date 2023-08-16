#Author:  Mustafa Helal
#!/usr/bin/python
import os
import pandas as pd
import glob
import time
import numpy as np
import multiprocessing
from multiprocessing import Pool
import sys
import argparse


#assembly function
def assembleGenomes(threads, read_files):
	if os.path.exists("Assembly/"):
		os.system("rm -rf Assembly/*")

	reads = glob.glob(read_files + "/*R1_001.fastq.gz")

	for read1 in reads:
		read2 = read1.split("R1_001.fastq.gz")[0] + "R2_001.fastq.gz"
		name = read1.split("_S")[0].split("_")[-1]
		os.system("spades.py" + " -o Assembly/" + name + "/" + " -1 " + read1 + " -2 " + read2 + " -t " + threads)
		os.system("mv Assembly/" + name + "/scaffolds.fasta Assembly/" + name + ".fasta")
		os.system("rm -r Assembly/" + name + "/")

#create cgMLST schema_seed
def createMLST(threads, input, threshold):

	if os.path.exists("MLST/"):
		os.system("rm -rf MLST")

	os.system("chewBBACA.py CreateSchema -i " + input + " --cpu " + threads + " -o MLST")
	os.system("cd MLST/ && chewBBACA.py AlleleCall -i " + input + " -g schema_seed/ -o results_cg --cpu " + threads)
	os.system("cd MLST/ && chewBBACA.py RemoveGenes -i results_cg/results_alleles.tsv -g results_cg/paralogous_counts.tsv -o alleleCallMatrix_cg.tsv") #noch mit dauiu
	# Extract cgMLST
	os.system("cd MLST/ && chewBBACA.py ExtractCgMLST -i alleleCallMatrix_cg.tsv -o cgMLST_ref --t " + str(threshold) + "") #noch mit dazu
	file = "MLST/cgMLST_ref/cgMLST" + str(int(threshold * 100)) + ".tsv"
	os.system("sed -i 's/.fasta//g'" + file)  #noch mit dazu

#generate multifasta files
def generate_multifasta(prot_files, df, schema_seed, dir_name_1):
	read_files = df.index.tolist()
	file_header = df.columns.tolist()
	for i in range(len(read_files)):
		fasta_name = read_files[i] + ".fasta"
		with open(schema_seed+fasta_name, "r") as ID_file, open(dir_name_1 + "/"+fasta_name,"w+") as multifasta:
			Lines = ID_file.readlines()
			for header in file_header:
				index = df.at[read_files[i], header]
				line_num = 0
				index_count = 0
				for line in Lines:
					if line.startswith(">"):
						index_2 = line.rsplit("_")[-1]
						index_2 = index_2.split("\n")[0]
						if str(index_2) == str(index):
							multifasta.write(Lines[line_num].strip("\n") + ":ID-" + header + "\n")
							multifasta.write(Lines[line_num+1])
							break
						if index == 0:
							multifasta.write(Lines[line_num].strip("\n") + ":ID-" + header + "\n")
							multifasta.write("X"+ "\n")
							break
					line_num += 1

#alignment function for parallelization
def align(list):
	thread = list[0]
	prot = list[1]
	name = list[2]
	dir_name_2 = "gene_alignment_results"
	abs_path = os.path.abspath(os.getcwd()) + "/" + dir_name_2

	for i in range(len(prot)):
		os.system("muscle -quiet -in " + prot[i] + " -out " + abs_path + "/" + name[i] + ".afa")


def main():

	parser = argparse.ArgumentParser(description="Build a core genome phylogeny using assembly or paird-end read files.")
	parser.add_argument("-i", "--input", required=True, help="Input path to files directory.")
	parser.add_argument("-t", "--threads", default=4, required=False, help="Amount of threads to use. Default is 4.")
	parser.add_argument("-o", "--output_dir", required=True, help="Output path for the generated files.")
	parser.add_argument("-m", "--model", required=False, default="GTR+G", help="Substitution Model für RaxML-ng. Default is GTR+G")
	parser.add_argument("-th", "--threshold", required=False, default=0.95, help="Clustering Threshold for ChewBBACA. Default is 0.95")
	args = parser.parse_args()

	#define input
	read_files = args.input #input files / reads in .fastq or genoms in .fasta format
	threads = args.threads #amount of threads

	#ask for input format
	if read_files[0].endswith(".fastq"):
		assembleGenomes(threads, read_files)
		createMLST(threads, "Assembly/", args.threshold)
	else:
		createMLST(threads, read_files, args.threshold)

	schema_seed = "MLST/schema_seed/" 	#path to gene allele_type files
	table = "MLST/cgMLST_ref/cgMLST" + str(int(args.threshold * 100)) + ".tsv" #path to mlst_table.tsv

	#import prot_files
	prot_files = [f for f in glob.glob(schema_seed + "*.fasta")]
	df = pd.read_csv(table, sep = "\t")
	df.set_index('FILE', inplace=True)

	#created dir for multifasta results
	dir_name_1 = "multifasta_alignments_results"
	if os.path.exists(dir_name_1):
		os.system("rm -rf " + dir_name_1)
		os.system("mkdir " + dir_name_1)
		print("Directory " , dir_name_1 ,  " Created ")
	else:
		os.system("mkdir " + dir_name_1)
		print("Directory " , dir_name_1 ,  " Created ")


	generate_multifasta(prot_files, df.T, schema_seed, dir_name_1)

	# second file import for alignments
	multi_fasta_files = [f for f in glob.glob(dir_name_1 +"/"+"*.fasta")]
	result_names = [name.split(".")[0] for name in os.listdir(schema_seed) if name.endswith(".fasta")]


	#create dir for alignment results
	dir_name_2 = "gene_alignment_results"
	if os.path.exists(dir_name_2):
		os.system("rm -rf " + dir_name_2)
		os.system("mkdir " + dir_name_2)
		print("Directory " , dir_name_2 ,  " Created ")
	else:
		os.system("mkdir " + dir_name_2)
		print("Directory " , dir_name_2 ,  " Created ")

	abs_path = os.path.abspath(os.getcwd()) + "/" + dir_name_2
	cpu_threads = multiprocessing.cpu_count()


	# set amount of thread and parallele functions here

	amount_threads = int(threads)
	if cpu_threads >= amount_threads:
		print("using " + str(amount_threads) + " threads:")
		#split files for parallel usage
		prot_list = np.array_split(multi_fasta_files, amount_threads)
		name_list = [elem.split("/")[1] for elem in multi_fasta_files]
		name_list = [elem.split(".")[0] for elem in name_list]
		name_list = np.array_split(name_list, amount_threads)
	else:
		amount_threads = cpu_threads-3 # -3 to not occupy all the cores in the system
		print("passed more threads than available -- running with " + str(amount_threads) + " Threads")
		#split files for parallel usage
		prot_list = np.array_split(multi_fasta_files, amount_threads)
		name_list = [elem.split("/")[1] for elem in multi_fasta_files]
		name_list = [elem.split(".")[0] for elem in name_list]
		name_list = np.array_split(name_list, amount_threads)

	#Parallel function
	if cpu_threads >= amount_threads:
		pool = Pool(amount_threads)
		params = [[i+1, prot_list[i].tolist(), name_list[i].tolist() ] for i in range(amount_threads)]
		results = pool.map(align, params)

	else:
		pool = Pool(cpu_threads-3)
		params = [[i+1, prot_list[i].tolist(), name_list[i].tolist() ] for i in range(cpu_threads-3)]
		results = pool.map(align, params)

	#create dir for concat results
	dir_name_3 = "concat_alignment_tree_results"
	if os.path.exists(dir_name_3):
		os.system("rm -rf " + dir_name_3)
		os.system("mkdir " + dir_name_3)
		print("Directory " , dir_name_3 ,  " Created ")
	else:
		os.system("mkdir " + dir_name_3)
		print("Directory " , dir_name_3 ,  " Created ")

	abs_path_2 = os.path.abspath(os.getcwd()) + "/" + dir_name_3

	alignment_files = os.listdir(abs_path)
	id_names = df.index.tolist()
	prot_names = df.columns.tolist()


	#concat all files
	with open(abs_path_2+"/concat_file.afa", "w") as write_file:
		for id in id_names:
			ID = "ID-" + id
			write_file.write(">"+id+"\n")
			print(ID)
			for file in prot_names:
				with open(abs_path + "/" + file + ".afa", "r") as read_file:
					lines = read_file.readlines()
					num_lines_between = 0
					j = 1
					while lines[j][0] != ">":
						num_lines_between += 1
						j += 1
					for i in range(len(lines)):
						ID_FILE = lines[i].split(":")[-1]
						ID_FILE = ID_FILE.replace("\n", "")
						if ID_FILE == ID:
							END = 1
							while END != num_lines_between+1:
								write_line = lines[i+1].replace("X", "-")
								write_file.write(write_line)
								END += 1
								i += 1
						else:
							continue

	# generate phylogenetic tree
	os.system("raxml-ng --all --force perf_threads --msa " + dir_name_3 +"/concat_file.afa  --model " + args.model + " --threads " + str(amount_threads))

	#moving files
	print("Moving results...")

	if os.path.exists("final_results"):
		os.system("rm -rf final_results")

	os.system("mkdir final_results")
	os.system("mv -t final_results concat_alignment_tree_results gene_alignment_results multifasta_alignments_results MLST")

	if os.path.exists(args.output_dir + "final_results"):
		os.system("rm -rf " + args.output_dir + "final_results")
	os.system("mv -t " + args.output_dir + " final_results")

	print(f"\033[92m Analysis has finished! Results are in " + args.output_dir + ".")


if __name__ == "__main__":
	try:
		main()
	except Exception as e:
        print("\033[91m An error occurred: " + str(e))
