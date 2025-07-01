import json
import xml.etree.ElementTree as ET

def add_value_to_element(element, value):
    if isinstance(value, list):
        for item in value:
            item_element = ET.SubElement(element, "item")
            add_value_to_element(item_element, item)
    elif isinstance(value, dict):
        for sub_key, sub_value in value.items():
            sub_element = ET.SubElement(element, sub_key.replace(" ", "_"))
            add_value_to_element(sub_element, sub_value)
    else:
        element.text = str(value)

files = [

    {"file": "baserow/out/Catalogues",
     "root": "Catalogues",
     "element": "Catalogue"},

    {"file": "baserow/out/Endpoints",
     "root": "Endpoints",
     "element": "Endpoint"},

    {"file": "baserow/out/Formats_and_Semantic_Resources",
     "root": "Formats_and_Semantic_Resources",
     "element": "Resource"},

    {"file": "baserow/out/Providers",
     "root": "Providers",
     "element": "Provider"},

    {"file": "baserow/out/Resource_Types",
     "root": "Resource_Types",
     "element": "Resource_Type"},

    {"file": "baserow/out/Sources",
     "root": "Sources",
     "element": "Source"},

]

for file in files:
    json_file = file["file"] + ".json"
    xml_file = file["file"] + ".xml"
    with open(json_file, "r") as f:
        data = json.load(f)  # data is a list of dicts
    # Create XML root
    root = ET.Element(file["root"])
    for id, columns in data.items():
        root_element = ET.SubElement(root, file["element"])
        for column, value in columns.items():
            # Create sub-element for each column
            column_element = ET.SubElement(root_element, column.replace(" ", "_"))
            add_value_to_element(column_element, value)
    # Write to XML file
    tree = ET.ElementTree(root)
    tree.write(xml_file, encoding="utf-8", xml_declaration=True)
