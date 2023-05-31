import streamlit as st
import pandas as pd
view = [100,150,30]
st.write("# 차트의 제목")
st.write("## 부제목")
st.bar_chart(view)
sview = pd.Series(view)
sview