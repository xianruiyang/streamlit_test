import streamlit as st
import pandas as pd
from PIL import Image 

st.markdown("# Page 1 ❄️")
st.sidebar.markdown("# Page 1 ❄️")
image_01 = Image.open('./image/school.jpg')
st.image(image_01)