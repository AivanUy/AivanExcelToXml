# This is a sample Python script.
import html

from ExcelToXml import ExcelToXml


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    e2xml = ExcelToXml("original/strings.xml", "original-en/strings.xml", "excel", "excel-en")

    # excel 转 xml
    e2xml.excel_to_xml("中英翻译.xlsx", ["翻译文档", "1.0.6翻译"], 1)
    e2xml.excel_to_xml("中英翻译.xlsx", ["翻译文档", "1.0.6翻译"], 2)

    # 找出原有的name 内容的变化
    e2xml.find_change_cn()
    e2xml.find_change_en()

    # 找出新增加的name 和内容
    e2xml.find_new_cn()
    e2xml.find_new_en()

     # 比较，找出 内容相同，name不同的
    e2xml.compare_element_cn()
    e2xml.compare_element_en()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
