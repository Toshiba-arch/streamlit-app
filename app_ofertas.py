import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import random

# Configuração da página
title = "Gerador de Conteúdo de Ofertas"
st.set_page_config(page_title=title, layout="wide")

# Função para calcular o desconto
def calcular_desconto(preco_original, preco_atual):
    if preco_original > preco_atual:
        desconto = ((preco_original - preco_atual) / preco_original) * 100
        return round(desconto, 2)
    return 0

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
        post_texto += f"💥 Use o código de cupom: **{cupom}**\n"
    post_texto += f"👉 [Compra agora]({link_referencia})\n"
    if tags:
        post_texto += "\n" + " ".join([f"#{tag}" for tag in tags])
    return post_texto

# Função para estilizar a imagem
def estilizar_imagem(imagem_url, preco_atual):
    cores_fundo = ["#FFD700", "#87CEEB", "#FFA500", "#90EE90", "#D2B48C", "#ADD8E6"]
    cor_fundo = random.choice(cores_fundo)

    response = requests.get(imagem_url)
    imagem = Image.open(BytesIO(response.content)).convert("RGBA")

    margem = 50
    largura, altura = imagem.size
    nova_largura = largura + 2 * margem
    nova_altura = altura + 2 * margem
    nova_imagem = Image.new("RGBA", (nova_largura, nova_altura), cor_fundo)

    nova_imagem.paste(imagem, (margem, margem), imagem)

    draw = ImageDraw.Draw(nova_imagem)
    try:
        fonte = ImageFont.truetype("arial.ttf", 30)  # Tentar uma fonte mais robusta
    except IOError:
        fonte = ImageFont.load_default()  # Se falhar, usar a fonte padrão
    
    texto_preco = f"€{preco_atual:.2f}"
    tamanho_texto = draw.textbbox((0, 0), texto_preco, font=fonte)
    largura_texto = tamanho_texto[2] - tamanho_texto[0]
    altura_texto = tamanho_texto[3] - tamanho_texto[1]
    padding = 10

    x1 = nova_largura - largura_texto - 2 * padding - margem
    y1 = nova_altura - altura_texto - 2 * padding - margem
    x2 = nova_largura - margem
    y2 = nova_altura - margem

    draw.rectangle([x1, y1, x2, y2], fill="black")
    draw.text((x1 + padding, y1 + padding), texto_preco, fill="white", font=fonte)

    return nova_imagem

# Função principal da aplicação
def run():
    st.title(title)

    nome_produto = st.text_input("Nome do Produto")
    tem_desconto = st.radio("O produto tem desconto?", ('Sim', 'Não'))

    if tem_desconto == 'Sim':
        desconto_percentual = st.number_input("Porcentagem de Desconto (%)", min_value=0.0, step=0.01, format="%.2f")
        preco_atual = st.number_input("Preço Atual (€)", min_value=0.0, step=0.01, format="%.2f")
        preco_original = preco_atual / (1 - desconto_percentual / 100)
    else:
        preco_original = st.number_input("Preço Original (€)", min_value=0.0, step=0.01, format="%.2f")
        preco_atual = st.number_input("Preço Atual (€)", min_value=0.0, step=0.01, format="%.2f")

    cupom = st.text_input("Código de Cupom (se houver)")
    imagem_url = st.text_input("Link da Imagem do Produto")
    link_referencia = st.text_input("Link de Afiliado")

    tags = st.text_area("Tags para o Anúncio (separadas por vírgula)").split(",")
    tags = [tag.strip() for tag in tags if tag.strip()]

    desconto = calcular_desconto(preco_original, preco_atual)

    if st.button("Gerar Post"):
        if nome_produto and link_referencia and preco_atual and imagem_url:
            produto = {
                "nome": nome_produto,
                "preco_original": preco_original,
                "preco_atual": preco_atual,
                "desconto": desconto,
                "imagem": imagem_url,
                "cupom": cupom
            }

            post_texto = gerar_post(produto, link_referencia, tags)
            imagem_estilizada = estilizar_imagem(imagem_url, preco_atual)
            st.image(imagem_estilizada, caption=f"Imagem de {nome_produto}", use_container_width=False, width=600)

            img_buffer = BytesIO()
            imagem_estilizada.save(img_buffer, format="PNG")
            img_buffer.seek(0)
            st.download_button(
                label="Baixar Imagem",
                data=img_buffer,
                file_name=f"{nome_produto.replace(' ', '_')}.png",
                mime="image/png"
            )

            st.text_area("Texto do Post para Compartilhar", post_texto, height=200)

if __name__ == "__main__":
    run()
