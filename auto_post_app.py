import streamlit as st
import requests
from bs4 import BeautifulSoup
from time import sleep

# Função para gerar o texto do post
def gerar_post(produto, link_referencia, tags):
    nome = produto['nome']
    preco_original = produto['preco_original']
    preco_atual = produto['preco_atual']
    desconto = produto['desconto']
    cupom = produto['cupom']
    
    # Garantir que os preços sejam números
    try:
        preco_original = float(preco_original.replace('€', '').replace(',', '.')) if preco_original else 0
        preco_atual = float(preco_atual.replace('€', '').replace(',', '.')) if preco_atual else 0
    except ValueError:
        preco_original = preco_atual = 0  # Caso não seja possível converter, atribuímos 0 como padrão

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

def auto_post_app():
    st.write("### Gerador Automático de Posts")

    # Input para o link de referência
    url = st.text_input("Insira o link de referência para gerar o post automaticamente:")

    if url:
        with st.spinner('Carregando...'):
            try:
                # Cabeçalho para emular um navegador e evitar bloqueio
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                }

                # Tentativa de obter o conteúdo da página
                response = requests.get(url, headers=headers)
                response.raise_for_status()  # Levanta uma exceção se o status code não for 200

                # Verificar o conteúdo retornado para depurar
                # print(response.text)  # Descomente para ver o HTML da página

                soup = BeautifulSoup(response.content, 'html.parser')

                # Procurar pela div dp-container onde estão os dados
                dp_container = soup.find('div', {'id': 'dp-container'})
                if dp_container:
                    # Captura o nome do produto
                    title = dp_container.find('span', {'id': 'productTitle'}).text.strip() if dp_container.find('span', {'id': 'productTitle'}) else "Sem título disponível"
                    
                    # Captura a descrição do produto
                    description = dp_container.find('div', {'id': 'productDescription'}).text.strip() if dp_container.find('div', {'id': 'productDescription'}) else "Sem descrição disponível"
                    
                    # Captura o preço
                    price = dp_container.find('span', {'id': 'priceblock_ourprice'}) or dp_container.find('span', {'id': 'priceblock_dealprice'})
                    price = price.text.strip() if price else "Preço não disponível"
                    
                    # Captura o desconto, caso exista
                    discount = "Sem desconto"
                    discount_tag = dp_container.find('span', {'class': 'a-declarative'})
                    if discount_tag:
                        discount = discount_tag.text.strip()

                    # Captura a URL da imagem
                    image_tag = dp_container.find('img', {'id': 'landingImage'})
                    image_url = image_tag['src'] if image_tag and 'src' in image_tag.attrs else ""

                    # Captura o cupom, se disponível
                    coupon = "Sem cupom disponível"
                    coupon_tag = dp_container.find('span', {'class': 'a-declarative'})
                    if coupon_tag:
                        coupon = coupon_tag.text.strip()

                    # Exibição dos dados extraídos
                    st.write("#### Personalize os elementos do post:")
                    title = st.text_input("Título (ex: Nome do Produto):", value=title, key="auto_title")
                    description = st.text_area("Descrição (detalhes do produto):", value=description, key="auto_description", height=100)
                    price = st.text_input("Preço (ex: €199,99):", value=price, key="auto_price")
                    discount = st.text_input("Desconto (ex: 20%):", value=discount, key="auto_discount")
                    coupon = st.text_input("Cupom (ex: CÓDIGO20):", value=coupon, key="auto_coupon")

                    # Campo para URL de imagem
                    if image_url:
                        st.image(image_url, caption="Imagem extraída da Amazon", use_column_width=True)

                    # Tags
                    tags = st.text_input("Tags (separadas por vírgula):", "")

                    # Gerar conteúdo do post
                    produto = {
                        'nome': title,
                        'preco_original': price,
                        'preco_atual': price,
                        'desconto': discount.replace("Desconto: ", "").replace("%", "") if discount != "Sem desconto" else "0",
                        'cupom': coupon if coupon != "Sem cupom disponível" else ""
                    }
                    post_texto = gerar_post(produto, url, tags.split(",") if tags else [])

                    st.write("### Pré-visualização do Post:")
                    st.text_area("Texto do Post para copiar e colar:", value=post_texto, height=200)

                    # Botões para download
                    st.download_button("Baixar Post (.txt)", data=post_texto, file_name="post_automatico.txt")
                
                    # Exportação para Markdown
                    post_md = (
                        f"# {title}\n\n"
                        f"{description}\n\n"
                        f"**Preço:** {price}\n"
                        f"**Desconto:** {discount}\n"
                        f"**Cupom:** {coupon}\n\n"
                        f"**Clique aqui para aproveitar a oferta:** {url}\n\n"
                    )
                    if image_url:
                        post_md += f"![Imagem do Produto]({image_url})\n"
                    st.download_button("Baixar Post (.md)", data=post_md, file_name="post_automatico.md")
                else:
                    st.error("Não foi possível localizar os dados da página.")
            except requests.exceptions.RequestException as e:
                st.error(f"Erro ao processar o link: {e}")
