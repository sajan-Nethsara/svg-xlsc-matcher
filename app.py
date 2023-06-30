# importing libs
from bs4 import BeautifulSoup
import pandas as pd

# global variables
excel_path = 'input.xlsx'
svg_path = 'input.svg'


# basic functions

def convert_string(string):
    # Convert string to lowercase
    converted_string = str(string)
    lower_string = converted_string.lower()

    # Remove spaces from the string
    no_space_string = lower_string.replace(" ", "")

    return no_space_string


def get_excel_array(sheet, n):
    row_array = sheet.iloc[:, n].values
    return row_array


def convert_string_array(arr):
    converted = list(map(convert_string, arr))
    return converted

# making element names
def get_label_id(input_string):
    split_string = input_string.split("-")
    split_string[-1] = "label"
    modified_string = "-".join(split_string)
    return modified_string

def get_group_id(input_string):
    split_string = input_string.split("-")
    split_string[-1] = "group"
    modified_string = "-".join(split_string)
    return modified_string

def get_section_id(input_string):
    split_string = input_string.split("-")
    split_string[-1] = "section"
    modified_string = "-".join(split_string)
    return modified_string


# to main functions

def find_inner_text(text_element):
    inner_text = ""
    for child in text_element.children:
        if child.name == "tspan":
            inner_text += child.get_text()
        else:
            inner_text += child.get_text()
    return inner_text       

def get_map_text_converted_array(sheet):
    map_text = get_excel_array(sheet, 0)
    converted = convert_string_array(map_text)
    return converted


def get_map_id_array(sheet):
    map_id = get_excel_array(sheet, 2)
    return map_id


# main functions

def manipulate_svg(map_text_list, map_id_list):
    # return soup
    with open(svg_path, "r") as f:
        soup = BeautifulSoup(f, "xml")
    section = soup.find(id="sections")
    all_group_elements = section.find_all("g" , recursive=False)
    for element in all_group_elements:
        text_element = element.find("text")
        inner_text = find_inner_text(text_element)
        inner_text_modified = convert_string(inner_text)
        search_index = map_text_list.index(inner_text_modified)
        map_id = map_id_list[search_index]
        group_name = get_group_id(map_id)
        section_name = get_section_id(map_id)
        label_name = get_label_id(map_id)

        #renaming process 
        element["id"] = group_name
        text_element["id"] = label_name
        print(f"this line arived {inner_text_modified}")

        # for child in element.children:
        #     if child.name == "text":
        #         child["id"] = label_name
        #     else:
        #         child["id"] = section_name    

        next_sibling = text_element.find_next_sibling()
        previous_sibling = text_element.find_previous_sibling()
        # renaming
        if next_sibling:
          next_sibling["id"] = section_name
        elif previous_sibling:
          previous_sibling["id"] = section_name
        else:
          print("sibling not found")

        print(f"rename success {section_name}")
    return soup

# the ultimate Main
def main():
    print("Hello App")
    sheet = pd.read_excel(excel_path)
    map_text_list = get_map_text_converted_array(sheet)
    map_id_list = get_map_id_array(sheet)
    print(map_text_list)
    print(map_id_list)
    new_soup = manipulate_svg(map_text_list,map_id_list)
    modified_svg_content = str(new_soup)
    with open("output.svg", "w") as output_file:
      output_file.write(modified_svg_content)
      print("SVG file Created successfully")
    print("<---->") 

main()