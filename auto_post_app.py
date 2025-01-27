import streamlit as st
import requests
from bs4 import BeautifulSoup
from PIL import Image
import io

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

def gerar_post(produto, link_referencia, tags, estilo="emoji"):
    nome = produto['nome']
    preco_original = produto['preco_original']
    preco_atual = produto['preco_atual']
    cupom = produto['cupom']
    desconto = calcular_desconto(preco_original, preco_atual)

    if estilo == "emoji":
        post_texto = f"📢 **Oferta Imperdível!** 📢\n"
        post_texto += f"🔹 **{nome}**\n"
        post_texto += f"💰 Antes **€{preco_original:.2f}** AGORA **€{preco_atual:.2f}**!\n"
        post_texto += f"📉 Poupa já **{desconto}%**!\n"
        if cupom:
            post_texto += f"💥 Use o código de cupom no checkout: **{cupom}**\n"
        post_texto += f"👉 [Compra agora]({link_referencia})\n"
        if tags:
            post_texto += "\n" + " ".join([f"#{tag}" for tag in tags])
    else:
        post_texto = f"**Oferta Imperdível!**\n"
        post_texto += f"Produto: **{nome}**\n"
        post_texto += f"Preço original: €{preco_original:.2f} | Preço atual: €{preco_atual:.2f}\n"
        post_texto += f"Desconto: **{desconto}%**\n"
        if cupom:
            post_texto += f"Cupom: {cupom}\n"
        post_texto += f"Link: [Clique aqui para comprar]({link_referencia})\n"
        if tags:
            post_texto += "\nTags: " + ", ".join(tags)

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

    url = st.text_input("Insira o link de referência para gerar o post automaticamente:")

    if url:
        with st.spinner('Carregando o produto...'):
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    "Accept-Language": "en-US,en;q=0.9,pt;q=0.8",
                }
                response = requests.get(url, headers=headers, timeout=15)  # Timeout aumentado
                response.raise_for_status()  # Levanta um erro para status 4xx ou 5xx
                soup = BeautifulSoup(response.content, 'html.parser')

                # Extração de informações do produto
                title = soup.find('span', {'id': 'productTitle'}).text.strip() if soup.find('span', {'id': 'productTitle'}) else ""
                preco_original = soup.find('span', {'id': 'priceblock_ourprice'}).text.strip().replace("€", "").replace(",", ".") if soup.find('span', {'id': 'priceblock_ourprice'}) else ""
                preco_atual = soup.find('span', {'id': 'priceblock_dealprice'}).text.strip().replace("€", "").replace(",", ".") if soup.find('span', {'id': 'priceblock_dealprice'}) else preco_original
                imagem_url = soup.find('img', {'id': 'imgBlkFront'})['src'] if soup.find('img', {'id': 'imgBlkFront'}) else ""
                cupom = "PROMO2023"  # Este pode ser um campo manual, mas por enquanto estou configurando um valor fixo
                tags = ["promoção", title.replace(" ", "").lower()]  # Tags sugeridas

                # Preenchendo campos de input
                title = st.text_input("Título do produto:", title)
                preco_original = st.text_input("Preço original (€):", preco_original)
                preco_atual = st.text_input("Preço atual (€):", preco_atual)
                cupom = st.text_input("Cupom:", cupom)
                tags = st.text_input("Tags (separadas por vírgula):", ",".join(tags)).split(",")
                estilo_post = st.radio("Estilo do post:", ["emoji", "formal"], index=0)

                produto = {
                    'nome': title,
                    'preco_original': preco_original,
                    'preco_atual': preco_atual,
                    'cupom': cupom
                }

                # Carregando a imagem automaticamente
                if imagem_url:
                    imagem_resized = redimensionar_imagem(imagem_url, 1200, 628)
                    if imagem_resized:
                        st.image(imagem_resized, caption="Pré-visualização da Imagem", use_container_width=True)
                        buffer = io.BytesIO()
                        imagem_resized.save(buffer, format="PNG")
                        st.download_button("Baixar Imagem", data=buffer.getvalue(), file_name="imagem_produto.png", mime="image/png")
                    else:
                        st.error("Não foi possível carregar a imagem para este produto.")
                else:
                    st.error("Imagem não encontrada.")

                # Gerar post
                if st.button("Gerar Post"):
                    post_texto = gerar_post(produto, url, tags, estilo=estilo_post)
                    st.write("### Pré-visualização do Post:")
                    st.text_area("Texto do Post:", post_texto, height=200)
                    st.download_button("Baixar Post (.txt)", data=post_texto, file_name="post_gerado.txt")

                # Compartilhar no Facebook
                facebook_url = f"https://www.facebook.com/sharer/sharer.php?u={url}"
                st.markdown(f"[Compartilhar no Facebook]({facebook_url})")

            except requests.exceptions.RequestException as e:
                st.error(f"Erro ao processar o link: {e}")

# Executando a aplicação
if __name__ == "__main__":
    auto_post_app()
