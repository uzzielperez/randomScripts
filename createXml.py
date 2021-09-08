import xml.etree.ElementTree as xml

def indent(elem, level=0):
        from xml.etree import ElementTree as xml
'''
copy and paste from http://effbot.org/zone/element-lib.htm#prettyprint
it basically walks your tree and adds spaces and newlines so the tree is
printed in a nice way
'''
def indent(elem, level=0):
  i = "\n" + level*"  "
  if len(elem):
    if not elem.text or not elem.text.strip():
      elem.text = i + "  "
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
    for elem in elem:
      indent(elem, level+1)
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
  else:
    if level and (not elem.tail or not elem.tail.strip()):
      elem.tail = i

# https://github.com/python/cpython/commit/63673916464bace8e2147357395fdf3497967ecb
def sort_attributes(root):
    for el in root.iter():
        attrib = el.attrib
        if len(attrib) > 1:
            attribs = sorted(attrib.items())
            attrib.clear()
            attrib.update(attribs)

def buildPerHBtree(CFGBrickset, RBX="HB0"):
  CFGBrick = xml.SubElement(CFGBrickset, "CFGBrick")

  Parameter = xml.SubElement(CFGBrick, "Parameter", type="string", name="INFOTYPE")
  Parameter.text = "HBTDCLUT"

  Parameter2 = xml.SubElement(CFGBrick, "Parameter", type="string", name="CREATIONSTAMP")
  Parameter2.text = "2020-9-7"

  Parameter3 = xml.SubElement(CFGBrick, "Parameter", type="string", name="CREATIONTAG")
  Parameter3.text = "HBTestTag"

  Parameter4 = xml.SubElement(CFGBrick, "Parameter", type="string", name="RBX")
  Parameter4.text = RBX

  rm = []
  rm.extend(range(1,6))

  for irm in rm:
        qie = []
        maxR = 65
        if irm == 5:
                maxR = 17
        qie.extend(range(1,maxR))
        #print irm, qie
        for i in qie:
                if irm == 1 or irm ==2:
                        Data = xml.SubElement(CFGBrick, "Data", qie="%s"%(str(i)), rm="%s"%(str(irm)), elements="1", encoding="hex")
                        Data.text = "0xd 0xd 0xd 0xd"
                        if i == 1:
                                Data.text = "0xe 0xe 0xe 0xe"
                        elif i == 2:
                                Data.text = "0xc 0xc 0xc 0xc"
                else:
                        Data = xml.SubElement(CFGBrick, "Data", qie="%s"%(str(i)), rm="%s"%(str(irm)), elements="1", encoding="hex")
                        Data.text = "0xf 0xc 0xd 0xe"



  sort_attributes(CFGBrick)



'''
function to build an example tree containing cars and ships
CFGBrickset is the root node
'''

def buildTree(site="904"):

  CFGBrickset = xml.Element("CFGBrickset")

  if site=="904":
        RBXList = ["HB0", "HB1", "HB2", "HB3", "HB4", "HB5"]
  elif site=="P5":
        i = 1
        RBXList = []
        while i < 19:
                if i < 10:
                        RBXList.append("HBP0%d" %i)
                        RBXList.append("HBM0%d" %i)
                else:
                        RBXList.append("HBP%d" %i)
                        RBXList.append("HBM%d" %i)
                print "Appending HBP/HBM", i
                i = i+1
  for rbx in RBXList:
        buildPerHBtree(CFGBrickset, rbx)

  indent(CFGBrickset)

  tree = xml.ElementTree(CFGBrickset)

  tree.write("HBTDCLUTtest%s.xml" %site, xml_declaration=True, encoding='utf-8', method="xml")

'''
main function, so this program can be called by python program.py
'''
if __name__ == "__main__":
  #buildTree()
  buildTree("P5")
