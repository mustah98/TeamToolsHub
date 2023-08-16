# Core Genome Phylogeny (CGP) Tool

## Introduction

The Core Genome Phylogeny (CGP) Tool is a Python script designed to build a core genome phylogeny using either assembly or paired-end read files. This tool utilizes various bioinformatics tools and processes, including genome assembly (using SPAdes), multi-locus sequence typing (using chewBBACA), gene alignment (using MUSCLE), and phylogenetic tree generation (using RaxML-ng). It aims to provide researchers with a streamlined workflow to analyze genomic data and infer evolutionary relationships among microbial isolates based on their core genome.

## Creating Conda Environment

1. Create the conda environment using the provided `CGP_environment.yml` file:

```bash
conda env create -n CGP -f CGP_environment.yml
```

2. Activate the conda environment:

```bash
conda activate CGP
```

## Usage

Run the CGP tool using the following command:

```bash
python CPG.py -i INPUT_DIR/ -o OUTPUT_DIR/ [-m MODEL] [-th THRESHOLD] [-t THREADS]
```

### Flags

- `i`, `input`: Path to the directory containing input files (reads in `.fastq` or genomes in `.fasta` format).
- `t`, `threads`: Number of threads to use for parallel processing. Default is 4.
- `o`, `output_dir`: Output path for generated files and results.
- `m`, `model`: Substitution model for RaxML-ng. Default is GTR+G.
- `th`, `threshold`: Clustering threshold for ChewBBACA. Default is 0.95.

## Workflow Steps

1. **Assembly** (`-i` flag with `.fastq` files):
   - If Assemblys are used as input, this step will be skipped.
   - Genome assembly is performed using SPAdes.
   - Paired-end reads (`R1` and `R2`) are assembled to scaffolds.
   - Assembled scaffolds are moved to the `Assembly` directory.

2. **MLST Schema Creation** (`-i` flag with `.fasta` files or after assembly):
   - A core genome MLST schema is created using `chewBBACA`.
   - Potentially paralogous genes are removed from allele calls.
   - The cgMLST table is generated and stored in the `MLST` directory.

3. **MultiFasta Generation**:
   - Multifasta files for gene alignment are generated based on the cgMLST schema.
   - These multifasta files are saved in the `multifasta_alignments_results` directory.

4. **Gene Alignment**:
   - Genes in multifasta format are aligned using MUSCLE.
   - Aligned gene sequences are saved in the `gene_alignment_results` directory.

5. **Concatenation and Phylogenetic Tree Generation**:
   - Aligned gene sequences are concatenated into a single alignment file.
   - A phylogenetic tree is generated using RaxML-ng.
   - The resulting tree is saved in the `concat_alignment_tree_results` directory.

6. **Results Output**:
   - All results and intermediate files are organized into the `final_results` directory.
   - The directory structure includes `concat_alignment_tree_results`, `gene_alignment_results`, `multifasta_alignments_results`, and `MLST`.

## Example

To run CGP with the required flags, use the following command:

```bash
python CGP.py -i input_files/ -t 8 -o output_results/ -m GTR+G -th 0.90
```

## Dependencies

The CGP Tool requires the following software/tools to be installed or accessible in your environment:

- SPAdes
- chewBBACA.py
- MUSCLE
- RaxML-ng

## Disclaimer

This tool is provided as-is without any warranty. Users are responsible for ensuring the compatibility of the tool with their environment and data.
