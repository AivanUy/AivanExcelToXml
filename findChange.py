# 找出 英文 name 相同 content 不同的
import os.path
import xml.etree.ElementTree as ET

originalEnTree = ET.parse("original-en/strings.xml")
originalEnRoot = originalEnTree.getroot()

excelEnTree = ET.parse("value-en/strings.xml")
excelEnRoot = excelEnTree.getroot()


# 对比 相同的name ，找出不同的 content 的 (原本的xml 作为参照物)
def compare_elements_name_not_content(originalE, excelE):
    noSameRoot = ET.Element("resources")
    noSameTree = ET.ElementTree(noSameRoot)
    for originalChild in originalE:
        for excelChild in excelE:
            if originalChild == "resources" or excelChild == "resources":
                continue

            originalName = originalChild.get('name')
            originalContent = originalChild.text

            excelName = excelChild.get('name')
            excelContent = excelChild.text

            if originalChild.tag == excelChild.tag and originalName == excelName and originalContent != excelContent:
                excelChild.attrib['excel'] = "1"
                noSameRoot.append(originalChild)
                noSameRoot.append(excelChild)

    dir_noSame = "content-change"
    isExists = os.path.exists(dir_noSame)
    if not isExists:
        os.makedirs(dir_noSame)

    noSameTree.write(f"{dir_noSame}/strings.xml", encoding='utf-8', xml_declaration=True, short_empty_elements=True)


if __name__ == '__main__':
    compare_elements_name_not_content(originalEnRoot, excelEnRoot)
