import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import random


# Definir o título antes de usá-lo
title = "Consultor de Promoções"

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
        post_texto += f"💥 Use o código de cupom no checkout: **{cupom}**\n"
    post_texto += f"👉 [Compra agora]({link_referencia})\n"
    if tags:
        post_texto += "\n" + " ".join([f"#{tag}" for tag in tags])
    return post_texto

# Função para estilizar a imagem
def estilizar_imagem(imagem_url, preco_atual, cor_fundo_caixa="#000000", cor_texto="white", tamanho_texto=150, padding=100, texto_caixa=None):
    """
    Estiliza a imagem com uma caixa no canto inferior direito contendo o preço, podendo configurar a cor, texto e tamanho da caixa.
    
    Parâmetros:
    - imagem_url: URL da imagem do produto
    - preco_atual: Preço atual do produto
    - cor_fundo_caixa: Cor do fundo da caixa (padrão: #000000)
    - cor_texto: Cor do texto (padrão: branco)
    - tamanho_texto: Tamanho do texto (padrão: 150)
    - padding: Espaçamento entre o texto e as bordas da caixa (padrão: 100)
    - texto_caixa: Texto que será exibido na caixa (padrão: preço do produto, caso não seja fornecido)
    
    Retorna:
    - nova_imagem: A imagem estilizada
    """
    
    # Escolher uma cor de fundo aleatória (se a cor do fundo não for especificada)
    cores_fundo = ["#FFD700", "#87CEEB", "#FFA500", "#90EE90", "#D2B48C", "#ADD8E6"]
    cor_fundo = random.choice(cores_fundo)

    # Baixar a imagem do produto
    response = requests.get(imagem_url)
    imagem = Image.open(BytesIO(response.content)).convert("RGBA")

    # Margem para o fundo
    margem = 50
    largura, altura = imagem.size
    nova_largura = largura + 2 * margem
    nova_altura = altura + 2 * margem
    
    # Criar uma nova imagem com fundo colorido
    nova_imagem = Image.new("RGBA", (nova_largura, nova_altura), cor_fundo)

    # Centralizar a imagem original no fundo
    pos_x = margem
    pos_y = margem
    nova_imagem.paste(imagem, (pos_x, pos_y), imagem)

    # Desenhar a caixa no canto inferior direito
    draw = ImageDraw.Draw(nova_imagem)
    
    try:
        # Tentativa de carregar uma fonte comum
        fonte = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", tamanho_texto)
    except IOError:
        # Caso a fonte DejaVu não seja encontrada, usa a fonte padrão
        fonte = ImageFont.load_default()

    # Texto da caixa, se não for fornecido, usa o preço atual
    if texto_caixa is None:
        texto_caixa = f"€{preco_atual:.2f}"
   
    # Tamanho do texto
    tamanho_texto = draw.textbbox((0, 0), texto_caixa, font=fonte)
    largura_texto = tamanho_texto[2] - tamanho_texto[0]
    altura_texto = tamanho_texto[3] - tamanho_texto[1]

    # Posições para desenhar a caixa no canto inferior direito
    x1 = nova_largura - largura_texto - padding - margem
    y1 = nova_altura - altura_texto - padding - margem
    x2 = nova_largura - margem
    y2 = nova_altura - margem

    # Desenhar a caixa com a cor configurada
    draw.rectangle([x1, y1, x2, y2], fill=cor_fundo_caixa)

    # Desenhar o texto dentro da caixa
    draw.text((x1 + padding, y1 + padding), texto_caixa, fill=cor_texto, font=fonte)

    return nova_imagem

# Função principal da aplicação
def run():
    st.title(title) 

    nome_produto = st.text_input("Nome do Produto")
    tem_desconto = st.radio("O produto tem desconto?", ('Sim', 'Não'))

    if tem_desconto == 'Sim':
        desconto_percentual = st.number_input("Porcentagem de Desconto (%)", min_value=0.0, step=0.01, format="%.2f")
        preco_original = st.number_input("Preço Original (€)", min_value=0.0, step=0.01, format="%.2f")
        # Calcula o preço com o desconto percentual
        preco_atual = preco_original * (1 - desconto_percentual / 100)
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
                "preco_atual": preco_atual,  # Preço final com desconto
                "desconto": desconto,
                "imagem": imagem_url,
                "cupom": cupom  # Cupom será incluído no post, mas não afeta o preço
            }

            # Gera o texto do post
            post_texto = gerar_post(produto, link_referencia, tags)

            # Se houver um cupom, adiciona a mensagem no lugar correto
            #if cupom:
            #    post_texto += f"\n💥 **Usar o código do cupom no checkout**: {cupom}"

            # Exibe a imagem estilizada
            imagem_estilizada = estilizar_imagem(imagem_url, preco_atual)
            st.image(imagem_estilizada, caption=f"Imagem de {nome_produto}", use_container_width=False, width=600)

            # Permite o download da imagem estilizada
            img_buffer = BytesIO()
            imagem_estilizada.save(img_buffer, format="PNG")
            img_buffer.seek(0)
            st.download_button(
                label="Baixar Imagem",
                data=img_buffer,
                file_name=f"{nome_produto.replace(' ', '_')}.png",
                mime="image/png"
            )

            # Exibe o texto do post
            st.text_area("Texto do Post para Compartilhar", post_texto, height=200)

if __name__ == "__main__":
    run()
