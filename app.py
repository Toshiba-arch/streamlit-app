import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import requests

# Função para calcular o desconto
def calcular_desconto(preco_original, preco_atual):
    if preco_original > preco_atual:
        desconto = ((preco_original - preco_atual) / preco_original) * 100
        return round(desconto, 2)
    return 0

# Função para criar a imagem com o texto sobreposto
def criar_imagem_com_texto(imagem_url, nome_produto, preco_original, preco_atual, desconto):
    # Baixar a imagem da URL
    response = requests.get(imagem_url)
    
    # Abrir a imagem a partir do conteúdo binário
    imagem = Image.open(io.BytesIO(response.content))
    
    # Definir o texto a ser sobreposto
    texto = f"{nome_produto}\nDe €{preco_original:.2f} por €{preco_atual:.2f}\nDesconto: {desconto}%"
    
    # Definir a posição do texto e o estilo
    draw = ImageDraw.Draw(imagem)
    font = ImageFont.load_default()  # Usando fonte padrão
    largura, altura = imagem.size
    draw.text((largura // 4, altura // 2), texto, font=font, fill=(255, 255, 255))
    
    # Salvar a imagem temporariamente
    img_byte_arr = io.BytesIO()
    imagem.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    return img_byte_arr

# Função para criar o post
def criar_post(produto, link_referencia, imagem_url):
    nome = produto['nome']
    preco_original = produto['preco_original']
    preco_atual = produto['preco_atual']
    desconto = produto['desconto']

    post_text = f"""📢 **Oferta Imperdível!** 📢  
🔹 **{nome}**  
💰 De **€{preco_original:.2f}** por apenas **€{preco_atual:.2f}**!  
📉 Economize **{desconto}%**!  
👉 [Compre agora]({link_referencia})  

🖼️ Veja a imagem do produto: {imagem_url}
        """
    return post_text

# Interface Streamlit
st.title("Gerador de Conteúdo com Ofertas da Amazon")
st.sidebar.header("Configurações")

# Passo 1: Inserir apenas o nome do produto
st.header("Adicionar nome do produto")
nome_produto = st.text_input("Nome do Produto")

# Passo 2: Selecionar se o produto tem desconto
st.header("O produto tem desconto?")
tem_desconto = st.radio("Selecione a opção:", ('Sim', 'Não'))

# Passo 3: Inserir preços e desconto
if tem_desconto == 'Sim':
    st.header("Informar Desconto e Preço Atual")
    desconto_percentual = st.number_input("Porcentagem de Desconto (%)", min_value=0.0, step=0.01, format="%.2f")
    preco_atual = st.number_input("Preço Atual (€)", min_value=0.0, step=0.01, format="%.2f")
    preco_original = preco_atual / (1 - desconto_percentual / 100)  # Cálculo automático do preço original
else:
    st.header("Inserir preços do produto")
    preco_original = st.number_input("Preço Original (€)", min_value=0.0, step=0.01, format="%.2f")
    preco_atual = st.number_input("Preço Atual (€)", min_value=0.0, step=0.01, format="%.2f")

# Cálculo do desconto se o preço original e atual forem inseridos
desconto = 0
if preco_original > 0 and preco_atual < preco_original:
    desconto = calcular_desconto(preco_original, preco_atual)

# Passo 4: Inserir manualmente a imagem
st.header("Inserir Imagem do Produto")
imagem_url = st.text_input("Cole o URL da Imagem do Produto")

# Passo 5: Gerar link com o Site Stripe
st.header("Gerar Link de Afiliado")
st.markdown("Acesse o Site Stripe da Amazon enquanto navega no site da Amazon e copie o link de afiliado gerado.")
link_referencia = st.text_input("Cole aqui o Link de Afiliado gerado pelo Site Stripe")

# Botão para gerar post
if st.button("Gerar Post"):
    if nome_produto and link_referencia and preco_atual and imagem_url:
        produto = {
            "nome": nome_produto,
            "preco_original": preco_original,
            "preco_atual": preco_atual,
            "desconto": desconto,
            "imagem": imagem_url
        }
        
        post_text = criar_post(produto, link_referencia, imagem_url)
        
        # Gerar a imagem com texto sobreposto
        imagem_com_texto = criar_imagem_com_texto(imagem_url, nome_produto, preco_original, preco_atual, desconto)
        
        st.subheader("Post Gerado")
        
        # Exibir imagem e o texto do post
        st.image(imagem_com_texto)
        st.text_area("Copie o texto abaixo para compartilhar nas redes sociais", post_text, height=200)

        st.markdown("""
        **Dica**: Ao copiar o texto gerado e colá-lo no **Facebook**, a imagem com o texto sobreposto será visualizada junto com o link clicável. 
        Certifique-se de que a imagem esteja hospedada publicamente (em um serviço como Imgur ou Google Drive) para que a visualização funcione corretamente.
        """)

    else:
        st.error("Por favor, insira todos os detalhes do produto e o link de afiliado.")
