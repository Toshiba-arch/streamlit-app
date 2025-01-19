import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import os

# Configuração da página deve ser o PRIMEIRO comando Streamlit no script
st.set_page_config(page_title="Gerador de Conteúdo de Ofertas", layout="wide")

# Verifica e aplica o CSS, se disponível
if os.path.exists("styles.css"):
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
else:
    st.warning("O arquivo 'styles.css' não foi encontrado. Estilos personalizados não serão aplicados.")

# Função para calcular o desconto
def calcular_desconto(preco_original, preco_atual):
    if preco_original > preco_atual:
        desconto = ((preco_original - preco_atual) / preco_original) * 100
        return round(desconto, 2)
    return 0

# Função para criar imagem com texto
def criar_imagem_com_texto(imagem_url, nome_produto, preco_original, preco_atual, desconto):
    response = requests.get(imagem_url)
    imagem = Image.open(BytesIO(response.content)).convert("RGBA")
    draw = ImageDraw.Draw(imagem)

    # Fontes padrão caso Arial não esteja disponível
    try:
        font = ImageFont.truetype("arial.ttf", size=36)
        font_bold = ImageFont.truetype("arialbd.ttf", size=40)
    except IOError:
        font = ImageFont.load_default()
        font_bold = font

    # Texto sobre o produto
    texto_nome = f"{nome_produto}"
    texto_preco = f"De €{preco_original:.2f} por €{preco_atual:.2f}"
    texto_desconto = f"-{desconto}%"
    largura, altura = imagem.size

    # Margens e posições
    margem = 20
    y_texto = margem

    # Adiciona textos à imagem
    draw.text((margem, y_texto), texto_nome, fill="white", font=font_bold, stroke_width=2, stroke_fill="black")
    y_texto += font_bold.getsize(texto_nome)[1] + 10
    draw.text((margem, y_texto), texto_preco, fill="green", font=font, stroke_width=2, stroke_fill="black")
    y_texto += font.getsize(texto_preco)[1] + 10
    draw.text((margem, y_texto), texto_desconto, fill="red", font=font, stroke_width=2, stroke_fill="black")

    # Ajusta o tamanho da imagem para redes sociais
    largura_nova = 800
    proporcao = largura_nova / largura
    nova_altura = int(altura * proporcao)
    imagem = imagem.resize((largura_nova, nova_altura), Image.LANCZOS)

    # Converte para JPEG
    imagem_convertida = Image.new("RGB", imagem.size, (255, 255, 255))
    imagem_convertida.paste(imagem, mask=imagem.split()[3])
    return imagem_convertida

# Função para gerar texto do post
def gerar_post(produto, link_referencia, tags):
    nome = produto['nome']
    preco_original = produto['preco_original']
    preco_atual = produto['preco_atual']
    desconto = produto['desconto']
    cupom = produto['cupom']

    # Texto principal
    post_texto = f"""\
📢 **Oferta Imperdível!** 📢\n
🔹 **{nome}**\n
💰 De **€{preco_original:.2f}** por apenas **€{preco_atual:.2f}**!\n
📉 Economize **{desconto}%**!\n
"""
    if cupom:
        post_texto += f"💥 Use o código de cupom: **{cupom}**\n"
    post_texto += f"👉 [Compre agora]({link_referencia})\n"

    # Adiciona tags
    if tags:
        post_texto += "\n" + " ".join([f"#{tag}" for tag in tags])
    return post_texto

# Função principal
def run():
    # Declaração explícita do título
    titulo = "Gerador de Conteúdo de Ofertas"
    st.title(titulo)

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
            imagem_com_texto = criar_imagem_com_texto(imagem_url, nome_produto, preco_original, preco_atual, desconto)
            st.image(imagem_com_texto, caption=f"Oferta de {nome_produto}", use_container_width=False, width=600)

            st.text_area("Texto do Post para Compartilhar", post_texto, height=200)

            buffer = BytesIO()
            imagem_com_texto.save(buffer, format="JPEG")
            st.download_button(
                label="Baixar Imagem com Texto",
                data=buffer.getvalue(),
                file_name="oferta.jpg",
                mime="image/jpeg"
            )

# Executa a aplicação
if __name__ == "__main__":
    run()
