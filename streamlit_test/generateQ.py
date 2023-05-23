import my_database as db

import random
import json
from lxml import etree

root = "./"

mdb = db.herb_db(root+'data/meddb.json')
mdb.update()
recipeIDs = list(mdb.data["recipe"].keys())
herbIDs = list(mdb.data["herb"].keys())

f = open(root+"data/learn_list.json")
learnList = json.load(f)
learnList = learnList[0:600]
f.close()
f = open(root+"data/fromList.json",encoding="utf-8")
fromList = json.load(f)
f.close()

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
    return output

def herbQ(id):
    correctOption = random.randint(0,3)
    temp = mdb.data["recipe"][id]
    resList = copy_list(herbIDs)
    correctID = random.choice(temp[1])[0]
    resList.remove(correctID)
    options = random.sample(resList,4)
    options[correctOption] = correctID
    for i in range(len(options)):
        options[i] = mdb.get_herb_name(options[i])
    options[0] = "A\n"+options[0]
    options[1] = "B\n"+options[1]
    options[2] = "C\n"+options[2]
    options[3] = "D\n"+options[3]
    out = {"type":"radio","quest":"请问 "+temp[0][0]+" 中含有以下哪种药材","options":options,"correct":correctOption}
    return out
def herbQs(num,seed):
    random.seed(seed)
    out = []
    recipeIDList = random.sample(recipeIDs,num)
    for i in recipeIDList:
        out.append(herbQ(i))
    return out

def fromQ():
    tempFromList = list(fromList)
    correctOption = random.randint(0,3)
    cr = random.choice(learnList)
    cr = readHtml(cr["html"])
    name = cr[0][1]
    tempFromList.remove(cr[1][1])
    options = random.sample(tempFromList,4)
    options[correctOption] = cr[1][1]
    out = {"type":"radio","quest":name+" 出自","options":options,"correct":correctOption}
    return out
def fromQs(num,seed):
    random.seed(seed)
    out = []
    for i in range(num):
        out.append(fromQ())
    return out

def useQ():
    correctOption = random.randint(0,3)
    options = random.sample(learnList,4)
    name = options[correctOption]["name"]
    for i in range(len(options)):
        options[i] = readHtml(options[i]["html"])[4][1]
    options[0] = "A\n"+options[0]
    options[1] = "B\n"+options[1]
    options[2] = "C\n"+options[2]
    options[3] = "D\n"+options[3]
    out = {"type":"radio","quest":"以下选项最符合 "+name+" 的功效描述的是","options":options,"correct":correctOption}
    return out
def useQs(num,seed):
    random.seed(seed)
    out = []
    for i in range(num):
        out.append(useQ())
    return out