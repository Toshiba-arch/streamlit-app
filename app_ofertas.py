import streamlit as st
from PIL import Image, ImageDraw, ImageFont
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

# Função para gerar imagem com texto sobre o produto
def criar_imagem_com_texto(imagem_url, nome_produto, preco_original, preco_atual, desconto):
    """
    Baixa a imagem do produto de uma URL e adiciona texto sobre o desconto e preço.
    Retorna a imagem modificada.
    """
    # Baixa a imagem a partir da URL fornecida
    response = requests.get(imagem_url)
    imagem = Image.open(BytesIO(response.content)).convert("RGBA")
    draw = ImageDraw.Draw(imagem)

    # Define a fonte para o texto (usa fonte padrão se "arial.ttf" não estiver disponível)
    try:
        font = ImageFont.truetype("arial.ttf", size=36)
        font_bold = ImageFont.truetype("arialbd.ttf", size=40)
    except IOError:
        font = ImageFont.load_default()
        font_bold = font

    # Monta o texto com informações do produto
    texto_nome = f"{nome_produto}"
    texto_preco = f"De €{preco_original:.2f} por €{preco_atual:.2f}"
    texto_desconto = f"-{desconto}%"
    largura, altura = imagem.size

    # Define posições e margens
    margem = 20
    y_texto = margem

    # Adiciona o nome do produto (em negrito)
    draw.text((margem, y_texto), texto_nome, fill="white", font=font_bold, stroke_width=2, stroke_fill="black")
    y_texto += font_bold.getsize(texto_nome)[1] + 10

    # Adiciona o preço atual (em verde)
    draw.text((margem, y_texto), texto_preco, fill="green", font=font, stroke_width=2, stroke_fill="black")
    y_texto += font.getsize(texto_preco)[1] + 10

    # Adiciona o desconto (em vermelho)
    draw.text((margem, y_texto), texto_desconto, fill="red", font=font, stroke_width=2, stroke_fill="black")

    # Redimensiona a imagem para adequar às redes sociais (ex: largura máxima de 800px)
    largura_nova = 800
    proporcao = largura_nova / largura
    nova_altura = int(altura * proporcao)
    imagem = imagem.resize((largura_nova, nova_altura), Image.LANCZOS)

    # Converte para JPEG
    imagem_convertida = Image.new("RGB", imagem.size, (255, 255, 255))
    imagem_convertida.paste(imagem, mask=imagem.split()[3])
    return imagem_convertida

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

            # Gera a imagem com o texto sobre o produto
            imagem_com_texto = criar_imagem_com_texto(imagem_url, nome_produto, preco_original, preco_atual, desconto)
            st.image(imagem_com_texto, caption=f"Oferta de {nome_produto}", use_container_width=False, width=600)

            # Exibe o texto do post na interface
            st.text_area("Texto do Post para Compartilhar", post_texto, height=200)

            # Botão para baixar a imagem gerada
            buffer = BytesIO()
            imagem_com_texto.save(buffer, format="JPEG")
            st.download_button(
                label="Baixar Imagem com Texto",
                data=buffer.getvalue(),
                file_name="oferta.jpg",
                mime="image/jpeg"
            )

# Executar a aplicação
if __name__ == "__main__":
    run()
