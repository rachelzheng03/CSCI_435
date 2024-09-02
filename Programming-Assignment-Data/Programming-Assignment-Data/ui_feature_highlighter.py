import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw 
import re
import argparse  
 
"""
Desc: depth first search for leaf nodes using recursion
Input: 
    root: the root of the xml file
    leaf_nodes: a list that will hold all the leaf nodes as they are found
Output: a list of all the leaf nodes in the xml file
"""
def __find_leaf_nodes(root, leaf_nodes: list):
    # get the children of the node "root"
    children = list(root)

    # if the node "root" has no children, then it is a leaf node
    if len(children) == 0:
        leaf_nodes.append(root)
    
    else:
        for child in children:
            __find_leaf_nodes(child, leaf_nodes)
    
    return leaf_nodes


"""
Desc: draw a yellow rectangle around the specified leaf level component
Input: 
    img: the img of the app to draw on
    node: the node corresponding to the feature that needs to be outlined
Output: None
"""
def __highlight_leaf_lvl_components(img, node):
    bounds=__get_and_reformat_bounds(node) 
    ImageDraw.Draw(img).rectangle(bounds, outline ="yellow", width=6)


"""
Desc: get and reformat the bounds(dimensions) of a node in an xml file
Input: 
    node: the node of which to get the bounds for
Output: the bounds of node formatted as [(x1, y1), (x2, y2)]
"""
def __get_and_reformat_bounds(node):
    # get the bounds attribute of "node"
    if "bounds" in node.attrib.keys():
        bounds = node.get('bounds')
    else:
        print("node has no attribute \"bounds\"")
        return

    # reformat bounds so that it can be used as an argument in the method ImageDraw.Draw().rectangle; 
    # for example, from [0,96][1440,320] to [(0,96), (1440,320)]
    pattern = re.compile('\[([0-9]+),([0-9]+)\]\[([0-9]+),([0-9]+)\]')
    m = pattern.match(bounds)
    coordinates = m.groups()
    return [(int(coordinates[0]), int(coordinates[1])), (int(coordinates[2]), int(coordinates[3]))]

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("xml", help = "the name or path of the xml file that needs to be parsed", type = str)
    parser.add_argument("png", help = "the name or path of the png file that corresponds with the xml file", type=str)
    parser.add_argument("--save", help = "saves the output picture", action="store_true")
    args=parser.parse_args()
    xml=args.xml
    png=args.png

    # make sure command line filenames end in the right extension
    try:
        assert(xml[-4:] == ".xml")
    except AssertionError as e:
        print("The extension of the provided xml file is incorrect\n")
        exit()
    try:
        assert(png[-4:] == ".png")
    except AssertionError as e:
        print("The extension of the provided png file is incorrect\n")
        exit()

    # parse the xml file
    try:
        tree = ET.parse(xml)
    except ET.ParseError as e:
        # if there is an error while parsing the xml, let the user know
        print("xml.etree.ElementTree.ParseError:", e)
        exit()

    root = tree.getroot()
    leaf_nodes=__find_leaf_nodes(root, [])
    #print(len(leaf_nodes))
    img = Image.open(png)
    for node in leaf_nodes:
        __highlight_leaf_lvl_components(img, node)

    if args.save:
        img.save(png[:len(png)-4]+".output.png")
    else:
        img.show()
