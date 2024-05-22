import pandas as pd
import streamlit as st
from genere import generer
import os

df = pd.read_csv('contacts_safti_csv.csv')
df=df.drop(['photo', 'minisite'], axis=1)

regions = list(df['region'].unique())
departements = list(df['département'].unique())
regions.insert(0,"Toutes les régions")
choix = st.sidebar.selectbox("Choisir une région", regions)
df = df.drop('Unnamed: 0', axis=1)

st.write(f"Sélection : {choix}")

if choix == "Toutes les régions":
    st.write(df.to_html(index=False), unsafe_allow_html=True)
else :
    df=df[df['region']==choix]
    st.write(df.to_html(index=False), unsafe_allow_html=True)