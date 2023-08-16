import argparse
import pandas as pd
# import colorsys
from distinctipy import distinctipy
import re
import os
import sys

def rgb_to_hex(rgb):
    return "#{:02X}{:02X}{:02X}".format(int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))

def replace_with_colors(input_list):
    unique_elements = list(set(input_list))
    unique_elements.sort()
    unique_colors = distinctipy.get_colors(len(unique_elements))
    unique_colors = [rgb_to_hex(color) for color in unique_colors]

    element_color_mapping = dict(zip(unique_elements, unique_colors))

    colored_list = [element_color_mapping[element] for element in input_list]
    amount_unique = len(unique_elements)

    return colored_list, unique_elements, unique_colors, amount_unique


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate annotation files for iTOL from a CSV dataframe.")
    parser.add_argument("-i", "--input", required=True, help="Input CSV dataframe file")
    parser.add_argument("-o", "--output_dir", required=True, help="Output directory for annotation files")
    args = parser.parse_args()

    unsafe_chars = r'[\\/:*?"<>|]'

    dataframe_path = args.input
    dataframe = pd.read_csv(dataframe_path, index_col=0)

    ids = list(dataframe.index)

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    try:
        for column in dataframe.columns:
            column_values = list(dataframe[column])
            colored_list, unique_elements, unique_colors, amount_unique = replace_with_colors(column_values)
            output_file_path = os.path.join(args.output_dir, re.sub(unsafe_chars, "_", column) + ".txt")
            with open(output_file_path, "w") as annotation_file:
                annotation_file.write("DATASET_COLORSTRIP\n")
                annotation_file.write("SEPARATOR COMMA\n")
                annotation_file.write("COLOR,#FFFFFF\n")
                annotation_file.write("DATASET_LABEL," + column + "\n")
                annotation_file.write("LEGEND_TITLE," + column + "\n")
                annotation_file.write("LEGEND_SHAPES," + ("2," * amount_unique).rstrip(",") + "\n")
                annotation_file.write("LEGEND_COLORS," + ",".join(unique_colors) + "\n")
                annotation_file.write("LEGEND_LABELS," + ",".join(map(str, unique_elements)) + "\n")
                annotation_file.write("DATA\n")
                annotation_file.write("\n".join([f"{item1},{item2}" for item1, item2 in zip(ids, colored_list)]))

        print(f"\033[92m Fineshed: Generated annotation files in '{args.output_dir}'", "green")

    except Exception as e:
        print(f"\033[91m An error occurred: {e}")
