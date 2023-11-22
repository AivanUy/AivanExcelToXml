import os.path
import xml.etree.ElementTree as ET

originalEnTree = ET.parse("original-en/strings.xml")
originalEnRoot = originalEnTree.getroot()

excelEnTree = ET.parse("excel-en/strings.xml")
excelEnRoot = excelEnTree.getroot()

originalCNTree = ET.parse("original/strings.xml")
originalCNRoot = originalCNTree.getroot()

excelCNTree = ET.parse("excel/strings.xml")
excelCNRoot = excelCNTree.getroot()


def isInExcel(e: ET.Element, root: ET.Element) -> bool:
    for child in root:
        nameE = e.get("name")
        nameChild = child.get("name")
        if nameE == nameChild:
            return True


# 找出  新的
def findNew(originalE, excelE, dir_new):
    newRoot = ET.Element("resources")
    newTree = ET.ElementTree(newRoot)
    for excelChild in excelE:
        if not isInExcel(excelChild, originalE):
            newRoot.append(excelChild)
    isExists = os.path.exists(dir_new)
    if not isExists:
        os.makedirs(dir_new)

    newTree.write(f"{dir_new}/strings.xml", encoding='utf-8', xml_declaration=True, short_empty_elements=True)


if __name__ == '__main__':
    # 按中文为参照物
    findNew(originalCNRoot, excelEnRoot, "content-en-new")
    findNew(originalCNRoot, excelCNRoot, "content-cn-new")
