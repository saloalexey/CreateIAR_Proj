import os
import sys
from lxml import etree
from os import listdir
from os.path import isfile, join



def AppendState(parent, name):
    group_record = etree.Element("state")
    parent.append(group_record)
    group_record.text = name
    return group_record

def AppendNode(type, parent, name):
    group_record = etree.Element(type)
    parent.append(group_record)
    group_name_record = etree.Element("name")
    group_name_record.text = name
    group_record.append(group_name_record)
    return group_record

def AppendGroup(parent, name):
    return AppendNode("group", parent, name)

def AppendFile(parent, name):
    return AppendNode("file", parent, name)



def ParseDir(dir_name, elements):
    for item in listdir(dir_name):
        if isfile(join(dir_name, item)):
            if any(item.endswith(x) for x in add_files):
                path = join(dir_name,  item).replace("./", "$PROJ_DIR$\\").replace(".\\", "$PROJ_DIR$\\")
                AppendFile(elements, path)
                print("New file " + item)
        else:
            if join(dir_name, item) in ignoreList:
                continue

            new_group = AppendGroup(elements, item)

            print ("New dir: " + join(dir_name, item))
            ParseDir(join(dir_name, item), new_group)
            print ("Grp end: " + item)

    return elements


def AddIncludePath(dir_name, elements):
    for item in listdir(dir_name):
        if isfile(join(dir_name, item)):
            continue
        else:
            if join(dir_name, item) in ignoreList:
                continue

            path = join(dir_name,  item).replace("./", "$PROJ_DIR$\\").replace(".\\", "$PROJ_DIR$\\")
            new_group = AppendState( elements, path)
            Parse_only_Dir(join(dir_name, item), elements)

    return elements

def findIncludePath(tag, elem, name):
    global idx
    global elem_include
    for e in elem:
        if(e.tag == tag):
            if(e.tag == "name"):
                if(e.text == name):
                    if idx == 5:
                        elem_include = elem
                        return
                    
                    idx += 1
                    find(tag_for_include[idx], elem, name_for_include[idx])
                else:
                    idx -= 1
                    return
                            
            else:
                if idx == 5:
                    return
                
                idx += 1
                find(tag_for_include[idx],e,name_for_include[idx])


ignoreList = [".\\settings", ".\\Debug"]
ewp_file = "Proj.ewp"
add_files = ['.c', '.h', '.cpp', 's', 'icf']
rootdir = "."


elements = ParseDir(rootdir, etree.Element("project"))

tree = etree.parse(ewp_file)
root = tree.getroot()


idx = 0
elem_include = 0
tag_for_include = ["configuration", "settings", "name", "data", "option", "name"]
name_for_include = ["", "", "ICCARM", "", "", "CCIncludePath2" ]
findIncludePath(tag_for_include[idx],root,name_for_include[idx])
elem_tmp = AddIncludePath(rootdir, elem_include)


    

for bad in root.xpath("//project/group|//project/file"):
  bad.getparent().remove(bad)

prj = root.xpath("//project")[0]

for subnode in elements:
    prj.append(subnode)

text_file = open(ewp_file, "wb")
text_file.write((etree.tostring(tree, pretty_print=True)))
text_file.close()
