import streamlit as st
from PIL import Image
import requests
from io import BytesIO

# Configuração da página
title = "Gerador de Conteúdo de Ofertas"
st.set_page_config(page_title=title, layout="wide")

# Função para calcular o desconto
def calcular_desconto(preco_original, preco_atual):
    """
    Calcula a porcentagem de desconto com base no preço original e atual.
    Retorna o desconto arredondado para duas casas decimais.
    """
    if preco_original > preco_atual:
        desconto = ((preco_original - preco_atual) / preco_original) * 100
        return round(desconto, 2)
    return 0

# Função para gerar o texto do post
def gerar_post(produto, link_referencia, tags):
    """
    Gera o texto do post para o anúncio, incluindo informações do produto e tags.
    """
    nome = produto['nome']
    preco_original = produto['preco_original']
    preco_atual = produto['preco_atual']
    desconto = produto['desconto']
    cupom = produto['cupom']

    # Monta o texto principal do post
    post_texto = f"""\
📢 **Oferta Imperdível!** 📢\n
🔹 **{nome}**\n
💰 De **€{preco_original:.2f}** por apenas **€{preco_atual:.2f}**!\n
📉 Economize **{desconto}%**!\n
"""
    if cupom:
        post_texto += f"💥 Use o código de cupom: **{cupom}**\n"

    # Adiciona o link de referência
    post_texto += f"👉 [Compre agora]({link_referencia})\n"

    # Adiciona as tags ao final do post
    if tags:
        post_texto += "\n" + " ".join([f"#{tag}" for tag in tags])

    return post_texto

# Função principal da aplicação
def run():
    """
    Interface principal da aplicação Streamlit para gerar conteúdo de anúncios.
    """
    st.title(title)

    # Entrada para o nome do produto
    nome_produto = st.text_input("Nome do Produto")
    tem_desconto = st.radio("O produto tem desconto?", ('Sim', 'Não'))

    # Entradas condicionais para preços e desconto
    if tem_desconto == 'Sim':
        desconto_percentual = st.number_input("Porcentagem de Desconto (%)", min_value=0.0, step=0.01, format="%.2f")
        preco_atual = st.number_input("Preço Atual (€)", min_value=0.0, step=0.01, format="%.2f")
        preco_original = preco_atual / (1 - desconto_percentual / 100)
    else:
        preco_original = st.number_input("Preço Original (€)", min_value=0.0, step=0.01, format="%.2f")
        preco_atual = st.number_input("Preço Atual (€)", min_value=0.0, step=0.01, format="%.2f")

    # Outras entradas para o anúncio
    cupom = st.text_input("Código de Cupom (se houver)")
    imagem_url = st.text_input("Link da Imagem do Produto")
    link_referencia = st.text_input("Link de Afiliado")

    # Entrada para tags e processamento
    tags = st.text_area("Tags para o Anúncio (separadas por vírgula)").split(",")
    tags = [tag.strip() for tag in tags if tag.strip()]

    # Calcula o desconto com base nos preços
    desconto = calcular_desconto(preco_original, preco_atual)

    # Botão para gerar o post
    if st.button("Gerar Post"):
        if nome_produto and link_referencia and preco_atual and imagem_url:
            # Cria um dicionário com as informações do produto
            produto = {
                "nome": nome_produto,
                "preco_original": preco_original,
                "preco_atual": preco_atual,
                "desconto": desconto,
                "imagem": imagem_url,
                "cupom": cupom
            }

            # Gera o texto do post
            post_texto = gerar_post(produto, link_referencia, tags)

            # Exibe a imagem do produto
            response = requests.get(imagem_url)
            imagem = Image.open(BytesIO(response.content))
            st.image(imagem, caption=f"Imagem de {nome_produto}", use_container_width=False, width=600)

            # Adiciona opção para download da imagem
            img_buffer = BytesIO()
            imagem.save(img_buffer, format="PNG")
            img_buffer.seek(0)
            st.download_button(
                label="Baixar Imagem",
                data=img_buffer,
                file_name=f"{nome_produto.replace(' ', '_')}.png",
                mime="image/png"
            )

            # Exibe o texto do post na interface
            st.text_area("Texto do Post para Compartilhar", post_texto, height=200)

# Executar a aplicação
if __name__ == "__main__":
    run()
