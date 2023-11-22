import os

import pandas as pd
import xml.etree.ElementTree as ET

df1 = pd.read_excel("中英翻译.xlsx", sheet_name="翻译文档")
df2 = pd.read_excel("中英翻译.xlsx", sheet_name="1.0.6翻译")
# 排序 去重
df1 = df1.sort_values(by='name').drop_duplicates('name')
df2 = df2.sort_values(by='name').drop_duplicates('name')


# 首字母 转 大写
def sheet_to_xml(ws, root, isChinese=1):
    for row in ws.values:
        key = row[0]
        value = row[isChinese]
        if key is not None and value is not None:
            if str(row[0]) != "name" and str(row[1]) != "Chinese" and str(row[2]) != "English":
                # print(f" {key} , {value}")
                item = ET.SubElement(root, "string", name=str(key).replace(" ", "_").replace("-", "_"))
                if isChinese == 2:
                    text = str(value).replace("Ai", "AI").replace("ai", "AI").capitalize()
                    if "\\'" in text:
                        # text = text.replace("Ai", "AI").replace("ai", "AI").capitalize()
                        pass
                    else:
                        text = text.replace("'", "\\'")
                    item.text = text
                else:
                    # 首字母 转 大写
                    item.text = str(value).replace("Ai", "AI").replace("ai", "AI").capitalize()


def excel_to_xml(filePath, isChinese=1):
    root = ET.Element("resources")
    sheet_to_xml(df1, root, isChinese)
    sheet_to_xml(df2, root, isChinese)
    tree = ET.ElementTree(root)
    tree.write(filePath, encoding='utf-8')


def isDirExistsOrCreate(path: str):
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)


if __name__ == '__main__':
    isDirExistsOrCreate("excel")
    isDirExistsOrCreate("excel-en")
    excel_to_xml(r"excel/strings.xml")
    excel_to_xml(r"excel-en/strings.xml", 2)
