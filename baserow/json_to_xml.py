import json
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape
from xml.sax.handler import ContentHandler
from xml.sax import make_parser

def add_value_to_element(element, value):
    if isinstance(value, list):
        for item in value:
            item_element = ET.SubElement(element, "item")
            add_value_to_element(item_element, item)
    elif isinstance(value, dict):
        for sub_key, sub_value in value.items():
            sub_element = ET.SubElement(element, sub_key.replace(" ", "_").replace("&", "and"))
            add_value_to_element(sub_element, sub_value)
    else:
        element.text = str(value)

def parsefile(file):
    parser = make_parser()
    parser.setContentHandler(ContentHandler())
    parser.parse(file)

files = [

    {"file": "Catalogues",
     "element": "Catalogue"},

    {"file": "Endpoints",
     "element": "Endpoint"},

    {"file": "Formats_and_Semantic_Resources",
     "element": "Resource"},

    {"file": "Providers",
     "element": "Provider"},

    {"file": "Resource_Types",
     "element": "Resource_Type"},

    {"file": "Sources",
     "element": "Source"},

]

for file in files:
    json_file = "out_json/" + file["file"] + ".json"
    xml_file = "out_xml/" + file["file"] + ".xml"
    print(f"Converting {json_file} to {xml_file}...")
    with open(json_file, "r") as f:
        data = json.load(f)
        # data is a dict where each key corresponds to the index of a row
        # each row is modeled as a dict where each key is a column of the row
        # values are either strings/numbers or other dicts (if they are linked entities)
    # Create XML root
    root = ET.Element("root")
    for id, columns in data.items():
        # .items() will return list of tuples, each with index and content of a row
        # we take only the content
        root_element = ET.SubElement(root, file["element"])
        for column, value in columns.items():
            # Create sub-element for each column header
            column_element = ET.SubElement(root_element, column.replace(" ", "_").replace("&", "and"))
            # Use function defined above to add value
            add_value_to_element(column_element, value)
    # Write to XML file
    tree = ET.ElementTree(root)
    ET.indent(tree, space="    ", level=0)
    tree.write(xml_file, encoding="utf-8", xml_declaration=True)
    # Check well-formedness of XML file
    try:
        parsefile(xml_file)
        print(f"✅ {xml_file} is well-formed")
    except Exception as e:
        print(f"🚨 {xml_file} is NOT well-formed! {e}")
    # Separator
    print("===")