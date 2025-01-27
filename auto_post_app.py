import streamlit as st
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
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
        response = requests.get(imagem_url, timeout=10)  # Timeout ajustado para 10 segundos
        response.raise_for_status()  # Levanta um erro para status 4xx ou 5xx
        imagem = Image.open(io.BytesIO(response.content))
        imagem = imagem.resize((largura, altura))
        return imagem
    except Exception as e:
        st.error(f"Erro ao carregar a imagem: {e}")
        # Fallback para uma imagem padrão se o link não for válido
        imagem_fallback_url = "https://via.placeholder.com/1200x628.png?text=Imagem+Produto+Indisponível"
        response = requests.get(imagem_fallback_url)
        imagem = Image.open(io.BytesIO(response.content))
        imagem = imagem.resize((largura, altura))
        return imagem

def sobrepor_texto_na_imagem(imagem, texto):
    try:
        draw = ImageDraw.Draw(imagem)
        fonte = ImageFont.load_default()
        largura, altura = imagem.size
        texto_largura, texto_altura = draw.textsize(texto, font=fonte)
        posicao = ((largura - texto_largura) // 2, altura - texto_altura - 20)
        draw.text(posicao, texto, (255, 255, 255), font=fonte)
        return imagem
    except Exception as e:
        st.error(f"Erro ao sobrepor texto na imagem: {e}")
        return imagem

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
                response = requests.get(url, headers=headers, timeout=15)
                response.raise_for_status()  # Levanta um erro para status 4xx ou 5xx
                soup = BeautifulSoup(response.content, 'html.parser')

                # Extração simplificada de informações do produto
                title = soup.find('span', {'id': 'productTitle'}).text.strip() if soup.find('span', {'id': 'productTitle'}) else "Produto Genérico"
                preco_original = soup.find('span', {'id': 'priceblock_ourprice'}).text if soup.find('span', {'id': 'priceblock_ourprice'}) else "0.00"
                preco_atual = preco_original
                cupom = "PROMO2023"  # Definido manualmente aqui, ou pode ser extraído de outra forma
                descricao = soup.find('div', {'id': 'productDescription'}).text.strip() if soup.find('div', {'id': 'productDescription'}) else "Sem descrição disponível"
                imagem_url = soup.find('img', {'id': 'landingImage'})['src'] if soup.find('img', {'id': 'landingImage'}) else "https://via.placeholder.com/1200x628.png?text=Imagem+Produto"
                
                title = st.text_input("Título do produto:", title)
                preco_original = st.number_input("Preço original (€):", value=float(preco_original.replace('€', '').replace(',', '.')), step=0.01)
                preco_atual = st.number_input("Preço atual (€):", value=float(preco_atual.replace('€', '').replace(',', '.')), step=0.01)
                cupom = st.text_input("Cupom:", cupom)
                tags = st.text_input("Tags (separadas por vírgula):", "").split(",")
                estilo_post = st.radio("Estilo do post:", ["emoji", "formal"], index=0)

                produto = {
                    'nome': title,
                    'preco_original': preco_original,
                    'preco_atual': preco_atual,
                    'cupom': cupom
                }

                if st.button("Gerar Post"):
                    post_texto = gerar_post(produto, url, tags, estilo=estilo_post)
                    st.write("### Pré-visualização do Post:")
                    st.text_area("Texto do Post:", post_texto, height=200)
                    st.download_button("Baixar Post (.txt)", data=post_texto, file_name="post_gerado.txt")

                st.write("### Imagem do Produto:")
                imagem_resized = redimensionar_imagem(imagem_url, 1200, 628)
                if imagem_resized:
                    imagem_final = sobrepor_texto_na_imagem(imagem_resized, f"{calcular_desconto(preco_original, preco_atual)}% OFF")
                    st.image(imagem_final, caption="Pré-visualização da Imagem", use_container_width=True)
                    buffer = io.BytesIO()
                    imagem_final.save(buffer, format="PNG")
                    st.download_button("Baixar Imagem", data=buffer.getvalue(), file_name="imagem_produto.png", mime="image/png")

                st.write("### Compartilhar:")
                st.button("Compartilhar no Facebook (Simulado)")

            except requests.exceptions.RequestException as e:
                st.error(f"Erro ao processar o link: {e}")

# Executando a aplicação
if __name__ == "__main__":
    auto_post_app()
