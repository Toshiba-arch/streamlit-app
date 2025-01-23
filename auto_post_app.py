import streamlit as st
import requests
from bs4 import BeautifulSoup

def auto_post_app():
    st.write("### Gerador Automático de Posts")

    # Input para o link de referência
    url = st.text_input("Insira o link de referência para gerar o post automaticamente:")

    if url:
        try:
            # Extração dos dados do link
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            # Tentar capturar título e descrição
            title = soup.title.string if soup.title else "Sem título disponível"
            description = ""
            desc_tag = soup.find("meta", attrs={"name": "description"})
            if desc_tag and "content" in desc_tag.attrs:
                description = desc_tag.attrs["content"]
            else:
                description = "Sem descrição disponível."

            # Exibição dos dados extraídos
            st.write("#### Título sugerido:")
            st.text_input("Título:", value=title, key="auto_title")

            st.write("#### Descrição sugerida:")
            st.text_area("Descrição:", value=description, key="auto_description")

            # Placeholder para imagem (a ser melhorado caso imagens sejam extraídas)
            st.write("#### Imagem sugerida:")
            image_url = soup.find("meta", property="og:image")
            if image_url and "content" in image_url.attrs:
                image = image_url.attrs["content"]
                st.image(image, caption="Imagem extraída do link")
            else:
                st.write("Nenhuma imagem encontrada.")

            # Botão para download ou ajuste do post final
            st.write("### Ajuste ou finalize o seu post abaixo:")
            st.text_area("Post Final:", value=f"**{title}**\n\n{description}", height=200)
            st.download_button("Baixar Post", data=f"{title}\n\n{description}", file_name="post_automatico.txt")

        except Exception as e:
            st.error(f"Erro ao processar o link: {e}")
