import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_excel("data.xlsx")

category = st.selectbox("Vyber kategóriu", df["Kategória"].unique())
filtered = df[df["Kategória"] == category]

fig = px.line(filtered, x="Dátum", y="Hodnota", color="Typ")
st.plotly_chart(fig)
