import json
from lxml import etree

root = "../"
f = open(root+"data/learn_list.json")
learnList = json.load(f)
f.close()

fromList = set()

def copy_list(inp):
    rt = list(inp)
    if len(rt) and (isinstance(rt[0],list) or isinstance(rt[0],tuple)):
        for i in range(len(rt)):
            rt[i] = copy_list(rt[i])
    return rt

def readHtml(fileName):
    output = []
    rootHead = root+"html/"
    try:
        f = open(rootHead+fileName,encoding="utf-8")
        content = f.read()
        f.close()
        html = etree.HTML(content)
        tr = html.xpath("//tr")
        for i in tr:
            output.append([i.xpath("th/text()")[0],i.xpath("td/text()")[0]])
    except:
        print(fileName)
    if output[1][1] == "验方":
        print(fileName)
    return output

def fromQ():
    for i in learnList:
        temp = readHtml(i["html"])
        fromList.add(temp[1][1])

fromQ()
with open("../data/fromList.json","w",encoding="utf-8")  as f:
    fromList = list(fromList)
    print(fromList)
    json.dump(fromList,f,ensure_ascii=False)
    
