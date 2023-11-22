import os
import pandas as pd
import xml.etree.ElementTree as ET

from pandas import DataFrame


def is_in_excel(e: ET.Element, root: ET.Element) -> bool:
    for child in root:
        nameE = e.get("name")
        nameChild = child.get("name")
        if nameE == nameChild:
            return True


def is_dir_exists_or_create(path: str):
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)


def find_new(original_e, excel_e, dir_new):
    new_root = ET.Element("resources")
    new_tree = ET.ElementTree(new_root)
    for excelChild in excel_e:
        if not is_in_excel(excelChild, original_e):
            new_root.append(excelChild)
    is_dir_exists_or_create(dir_new)
    new_tree.write(f"{dir_new}/strings.xml", encoding='utf-8', xml_declaration=True, short_empty_elements=True)


def find_change(originalE, excelE, dir_change):
    change_root = ET.Element("resources")
    change_tree = ET.ElementTree(change_root)
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
                change_root.append(originalChild)
                change_root.append(excelChild)
    is_dir_exists_or_create(dir_change)
    change_tree.write(f"{dir_change}/strings.xml", encoding='utf-8', xml_declaration=True, short_empty_elements=True)


# 对比 输出 两个xml 中文相同 而 key 不同的 (原本的xml 作为参照物)
def compare_elements_content(original_e: ET.Element, excel_e: ET.Element, dir_no_same: str):
    no_same_root = ET.Element("resources")
    no_same_tree = ET.ElementTree(no_same_root)
    for original_child in original_e:
        for excel_child in excel_e:
            if original_child == "resources" or excel_child.tag == "resources":
                continue
            original_name = original_child.attrib['name']
            excel_name = excel_child.attrib['name']
            # 找出 内容相同 而 name 不同的, 并且 不在 excel 上面的
            if original_child.tag == excel_child.tag and original_name != excel_name \
                    and original_child.text == excel_child.text and not is_in_excel(original_child, excel_e):
                excel_child.attrib['excel'] = "1"
                no_same_root.append(original_child)
                no_same_root.append(excel_child)
    # 输出不想的 两个
    is_dir_exists_or_create(dir_no_same)
    no_same_tree.write(f"{dir_no_same}/strings.xml", encoding="utf-8", short_empty_elements=True)


class ExcelToXml:
    def __init__(self, origin_path_cn, origin_path_en, out_path_cn, out_path_en):
        """"初始化方法"""
        self.origin_path_cn = origin_path_cn
        self.out_path_cn = out_path_cn
        self.origin_path_en = origin_path_en
        self.out_path_en = out_path_en

        # self.original_cn_tree = ET.parse(origin_path_cn)
        self.original_cn_root = ET.parse(origin_path_cn).getroot()

        # self.original_en_tree = ET.parse(origin_path_en)
        self.original_en_root = ET.parse(origin_path_en).getroot()

    def __sheet_to_xml(self, df: DataFrame, root: ET.Element, is_chinese: int = 1):
        """
         sheet 转 xml 首字母 转 大写
        :param df: pandas DataFrame 对象
        :param root: xml.etree.ElementTree 的 Element 对象
        :param is_chinese: 是否是中文
        :return: None
        """
        for row in df.values:
            key = row[0]
            value = row[is_chinese]
            if key is not None and value is not None:
                if str(row[0]) != "name" and str(row[1]) != "Chinese" and str(row[2]) != "English":
                    item = ET.SubElement(root, "string", name=str(key).replace(" ", "_").replace("-", "_"))
                    if is_chinese == 2:
                        text = str(value).replace("Aipay", "AIPay").replace("aib", "AIB").capitalize()
                        if "\\'" in text:
                            pass
                        else:
                            text = text.replace("'", "\\'")
                        item.text = text
                    else:
                        item.text = str(value).replace("Aipay", "AIPay").replace("aib", "AIB").capitalize()

    def excel_to_xml(self, excel_path: str, sheet_name_list: list, is_chinese: int = 1):
        """
         excel 转 xml
        :param excel_path: excel 路径
        :param sheet_name_list: sheet 名称List
        :param is_chinese: d
        :return: None
        """
        if is_chinese == 1:
            out_path = self.out_path_cn
        else:
            out_path = self.out_path_en

        is_dir_exists_or_create(out_path)

        root = ET.Element("resources")
        for sheet_name in sheet_name_list:
            df = pd.read_excel(excel_path, sheet_name=sheet_name).sort_values(by='name').drop_duplicates('name')
            self.__sheet_to_xml(df, root, is_chinese)
        tree = ET.ElementTree(root)
        tree.write(f"{out_path}/strings.xml", encoding='utf-8')

    def find_change_cn(self, dir_change="content-cn-change"):
        """
        中文，查找 已有name 的内容变化
        :param dir_change:
        :return:
        """
        excel_cn_root = ET.parse(f"{self.out_path_cn}/strings.xml").getroot()
        find_change(self.original_cn_root, excel_cn_root, dir_change)

    def find_change_en(self, dir_change="content-en-change"):
        """
        英文，查找 已有name 的内容变化
        :param dir_change:
        :return:
        """
        excel_en_root = ET.parse(f"{self.out_path_en}/strings.xml").getroot()
        find_change(self.original_en_root, excel_en_root, dir_change)

    def find_new_cn(self, dir_new="content-cn-new"):
        """
        中文，查找新曾的内容
        :param dir_new:
        :return:
        """
        excel_cn_root = ET.parse(f"{self.out_path_cn}/strings.xml").getroot()
        find_new(self.original_cn_root, excel_cn_root, dir_new)

    def find_new_en(self, dir_new="content-en-new"):
        """
        英文，查找新增的内容
        :param dir_new:
        :return:
        """
        excel_en_root = ET.parse(f"{self.out_path_en}/strings.xml").getroot()
        find_new(self.original_en_root, excel_en_root, dir_new)

    def compare_element_cn(self, dir_compare="content-cn-compare"):
        """
        中文，比较，找出 内容相同，name不同的
        :param dir_compare:
        :return:
        """
        excel_cn_root = ET.parse(f"{self.out_path_cn}/strings.xml").getroot()
        compare_elements_content(self.original_cn_root, excel_cn_root, dir_compare)

    def compare_element_en(self, dir_compare="content-en-compare"):
        """
           英文，比较，找出 内容相同，name不同的
           :param dir_compare:
           :return:
           """
        excel_en_root = ET.parse(f"{self.out_path_en}/strings.xml").getroot()
        compare_elements_content(self.original_en_root, excel_en_root, dir_compare)
