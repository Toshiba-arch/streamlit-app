import streamlit as st
import requests
from bs4 import BeautifulSoup

def auto_post_app():
    st.write("### Gerador Automático de Posts")

    # Input para o link de referência
    url = st.text_input("Insira o link de referência para gerar o post automaticamente:")

    if url:
        with st.spinner('Carregando...'):
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

                # Exibição dos elementos extraídos com opção de edição
                st.write("#### Personalize os elementos do post:")
                title = st.text_input("Título (ex: Nome do Produto):", value=title, key="auto_title")
                description = st.text_area("Descrição (detalhes do produto):", value=description, key="auto_description", height=100)
                price = st.text_input("Preço (ex: R$ 199,99):", value=price, key="auto_price")
                discount = st.text_input("Desconto (ex: 20%):", value=discount, key="auto_discount")
                coupon = st.text_input("Cupom (ex: CÓDIGO20):", value=coupon, key="auto_coupon")

                # Ajuste de imagem
                if image_url:
                    st.write("#### Imagem do produto:")
                    st.image(image_url, caption="Imagem extraída do link")
                    use_image = st.checkbox("Usar esta imagem no post", value=True)
                    if use_image:
                        image_width = st.slider("Ajuste a largura da imagem:", min_value=100, max_value=800, value=400)
                        image_height = st.slider("Ajuste a altura da imagem:", min_value=100, max_value=600, value=300)
                        st.image(image_url, caption="Imagem ajustada", width=image_width, height=image_height)
                else:
                    st.write("Nenhuma imagem encontrada.")
                    use_image = False

                # Construção do post final
                st.write("### Post Final:")
                post_content = (
                    f"**{title}**\n\n"
                    f"{description}\n\n"
                    f"Preço: {price}\n"
                    f"{discount}\n"
                    f"{coupon}\n"
                    f"Aproveite esta oferta clicando no link: {url}"
                )

                if use_image and image_url:
                    post_content += f"\n\n![Imagem do Produto]({image_url})"

                st.text_area("Pré-visualização do Post:", value=post_content, height=300)

                # Botões para download do post final
                st.download_button("Baixar Post (.txt)", data=post_content, file_name="post_automatico.txt")
                
                # Exportação para Markdown
                post_md = (
                    f"# {title}\n\n"
                    f"{description}\n\n"
                    f"**Preço:** {price}\n"
                    f"**Desconto:** {discount}\n"
                    f"**Cupom:** {coupon}\n\n"
                    f"**Clique aqui para aproveitar a oferta:** {url}\n\n"
                )
                if use_image and image_url:
                    post_md += f"![Imagem do Produto]({image_url})\n"
                st.download_button("Baixar Post (.md)", data=post_md, file_name="post_automatico.md")

            except Exception as e:
                st.error(f"Erro ao processar o link: {e}")
