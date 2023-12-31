# TeamToolsHub

Welcome to TeamToolsHub! This Git repository is a collection of useful and simple (!) command-line scripts and tools created by our team to streamline our workflow and enhance our productivity. Here, we share simple yet effective tools that can be easily used by everyone on the team. The repository will be regularly updated with new tools and improvements to existing ones. Feel free to contribute your own scripts and tools to make our development process even smoother.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Available Tools](#available-tools)
- [Contributing](#contributing)

## Installation

To start using the tools from this repository, follow these simple installation steps:

1. Clone the repository to your local machine:

    ```sh
    git clone https://github.com/YourUsername/TeamToolsHub.git
    ```

2. Navigate to the cloned directory:

    ```sh
    cd TeamToolsHub
    ```

3. Run the desired tool using the command line, as outlined in the [Usage](#usage) section.

## Usage

Each tool comes with a brief description of what it does, parameter settings, dependencies and an example of how to use it. Keep the discription as simple as possible. To use a tool, open a terminal window and navigate to the directory where the tool is located. Then, run the tool with the appropriate command, as shown.

## Available Tools

Here's a list of the tools currently available in this repository:

## 1. itol_file_generator
  - Description: Creates based on the columns of a CSV file color-coded IToL usable annotation files. For each column one annotation file is created.
  - Parameters:
    - `-i`: path to input csv.
    - `-o`: path to output directory.
  - Dependencies:
    - `pandas`
    - `distinctipy`
    - `CSV-Format`:

| IDs | annotation column 1 |annotation column 2 |
|----------|----------|----------|
| Sample_1 | Cat | Positive |
| Sample_2 | Dog | Negative |

  - Example:
    ```sh
      python itol_file_generator.py -i input.csv -o output_dir
    ```



## 2. Core Genome Phylogeny
- Description: Creates a core genome phylogeny from a set of genomes or paired-end sequence files.
- Parameters:
  - `i`: `input`: Path to the directory containing input files (reads in `.fastq` or genomes in `.fasta` format).
  - `t`: `threads`: Number of threads to use for parallel processing. Default is 4.
  - `o`: `output_dir`: Output path for generated files and results.
  - `m`: `model`: Substitution model for RaxML-ng. Default is GTR+G.
  - `th`: `threshold`: Clustering threshold for ChewBBACA. Default is 0.95.
- Dependencies:
  - `CGP_environment` : Create and activate the CGP environment.
  (for manual installation)
  - SPAdes
  - chewBBACA
  - MUSCLE
  - RaxML-ng
- Example:
  ```sh
  python CPG.py -i INPUT_DIR/ -o OUTPUT_DIR/ [-m MODEL] [-th THRESHOLD] [-t THREADS]
  ```

## Contributing

Everybody is encouraged to contribute their own scripts and tools to this repository. To contribute, follow these steps:

1. Fork the repository.
2. Create a new branch for your contribution:

    ```sh
    git checkout -b feature/new-tool
    ```

3. Add your script/tool to the repository, following the structure and guidelines of existing tools.

4. Commit your changes and push to your forked repository:

    ```sh
    git commit -m "Add: New tool - Description"
    git push origin feature/new-tool
    ```

5. Create a pull request from your forked repository to the main repository.
6. Update the README accordingly to keep everything up-to-date!
