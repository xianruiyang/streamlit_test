import streamlit as st
from streamlit.components.v1 import html

import json
from lxml import etree
import pandas as pd
from PIL import Image 

import myfun as mf

def readHtml(fileName):
    output = []
    rootHead = "./html/"
    f = open(rootHead+fileName,encoding="utf-8")
    content = f.read()
    f.close()
    html = etree.HTML(content)
    tr = html.xpath("//tr")
    for i in tr:
        output.append([i.xpath("th/text()")[0],i.xpath("td/text()")[0]])
    return output

def getList():
    f = open("./data/learn_list.json")
    data = json.load(f)
    f.close()
    return data

def setHtmlOutput(output):
    st.markdown("# "+output[0][1])
    st.markdown("###### "+output[1][0]+":"+output[1][1])
    st.markdown("---")
    for i in range(2,9):
        st.markdown("##### "+output[i][0])
        st.markdown(output[i][1])
        st.markdown("***")

st.set_page_config(
    page_title="知识学习",
)

learnList = getList()

mySearch = st.sidebar.text_input("搜索",placeholder="输入你要搜索的内容")
if mySearch:
    learnList = mf.sort_list(learnList,mySearch)

holder = st.sidebar.container()
showPerPage = st.sidebar.number_input("每页显示",min_value=5,max_value=50,value=5)
myPageNum = holder.number_input("页码",min_value=1,max_value=int((len(learnList)-1)/showPerPage+1))
#myPageNum = st.sidebar.number_input("页码",min_value=1,max_value=int((len(learnList)-1)/showPerPage+1))
num = 10
if myPageNum:
    num = myPageNum
first = (num-1)*showPerPage
last = num*showPerPage
if last>len(learnList):
    last = len(learnList)
learnList = learnList[first:last]

idx = 0
buttonList = []
for i in learnList:
    new = st.sidebar.button(label=i["name"],key=idx)
    buttonList.append([new,i["html"]])
    idx+=1
for i in buttonList:
    if i[0]:
        out = readHtml(i[1])
        setHtmlOutput(out)
        break
else:
    out = readHtml(buttonList[0][1])
    setHtmlOutput(out)

image_01 = Image.open('./image/school.jpg')
#st.image(image_01,width=300)

