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

            # Capturar título do produto
            title = soup.title.string if soup.title else "Sem título disponível"

            # Capturar descrição
            description = ""
            desc_tag = soup.find("meta", attrs={"name": "description"})
            if desc_tag and "content" in desc_tag.attrs:
                description = desc_tag.attrs["content"]

            # Capturar imagem do produto (preview)
            image_url = ""
            image_tag = soup.find("meta", property="og:image")
            if image_tag and "content" in image_tag.attrs:
                image_url = image_tag.attrs["content"]

            # Capturar preço
            price = "Preço não disponível"
            price_tag = soup.find("meta", property="product:price:amount")
            if price_tag and "content" in price_tag.attrs:
                price = f"R$ {price_tag.attrs['content']}"

            # Capturar desconto
            discount = "Sem desconto"
            discount_tag = soup.find("meta", property="product:discount:amount")
            if discount_tag and "content" in discount_tag.attrs:
                discount = f"Desconto: {discount_tag.attrs['content']}%"

            # Capturar cupom ou instrução para desconto
            coupon = "Sem cupom disponível"
            coupon_tag = soup.find("meta", property="product:discount:code")
            if coupon_tag and "content" in coupon_tag.attrs:
                coupon = f"Cupom: {coupon_tag.attrs['content']}"

            # Construção da descrição sugerida
            suggested_description = (
                f"**{title}**\n\n"
                f"{description}\n\n"
                f"Preço: {price}\n"
                f"{discount}\n"
                f"{coupon}\n"
                f"Aproveite esta oferta clicando no link: {url}"
            )

            # Exibição dos dados extraídos
            st.write("#### Título sugerido:")
            st.text_input("Título:", value=title, key="auto_title")

            st.write("#### Descrição sugerida:")
            st.text_area("Descrição:", value=suggested_description, key="auto_description", height=200)

            if image_url:
                st.write("#### Imagem sugerida:")
                st.image(image_url, caption="Imagem extraída do link")
            else:
                st.write("Nenhuma imagem encontrada.")

            # Botão para download ou ajuste do post final
            st.download_button("Baixar Post", data=suggested_description, file_name="post_automatico.txt")

        except Exception as e:
            st.error(f"Erro ao processar o link: {e}")
