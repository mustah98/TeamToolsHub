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

Each tool comes with a brief description of what it does, parameter settings, dependencies and an example of how to use it. Keep the discription as simple as possible. To use a tool, open a terminal window and navigate to the directory where the tool is located. Then, run the tool with the appropriate command, as shown in the example.

**data_renamer**
  - Description: A brief description of what the tool does.
  - Parameters:
      - `parameter1`: Description of parameter 1.
      - `parameter2`: Description of parameter 2.
  - Dependencies:
      - `Package 1`
      - `Package 2`
  - Example:
      ```sh
      ./data_renamer.sh --parameter1 value1 --parameter2 value2
      ```

## Available Tools

Here's a list of the tools currently available in this repository:

**itol_file_generator**
  - Description: Creates based on the columns of a CSV file color-coded IToL usable annotation files. For each column one annotation file is created.
  - Parameters:
    - `-i`: path to input csv.
    - `-o`: path to output directory.
  - Dependencies:
    - `pandas`
    - `distinctipy`
    - `CSV-Format`:
<center>
| IDs | annotation column 1 |annotation column 2 |
|----------|----------|----------|
| Sample_1 | Cat | Positive |
| Sample_2 | Dog | Negative |
</center>
  - Example:
    ```sh
      python itol_file_generator.py -i input.csv -o output_dir
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
