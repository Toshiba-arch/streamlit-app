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

    # Inicialização do estado da sessão
    if "produto" not in st.session_state:
        st.session_state.produto = {
            "nome": "",
            "preco_original": 0.0,
            "preco_atual": 0.0,
            "cupom": "",
            "imagem_url": "",
        }
    if "produto_validado" not in st.session_state:
        st.session_state.produto_validado = False

    # Entrada para o link de referência
    url_input = st.text_input("Insira o link de referência para gerar o post automaticamente:")
    
    if st.button("Validar Link"):
        with st.spinner("Validando o link e carregando os dados do produto..."):
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    "Accept-Language": "en-US,en;q=0.9,pt;q=0.8",
                }
                response = requests.get(url_input, headers=headers, timeout=15)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')

                # Extração de informações do produto
                nome = soup.find('span', {'id': 'productTitle'}).text.strip() if soup.find('span', {'id': 'productTitle'}) else "Produto Desconhecido"
                preco_original = soup.find('span', {'id': 'priceblock_ourprice'}).text.strip() if soup.find('span', {'id': 'priceblock_ourprice'}) else "0.00"
                preco_atual = soup.find('span', {'id': 'priceblock_dealprice'}).text.strip() if soup.find('span', {'id': 'priceblock_dealprice'}) else preco_original
                imagem_div = soup.find('div', {'class': 'imgTagWrapper'})
                imagem_url = imagem_div.find('img')['src'] if imagem_div and imagem_div.find('img') else ""

                # Atualiza os dados do produto no estado
                st.session_state.produto = {
                    "nome": nome,
                    "preco_original": float(preco_original.replace("€", "").replace(",", ".")) if preco_original else 0.0,
                    "preco_atual": float(preco_atual.replace("€", "").replace(",", ".")) if preco_atual else 0.0,
                    "cupom": "",
                    "imagem_url": imagem_url,
                }
                st.session_state.produto_validado = True
                st.success("Produto validado com sucesso!")
            except requests.exceptions.RequestException as e:
                st.error(f"Erro ao processar o link: {e}")

    # Formulário para inserir os detalhes e gerar o post
    if st.session_state.produto_validado:
        produto = st.session_state.produto

        # Inputs para ajustes manuais
        preco_original = st.number_input("Preço original (€):", value=produto['preco_original'], step=0.01)
        preco_atual = st.number_input("Preço atual (€):", value=produto['preco_atual'], step=0.01)
        cupom = st.text_input("Código de cupom (opcional):", value=produto['cupom'])
        tags_input = st.text_area("Tags (separadas por vírgula):", value="promoção, oferta")

        # Atualiza o estado com os valores manuais
        produto['preco_original'] = preco_original
        produto['preco_atual'] = preco_atual
        produto['cupom'] = cupom

        # Botão para gerar o post
        if st.button("Gerar Post"):
            tags = [tag.strip() for tag in tags_input.split(",")]
            post_texto = gerar_post(produto, url_input, tags)
            
            # Exibe o post
            st.write("### Pré-visualização do Post:")
            st.text_area("Texto do Post:", post_texto, height=200)

            # Botão para download do post
            st.download_button("Baixar Post (.txt)", data=post_texto, file_name="post_gerado.txt")

            # Exibe a imagem redimensionada
            if produto['imagem_url']:
                imagem_resized = redimensionar_imagem(produto['imagem_url'], 1200, 628)
                if imagem_resized:
                    st.image(imagem_resized, caption="Pré-visualização da Imagem", use_container_width=True)
                    buffer = io.BytesIO()
                    imagem_resized.save(buffer, format="PNG")
                    st.download_button("Baixar Imagem", data=buffer.getvalue(), file_name="imagem_produto.png", mime="image/png")
                else:
                    st.error("Não foi possível carregar a imagem para este produto.")

            # Links para compartilhamento
            facebook_url = f"https://www.facebook.com/sharer/sharer.php?u={url_input}"
            st.markdown(f"[Compartilhar no Facebook]({facebook_url})")

            x_text = urllib.parse.quote_plus(f"{produto['nome']} - {url_input}")
            x_url = f"https://twitter.com/intent/tweet?url={url_input}&text={x_text}"
            st.markdown(f"[Compartilhar no X]({x_url})")

            whatsapp_text = urllib.parse.quote_plus(f"{produto['nome']} - {url_input}")
            whatsapp_url = f"https://wa.me/?text={whatsapp_text}"
            st.markdown(f"[Compartilhar no WhatsApp]({whatsapp_url})")

# Executando a aplicação
if __name__ == "__main__":
    auto_post_app()
