import sys
from tkinter import messagebox as mb
import urllib.request
import xml.dom.minidom


valute_names = []
global ID
ID = {}


def getCourse(url, names=None):
    try:
        webInfo = urllib.request.urlopen(url)
        data = webInfo.read()
        url_split = url.split("/")[-1]
        XMLFile = url_split.replace("asp", "xml")
        with open(XMLFile, 'wb') as file:
            file.write(data)
        webInfo.close()
    except urllib.error.HTTPError:
        mb.showerror("Ошибка", "Проверьте ссылку парсера")
        sys.exit()
    valute_dict = {}
    DOM = xml.dom.minidom.parse(XMLFile)
    DOM.normalize()
    valutes = DOM.getElementsByTagName("Valute")
    if names is None:
        for each_valute in valutes:
            valute_dict[each_valute.getElementsByTagName("CharCode")[0].firstChild.data] = \
                round(float(each_valute.getElementsByTagName("Value")[0].firstChild.data.replace(',', '.'))
                      / int(each_valute.getElementsByTagName("Nominal")[0].firstChild.data), 4)
        val_id = []
        for k in valutes:
            val_id.append(k.getAttribute("ID"))
        for key in list(ID.keys()):
            if key not in val_id:
                del ID[key]
    else:
        for k in valutes:
            valute_dict[k.getElementsByTagName("CharCode")[0].firstChild.data] = \
                k.getElementsByTagName("Name")[0].firstChild.data
    return valute_dict


def getNames(url):
    try:
        webInfo = urllib.request.urlopen(url)
        data = webInfo.read()
        url_split = url.split("/")[-1]
        XMLFile = url_split.replace("asp", "xml")
        with open(XMLFile, 'wb') as file:
            file.write(data)
        webInfo.close()
    except urllib.error.HTTPError:
        mb.showerror("Ошибка", "Проверьте ссылку парсера")
        sys.exit()
    DOM = xml.dom.minidom.parse(XMLFile)
    DOM.normalize()
    Items = DOM.getElementsByTagName("Item")
    for each in Items:
        ID[each.getAttribute("ID")] = each.getElementsByTagName("Name")[0].firstChild.data
    return ID


if __name__ == "__main__":
    mb.showerror("Ошибка", "Проверьте подключение модулей")
    sys.exit()
