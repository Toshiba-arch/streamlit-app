import os
import streamlit as st

st.title("Menu Principal")
escolha = st.selectbox("Escolha uma funcionalidade", ["Gerador de Posts", "Gerador de Números do Euromilhões"])

if escolha == "Gerador de Posts":
    os.system("streamlit run app_ofertas.py")
elif escolha == "Gerador de Números do Euromilhões":
    os.system("streamlit run app_euromilhoes.py")
