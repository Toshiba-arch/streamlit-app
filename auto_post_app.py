import streamlit as st
import requests
from bs4 import BeautifulSoup
from PIL import Image
import io
import urllib.parse

def calcular_desconto(preco_original, preco_atual):
    try:
        if preco_original == 0:
            return 0
        preco_original = float(preco_original)
        preco_atual = float(preco_atual)
        desconto = ((preco_original - preco_atual) / preco_original) * 100
        return round(desconto, 2)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0

def gerar_post(produto, link_referencia, tags):
    nome = produto['nome']
    preco_original = produto['preco_original']
    preco_atual = produto['preco_atual']
    cupom = produto['cupom']
    desconto = calcular_desconto(preco_original, preco_atual)

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

def redimensionar_imagem(imagem_url, largura, altura):
    try:
        response = requests.get(imagem_url)
        response.raise_for_status()
        imagem = Image.open(io.BytesIO(response.content))
        imagem = imagem.resize((largura, altura))
        return imagem
    except Exception as e:
        st.error(f"Erro ao carregar a imagem: {e}")
        return None

def auto_post_app():
    st.title("Gerador Automático de Posts")

    if 'url' not in st.session_state:
        st.session_state.url = ""
        st.session_state.title = ""
        st.session_state.preco_original = 0.0
        st.session_state.preco_atual = 0.0
        st.session_state.cupom = "PROMO2023"
        st.session_state.tags = ["promoção", ""]
    
    url = st.text_input("Insira o link de referência para gerar o post automaticamente:", value=st.session_state.url)

    # Se o URL for inserido, fazer o scraping
    if url:
        with st.spinner('Carregando o produto...'):
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    "Accept-Language": "en-US,en;q=0.9,pt;q=0.8",
                }
                response = requests.get(url, headers=headers, timeout=15)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')

                # Extração de informações do produto
                title = soup.find('span', {'id': 'productTitle'}).text.strip() if soup.find('span', {'id': 'productTitle'}) else ""
                preco_original = soup.find('span', {'id': 'priceblock_ourprice'}).text.strip() if soup.find('span', {'id': 'priceblock_ourprice'}) else ""
                preco_atual = soup.find('span', {'id': 'priceblock_dealprice'}).text.strip() if soup.find('span', {'id': 'priceblock_dealprice'}) else preco_original
                imagem_div = soup.find('div', {'class': 'imgTagWrapper'})

                # Se imagem for encontrada, pega o URL
                if imagem_div:
                    imagem_url = imagem_div.find('img')['src'] if imagem_div.find('img') else ""

                # Preenchendo os campos do produto
                st.session_state.title = title
                st.session_state.preco_original = preco_original
                st.session_state.preco_atual = preco_atual
                produto = {
                    'nome': title,
                    'preco_original': preco_original,
                    'preco_atual': preco_atual,
                    'cupom': st.session_state.cupom
                }

                # Exibindo o preço e a imagem
                st.text_input("Título do produto:", value=title)
                st.number_input("Preço original (€):", value=float(preco_original.replace("€", "").replace(",", ".")) if preco_original else 0.0, step=0.01)
                st.number_input("Preço atual (€):", value=float(preco_atual.replace("€", "").replace(",", ".")) if preco_atual else preco_original, step=0.01)

                # Exibição da imagem
                if imagem_url:
                    imagem_resized = redimensionar_imagem(imagem_url, 1200, 628)
                    st.image(imagem_resized, caption="Pré-visualização da Imagem", use_container_width=True)

                # Botão para gerar o post
                if st.button("Gerar Post"):
                    post_texto = gerar_post(produto, url, ["promoção", title.replace(" ", "").lower()])
                    st.write("### Pré-visualização do Post:")
                    st.text_area("Texto do Post:", post_texto, height=200)
                    st.download_button("Baixar Post (.txt)", data=post_texto, file_name="post_gerado.txt")

                    if imagem_resized:
                        buffer = io.BytesIO()
                        imagem_resized.save(buffer, format="PNG")
                        st.download_button("Baixar Imagem", data=buffer.getvalue(), file_name="imagem_produto.png", mime="image/png")
                    else:
                        st.error("Não foi possível carregar a imagem para este produto.")

                    # Link para o Facebook
                    facebook_url = f"https://www.facebook.com/sharer/sharer.php?u={url}"
                    st.markdown(f"[Compartilhar no Facebook]({facebook_url})")

                    # Link para o X (Twitter)
                    x_text = urllib.parse.quote_plus(f"{title} - {url}")  # Codifica o título e o URL para o X
                    x_url = f"https://twitter.com/intent/tweet?url={url}&text={x_text}"
                    st.markdown(f"[Compartilhar no X]({x_url})")

                    # Link para o WhatsApp
                    whatsapp_text = urllib.parse.quote_plus(f"{title} - {url}")  # Codifica o título e o URL para o WhatsApp
                    whatsapp_url = f"https://wa.me/?text={whatsapp_text}"
                    st.markdown(f"[Compartilhar no WhatsApp]({whatsapp_url})")

            except requests.exceptions.RequestException as e:
                st.error(f"Erro ao processar o link: {e}")

# Executando a aplicação
if __name__ == "__main__":
    auto_post_app()
