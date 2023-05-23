import streamlit as st
import random

import generateQ as gq



randomKey = st.sidebar.number_input("试卷号",min_value=0,max_value=100000,value=0)
questNum = st.sidebar.number_input("题目数量",min_value=15,max_value=150,value=15)
st.markdown("---")

while 1:
    try:
        row_qList = []
        row_qList += gq.herbQs(int(questNum/3),randomKey*questNum-questNum)
        row_qList += gq.fromQs(int(questNum/3),randomKey*questNum-questNum)
        row_qList += gq.useQs(questNum-2*int(questNum/3),randomKey*questNum-questNum)
        random.shuffle(row_qList)
        break
    except:
        randomKey+=1
        #st.markdown("### 这个试卷号似乎出了点问题，试试别的吧")

qList = []
idx = 1
for i in row_qList:
    if(i["type"]=="radio"):
        q = st.radio(str(idx)+"、"+i["quest"],i["options"])
        cr = st.container()
        st.markdown("---")
        qList.append([q,i["options"][i["correct"]],cr])
    idx+=1
idx = 1
wrongList = []
if st.button("提交"):
    point = 0
    for i in qList:
        if i[0]==i[1]:
            point+=1
            i[2].markdown("回答正确")
        else:
            i[2].markdown("回答错误")
            i[2].markdown("你选择了 {}".format(i[0]))
            i[2].markdown("答案是 {}".format(i[1]))
            wrongList.append(str(idx))
        idx+=1
    st.sidebar.markdown("# 得分：{}".format(str(int(point/questNum*100))))
    st.sidebar.markdown("共{}题，你做对了{}题".format(str(questNum),str(point)))
    if len(wrongList):
        wrongList = "、".join(wrongList)
        st.sidebar.markdown("错误题号 "+wrongList)

    
