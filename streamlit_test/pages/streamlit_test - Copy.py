#streamlit run E:\Desktob\program\python\streamlit_test\streamlit_test\streamlit_test.py
import streamlit as st
from streamlit.components.v1 import html


f = open("E:\\Desktob\\program\\python\\streamlit_test\\streamlit_test\\web.html",'r',encoding='UTF-8')
content = f.read()
f.close()
html(content,width=1002,height=2000,scrolling = True)

