import streamlit as st
from PIL import Image

import random
import uuid
from lxml import etree
from streamlit.components.v1 import html
import json
import pandas as pd

st.markdown("# 欢迎使用中药配方学习系统")

image_01 = Image.open('./image/school.jpg')
st.image(image_01,width=300)