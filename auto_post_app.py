import streamlit as st
import requests
from bs4 import BeautifulSoup
from PIL import Image
import io
import urllib.parse

def extrair_dados_produto(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9,pt;q=0.8",
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        center_col = soup.find('div', {'id': 'centerCol'})
        if not center_col:
            return None

        nome = center_col.find('span', {'id': 'productTitle'})
        nome = nome.text.strip() if nome else "Produto Desconhecido"

        preco_original = center_col.find('span', {'class': 'priceBlockStrikePriceString'})
        preco_original = float(preco_original.text.replace("\u20ac", "").replace(",", ".").strip()) if preco_original else 0.0

        preco_atual = center_col.find('span', {'id': 'priceblock_ourprice'}) or center_col.find('span', {'id': 'priceblock_dealprice'})
        preco_atual = float(preco_atual.text.replace("\u20ac", "").replace(",", ".").strip()) if preco_atual else preco_original

        imagem_div = center_col.find('img', {'id': 'landingImage'})
        imagem_url = imagem_div['src'] if imagem_div else ""

        return {
            "nome": nome,
            "preco_original": preco_original,
            "preco_atual": preco_atual,
            "imagem_url": imagem_url,
        }
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao acessar a página do produto: {e}")
        return None
    except Exception as e:
        st.error(f"Erro ao processar os dados do produto: {e}")
        return None

def calcular_desconto(preco_original, preco_atual):
    try:
        if preco_original == 0:
            return 0
        desconto = ((preco_original - preco_atual) / preco_original) * 100
        return round(desconto, 2)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0

def gerar_post(produto, link_referencia, tags):
    nome = produto['nome']
    preco_original = produto['preco_original']
    preco_atual = produto['preco_atual']
    desconto = calcular_desconto(preco_original, preco_atual)

    post_texto = f"\ud83d\udce2 **Oferta Imperd\u00edvel!** \ud83d\udce2\n"
    post_texto += f"\ud83d\udd39 **{nome}**\n"
    post_texto += f"\ud83d\udcb0 Antes **\u20ac{preco_original:.2f}** AGORA **\u20ac{preco_atual:.2f}**!\n"
    post_texto += f"\ud83d\udcc9 Poupa j\u00e1 **{desconto}%**!\n"
    post_texto += f"\ud83d\udc49 [Compra agora]({link_referencia})\n"
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
    st.title("Gerador Autom\u00e1tico de Posts")

    if "produto" not in st.session_state:
        st.session_state.produto = {
            "nome": "",
            "preco_original": 0.0,
            "preco_atual": 0.0,
            "imagem_url": "",
        }

    url_input = st.text_input("Insira o link do produto na Amazon:")

    if st.button("Carregar Dados do Produto"):
        with st.spinner("Carregando dados do produto..."):
            produto = extrair_dados_produto(url_input)
            if produto:
                st.session_state.produto = produto
                st.success("Dados carregados com sucesso!")
            else:
                st.error("Não foi possível extrair os dados do produto.")

    produto = st.session_state.produto
    if produto["nome"]:
        st.text_input("Nome do Produto:", value=produto['nome'], key="nome")
        preco_original = st.number_input("Preço Original (€):", value=produto['preco_original'], step=0.01)
        preco_atual = st.number_input("Preço Atual (€):", value=produto['preco_atual'], step=0.01)
        tags_input = st.text_area("Tags (separadas por vírgula):", value="promoção, oferta")

        produto['preco_original'] = preco_original
        produto['preco_atual'] = preco_atual

        if st.button("Gerar Post"):
            tags = [tag.strip() for tag in tags_input.split(",")]
            post_texto = gerar_post(produto, url_input, tags)

            st.write("### Pré-visualização do Post:")
            st.text_area("Texto do Post:", post_texto, height=200)

            st.download_button("Baixar Post (.txt)", data=post_texto, file_name="post_gerado.txt")

            if produto['imagem_url']:
                imagem_resized = redimensionar_imagem(produto['imagem_url'], 1200, 628)
                if imagem_resized:
                    st.image(imagem_resized, caption="Pré-visualização da Imagem", use_container_width=True)
                    buffer = io.BytesIO()
                    imagem_resized.save(buffer, format="PNG")
                    st.download_button("Baixar Imagem", data=buffer.getvalue(), file_name="imagem_produto.png", mime="image/png")

            facebook_url = f"https://www.facebook.com/sharer/sharer.php?u={url_input}"
            st.markdown(f"[Compartilhar no Facebook]({facebook_url})")

            x_text = urllib.parse.quote_plus(f"{produto['nome']} - {url_input}")
            x_url = f"https://twitter.com/intent/tweet?url={url_input}&text={x_text}"
            st.markdown(f"[Compartilhar no X]({x_url})")

            whatsapp_text = urllib.parse.quote_plus(f"{produto['nome']} - {url_input}")
            whatsapp_url = f"https://wa.me/?text={whatsapp_text}"
            st.markdown(f"[Compartilhar no WhatsApp]({whatsapp_url})")

if __name__ == "__main__":
    auto_post_app()
