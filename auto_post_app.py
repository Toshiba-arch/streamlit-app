import streamlit as st
import requests
from bs4 import BeautifulSoup
from PIL import Image
import io
import urllib.parse
import time

# Função para expandir links encurtados
def expandir_link(url_encurtado):
    try:
        response = requests.head(url_encurtado, allow_redirects=True)
        return response.url
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao expandir o link: {e}")
        return None

# Função para extrair dados do produto
def extrair_dados_produto(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9,pt;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Referer": "https://www.amazon.com/",
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extração de dados do produto
        nome = soup.find('span', {'id': 'productTitle'}).text.strip() if soup.find('span', {'id': 'productTitle'}) else "Produto Desconhecido"
        preco_original = (
            soup.find('span', {'id': 'priceblock_ourprice'}) or
            soup.find('span', {'id': 'priceblock_dealprice'}) or
            soup.find('span', {'class': 'a-price a-text-price'})
        )
        preco_original = preco_original.text.strip() if preco_original else "0.00"
        preco_atual = soup.find('span', {'id': 'priceblock_dealprice'}).text.strip() if soup.find('span', {'id': 'priceblock_dealprice'}) else preco_original
        cupom = soup.find('span', {'class': 'couponBadge'})
        cupom = cupom.text.strip() if cupom else ""
        avaliacao = soup.find('span', {'class': 'a-icon-alt'})
        avaliacao = avaliacao.text.strip() if avaliacao else "Sem avaliação"
        num_avaliacoes = soup.find('span', {'id': 'acrCustomerReviewText'})
        num_avaliacoes = num_avaliacoes.text.strip() if num_avaliacoes else "0 avaliações"
        descricao = soup.find('div', {'id': 'productDescription'})
        descricao = descricao.text.strip() if descricao else "Descrição não disponível"
        imagem_div = soup.find('div', {'class': 'imgTagWrapper'})
        imagem_url = imagem_div.find('img')['src'] if imagem_div and imagem_div.find('img') else ""

        return {
            "nome": nome,
            "preco_original": float(preco_original.replace("€", "").replace(",", ".")) if preco_original else 0.0,
            "preco_atual": float(preco_atual.replace("€", "").replace(",", ".")) if preco_atual else 0.0,
            "cupom": cupom,
            "avaliacao": avaliacao,
            "num_avaliacoes": num_avaliacoes,
            "descricao": descricao,
            "imagem_url": imagem_url,
        }
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao acessar a página do produto: {e}")
        return None
    except Exception as e:
        st.error(f"Erro ao processar os dados: {e}")
        return None

# Função para calcular o desconto
def calcular_desconto(preco_original, preco_atual):
    try:
        if preco_original == 0:
            return 0
        desconto = ((preco_original - preco_atual) / preco_original) * 100
        return round(desconto, 2)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0

# Função para gerar o post
def gerar_post(produto, link_referencia, tags):
    nome = produto['nome']
    preco_original = produto['preco_original']
    preco_atual = produto['preco_atual']
    cupom = produto['cupom']
    desconto = calcular_desconto(preco_original, preco_atual)
    avaliacao = produto['avaliacao']
    num_avaliacoes = produto['num_avaliacoes']
    descricao = produto['descricao']

    post_texto = f"📢 **Oferta Imperdível!** 📢\n"
    post_texto += f"🔹 **{nome}**\n"
    post_texto += f"⭐ **Avaliação:** {avaliacao} ({num_avaliacoes})\n"
    post_texto += f"📝 **Descrição:** {descricao}\n"
    post_texto += f"💰 **Preço Original:** €{preco_original:.2f}\n"
    post_texto += f"💥 **Preço Atual:** €{preco_atual:.2f}\n"
    post_texto += f"📉 **Desconto:** {desconto}%\n"
    if cupom:
        post_texto += f"🎟️ **Cupom:** {cupom}\n"
    post_texto += f"👉 [Compre Agora]({link_referencia})\n"
    if tags:
        post_texto += "\n" + " ".join([f"#{tag}" for tag in tags])

    return post_texto

# Função para redimensionar a imagem
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

# Aplicação principal
def auto_post_app():
    st.title("Gerador Automático de Posts")

    # Inicialização do estado da sessão
    if "produto" not in st.session_state:
        st.session_state.produto = {
            "nome": "",
            "preco_original": 0.0,
            "preco_atual": 0.0,
            "cupom": "",
            "avaliacao": "",
            "num_avaliacoes": "",
            "descricao": "",
            "imagem_url": "",
        }
    if "produto_validado" not in st.session_state:
        st.session_state.produto_validado = False

    # Entrada para o link de referência
    url_input = st.text_input("Insira o link de referência para gerar o post automaticamente:")

    if st.button("Validar Link"):
        with st.spinner("Validando o link e carregando os dados do produto..."):
            link_expandido = expandir_link(url_input) if "http" in url_input else url_input
            if link_expandido:
                dados_produto = extrair_dados_produto(link_expandido)
                if dados_produto:
                    st.session_state.produto = dados_produto
                    st.session_state.produto_validado = True
                    st.success("Produto validado com sucesso!")
                else:
                    st.error("Não foi possível extrair os dados do produto.")
            else:
                st.error("Não foi possível expandir o link.")

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
