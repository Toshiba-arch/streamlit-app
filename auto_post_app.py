import streamlit as st
import requests
from bs4 import BeautifulSoup
from time import sleep

# Função para gerar o texto do post
def gerar_post(produto, link_referencia, tags):
    nome = produto['nome']
    preco_original = produto['preco_original']
    preco_atual = produto['preco_atual']
    desconto = produto['desconto']
    cupom = produto['cupom']
    
    post_texto = f"📢 **Oferta Imperdível!** 📢\n"
    post_texto += f"🔹 **{nome}**\n"
    post_texto += f"💰 Antes **€{preco_original:.2f}** AGORA **€{preco_atual:.2f}**!\n"
    post_texto += f"📉 Poupa já **{desconto}%**!\n"
    if cupom:
        post_texto += f"💥 Use o código de cupom no checkout: **{cupom}**\n"
    post_texto += f"👉 [Compra agora]({link_referencia})\n"
    if tags:
        post_texto += "\n" + " ".join([f"#{tag}" for tag in tags])
    return post_texto

def auto_post_app():
    st.write("### Gerador Automático de Posts")

    # Input para o link de referência
    url = st.text_input("Insira o link de referência para gerar o post automaticamente:")

    if url:
        with st.spinner('Carregando...'):
            try:
                # Cabeçalho para emular um navegador e evitar bloqueio
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                }

                # Tentativa de obter o conteúdo da página
                response = requests.get(url, headers=headers)
                response.raise_for_status()  # Levanta uma exceção se o status code não for 200
                soup = BeautifulSoup(response.content, 'html.parser')

                # Extração dos dados do link
                title = soup.title.string if soup.title else "Sem título disponível"
                description = ""
                desc_tag = soup.find("meta", attrs={"name": "description"})
                if desc_tag and "content" in desc_tag.attrs:
                    description = desc_tag.attrs["content"]

                # Captura o preço (se disponível)
                price = "Preço não disponível"
                price_tag = soup.find("meta", property="product:price:amount")
                if price_tag and "content" in price_tag.attrs:
                    price = f"€ {price_tag.attrs['content']}"

                # Captura o desconto
                discount = "Sem desconto"
                discount_tag = soup.find("meta", property="product:discount:amount")
                if discount_tag and "content" in discount_tag.attrs:
                    discount = f"Desconto: {discount_tag.attrs['content']}%"

                # Captura o cupom
                coupon = "Sem cupom disponível"
                coupon_tag = soup.find("meta", property="product:discount:code")
                if coupon_tag and "content" in coupon_tag.attrs:
                    coupon = f"Cupom: {coupon_tag.attrs['content']}"

                # Exibição dos dados extraídos
                st.write("#### Personalize os elementos do post:")
                title = st.text_input("Título (ex: Nome do Produto):", value=title, key="auto_title")
                description = st.text_area("Descrição (detalhes do produto):", value=description, key="auto_description", height=100)
                price = st.text_input("Preço (ex: €199,99):", value=price, key="auto_price")
                discount = st.text_input("Desconto (ex: 20%):", value=discount, key="auto_discount")
                coupon = st.text_input("Cupom (ex: CÓDIGO20):", value=coupon, key="auto_coupon")

                # Campo para URL de imagem
                image_url = st.text_input("Insira a URL da imagem desejada:", "")
                if image_url:
                    try:
                        response = requests.get(image_url)
                        if response.status_code == 200:
                            st.image(image_url, caption="Imagem inserida pelo usuário", use_column_width=True)
                        else:
                            st.error("Erro ao carregar a imagem. Verifique a URL.")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Erro ao carregar a imagem: {e}")

                # Tags
                tags = st.text_input("Tags (separadas por vírgula):", "")

                # Gerar conteúdo do post
                produto = {
                    'nome': title,
                    'preco_original': price,
                    'preco_atual': price,
                    'desconto': discount.replace("Desconto: ", "").replace("%", "") if discount != "Sem desconto" else "0",
                    'cupom': coupon if coupon != "Sem cupom disponível" else ""
                }
                post_texto = gerar_post(produto, url, tags.split(",") if tags else [])

                st.write("### Pré-visualização do Post:")
                st.text_area("Texto do Post para copiar e colar:", value=post_texto, height=200)

                # Botões para download
                st.download_button("Baixar Post (.txt)", data=post_texto, file_name="post_automatico.txt")
                
                # Exportação para Markdown
                post_md = (
                    f"# {title}\n\n"
                    f"{description}\n\n"
                    f"**Preço:** {price}\n"
                    f"**Desconto:** {discount}\n"
                    f"**Cupom:** {coupon}\n\n"
                    f"**Clique aqui para aproveitar a oferta:** {url}\n\n"
                )
                if image_url:
                    post_md += f"![Imagem do Produto]({image_url})\n"
                st.download_button("Baixar Post (.md)", data=post_md, file_name="post_automatico.md")

            except requests.exceptions.RequestException as e:
                st.error(f"Erro ao processar o link: {e}")
                sleep(2)  # Tenta novamente após 2 segundos
