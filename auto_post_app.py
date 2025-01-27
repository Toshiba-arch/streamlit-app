import streamlit as st
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
import io

if url:
    with st.spinner('Carregando...'):
        try:
            # Melhorando os cabeçalhos
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
                "Accept-Language": "pt-PT,pt;q=0.9,en-US;q=0.8,en;q=0.7",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1"
            }

            # Limpeza da URL
            url_base = url.split('?')[0]

            response = requests.get(url_base, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Resto do processamento...
            st.success("Dados carregados com sucesso!")

        except requests.exceptions.HTTPError as http_err:
            st.error(f"Erro HTTP: {http_err}")
        except requests.exceptions.RequestException as req_err:
            st.error(f"Erro de conexão: {req_err}")

# Função para calcular o desconto em percentagem
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

# Função para gerar o texto do post
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

# Função para redimensionar imagem
def redimensionar_imagem(imagem_url, largura, altura):
    response = requests.get(imagem_url)
    imagem = Image.open(io.BytesIO(response.content))
    imagem = imagem.resize((largura, altura))
    return imagem

# Função para sobrepor texto na imagem
def sobrepor_texto_na_imagem(imagem, texto):
    draw = ImageDraw.Draw(imagem)
    fonte = ImageFont.load_default()
    largura, altura = imagem.size
    texto_largura, texto_altura = draw.textsize(texto, font=fonte)
    posicao = ((largura - texto_largura) // 2, altura - texto_altura - 20)
    draw.text(posicao, texto, (255, 255, 255), font=fonte)
    return imagem

# Aplicação principal
def auto_post_app():
    st.title("Gerador Automático de Posts")

    # Input para o link de referência
    url = st.text_input("Insira o link de referência para gerar o post automaticamente:")

    if url:
        with st.spinner('Carregando...'):
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    "Accept-Language": "en-US,en;q=0.9,pt;q=0.8",
                }
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')

                # Simulação da extração de dados
                title = soup.find('span', {'id': 'productTitle'}).text.strip() if soup.find('span', {'id': 'productTitle'}) else "Produto Genérico"
                preco_original = 100.0
                preco_atual = 75.0
                imagem_url = "https://via.placeholder.com/1200x628.png?text=Imagem+Produto"
                cupom = "PROMO2023"
                tags = ["desconto", "promoção"]

                # Entrada de dados
                title = st.text_input("Título do produto:", title)
                preco_original = st.number_input("Preço original (€):", value=preco_original, step=0.01)
                preco_atual = st.number_input("Preço atual (€):", value=preco_atual, step=0.01)
                cupom = st.text_input("Cupom:", cupom)
                tags = st.text_input("Tags (separadas por vírgula):", ",".join(tags)).split(",")
                estilo_post = st.radio("Estilo do post:", ["emoji", "formal"], index=0)

                # Gerar e exibir texto do post
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

                # Controle de imagem
                st.write("### Imagem do Produto:")
                imagem_resized = redimensionar_imagem(imagem_url, 1200, 628)
                imagem_final = sobrepor_texto_na_imagem(imagem_resized, f"{calcular_desconto(preco_original, preco_atual)}% OFF")
                st.image(imagem_final, caption="Pré-visualização da Imagem", use_column_width=True)
                buffer = io.BytesIO()
                imagem_final.save(buffer, format="PNG")
                st.download_button("Baixar Imagem", data=buffer.getvalue(), file_name="imagem_produto.png", mime="image/png")

                # Integração com redes sociais (simulado)
                st.write("### Compartilhar:")
                st.button("Compartilhar no Facebook (Simulado)")

            except requests.exceptions.RequestException as e:
                st.error(f"Erro ao processar o link: {e}")
