import os.path
import xml.etree.ElementTree as ET
# 找出 中文 内容相同 name 不相同的  改成 excel 里面的 name
# 对比原来的strings.xml 和 excel生成的 strings.xml，找出 原来中 不在excel 内的 并输出，确保 name 和 excel 上的翻译一至 ，这需要 输出后 手动去修改
originalTree = ET.parse("original/strings.xml")
originalRoot = originalTree.getroot()

excelTree = ET.parse("value/strings.xml")
excelRoot = excelTree.getroot()


def isInExcel(e: ET.Element, root: ET.Element) -> bool:
    for child in root:
        nameE = e.get("name")
        nameChild = child.get("name")
        if nameE == nameChild:
            return True


# 对比 输出 两个xml 中文相同 而 key 不同的 (原本的xml 作为参照物)
def compare_elements_content(originalE, excelE):
    noSameRoot = ET.Element("resources")
    noSameTree = ET.ElementTree(noSameRoot)
    for originalChild in originalE:
        for excelChild in excelE:
            if originalChild == "resources" or excelChild.tag == "resources":
                continue
            originalName = originalChild.attrib['name']
            excelName = excelChild.attrib['name']
            # 找出 内容相同 而 name 不同的, 并且 不在 excel 上面的
            if originalChild.tag == excelChild.tag and originalName != excelName \
                    and originalChild.text == excelChild.text and not isInExcel(originalChild, excelRoot):
                excelChild.attrib['excel'] = "1"
                noSameRoot.append(originalChild)
                noSameRoot.append(excelChild)
    # 输出不想的 两个
    dir_noSame = "no-same"
    isExists = os.path.exists(dir_noSame)
    if not isExists:
        os.makedirs(dir_noSame)
    noSameTree.write("noSame/strings.xml", encoding="utf-8", short_empty_elements=True)


if __name__ == '__main__':
    compare_elements_content(originalRoot, excelRoot)
