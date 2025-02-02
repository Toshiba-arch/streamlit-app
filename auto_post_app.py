import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
from io import BytesIO
import urllib.parse

# Configurações globais
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive"
}

def extrair_preco(texto):
    """Extrai valores numéricos de strings de preço"""
    try:
        return float(re.sub(r'[^\d.,]', '', texto).replace(',', '.'))
    except:
        return 0.0

def extrair_dados_produto(url_afiliado):
    """Função de extração de dados usando o URL original"""
    try:
        response = requests.get(url_afiliado, headers=HEADERS, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extração de dados
        dados = {
            "nome": (soup.find('span', {'id': 'productTitle'}) or soup.find('h1', {'id': 'title'})).get_text(strip=True),
            "preco_original": 0.0,
            "preco_atual": 0.0,
            "cupom": "",
            "url_afiliado": url_afiliado,
            "imagem_url": ""
        }

        # Preços com fallback
        price_selectors = [
            ('priceblock_ourprice', 'priceblock_dealprice'),
            ('a-price-whole', 'a-offscreen'),
            ('apexPriceToPay', 'basisPrice')
        ]
        
        for original, atual in price_selectors:
            original_elem = soup.find('span', {'id': original}) or soup.find('span', {'class': original})
            atual_elem = soup.find('span', {'id': atual}) or soup.find('span', {'class': atual})
            
            if original_elem and atual_elem:
                dados['preco_original'] = extrair_preco(original_elem.text)
                dados['preco_atual'] = extrair_preco(atual_elem.text)
                break

        # Cupom
        coupon_section = soup.find('div', {'id': 'promoPriceBlockMessage'})
        if coupon_section:
            cupom_badge = coupon_section.find('span', {'class': 'couponBadge'})
            dados['cupom'] = cupom_badge.text.strip() if cupom_badge else ""

        # Imagem do produto
        img_container = soup.find('div', {'id': 'imgTagWrapperId'})
        if img_container:
            img = img_container.find('img')
            if img and 'src' in img.attrs:
                dados['imagem_url'] = img['src']
        else:
            main_image = soup.find('img', {'id': 'landingImage'})
            if main_image and 'src' in main_image.attrs:
                dados['imagem_url'] = main_image['src']

        return dados

    except Exception as e:
        st.error(f"Erro na extração de dados: {str(e)}")
        return None

def calcular_desconto(original, atual):
    """Cálculo seguro de desconto"""
    try:
        if original > 0 and atual < original:
            return round(((original - atual) / original) * 100, 2)
        return 0.0
    except ZeroDivisionError:
        return 0.0

def formatar_moeda(valor):
    """Formata valores para exibição monetária"""
    return f"€{valor:,.2f}".replace(',', ' ').replace('.', ',')

def gerar_post(data, tags):
    """Geração de post com formatação copiável"""
    desconto = calcular_desconto(data['preco_original'], data['preco_atual'])
    
    post = []
    post.append(f"🚨🔥 OFERTA RELÂMPAGO! 🔥🚨\n📦 {data['nome']}")
    
    # Linha de preços
    if desconto > 0:
        preco_original_formatado = formatar_moeda(data['preco_original'])
        preco_atual_formatado = formatar_moeda(data['preco_atual'])
        post.append(f"\n💵 ANTES: ~~{preco_original_formatado}~~\n💸 AGORA: {preco_atual_formatado}\n🎉 POUPANÇA {desconto}%!")
    else:
        post.append(f"\n💵 Preço: {formatar_moeda(data['preco_atual'])}")
    
    # Cupom
    if data['cupom']:
        post.append(f"\n🎁 CUPOM para usar no checkout: {data['cupom'].upper()} 🎁")
    
    # Link de afiliado
    post.append(f"\n🛒 Clica no link: {data['url_afiliado']}")
    
    # Hashtags
    post.append("\n📌 " + "  ".join([f"#{tag.strip()}" for tag in tags]))
    
    return "\n".join(post)

def auto_post_app():
    st.title("🛒 Gerador de Posts para Afiliados Pro")
    
    if 'dados_produto' not in st.session_state:
        st.session_state.dados_produto = None
    
    url_afiliado = st.text_input("Cole seu link de afiliado curto:", key="url_input")
    
    if st.button("Carregar Produto"):
        with st.spinner("Analisando produto..."):
            dados = extrair_dados_produto(url_afiliado)
            if dados:
                st.session_state.dados_produto = dados
                st.success("Dados carregados!")
            else:
                st.error("Erro ao carregar dados. Verifique o link ou preencha manualmente.")

    if st.session_state.dados_produto:
        dados = st.session_state.dados_produto
        
        with st.expander("🔧 Editar Detalhes"):
            col1, col2 = st.columns(2)
            with col1:
                dados['preco_original'] = st.number_input("Preço Original:", 
                                                        value=dados['preco_original'],
                                                        min_value=0.0,
                                                        step=0.01)
                
                dados['preco_atual'] = st.number_input("Preço Atual:", 
                                                     value=dados['preco_atual'],
                                                     min_value=0.0,
                                                     step=0.01)
            
            with col2:
                dados['cupom'] = st.text_input("Código do Cupom:", value=dados['cupom'])
                tags = st.text_input("Hashtags (separar por vírgulas):", value="promoção, desconto, amazon, oferta")

        # Seção de imagem do produto
        if dados['imagem_url']:
            st.subheader("📸 Imagem do Produto")
            col1, col2 = st.columns([2, 1])
            with col1:
                st.image(dados['imagem_url'], use_container_width=True)
            
            with col2:
                # Download da imagem
                response = requests.get(dados['imagem_url'])
                if response.status_code == 200:
                    st.download_button(
                        label="⬇️ Baixar Imagem",
                        data=BytesIO(response.content),
                        file_name="produto.jpg",
                        mime="image/jpeg"
                    )
                else:
                    st.warning("Imagem não disponível para download")

        # Inicializa a variável post_gerado para evitar erro
        post_gerado = ""
        #post_gerado = gerar_post(dados, tags.split(','))
        
        # Área copiável
        st.subheader("📋 Post Formatado para Copiar")
        st.text_area("Clique para selecionar e copiar:", 
                    value=post_gerado, 
                    height=250,
                    key="post_area")
        
        # Visualização estilizada
        st.subheader("👀 Pré-visualização do Post")
        preview_html = f"""
        <div style="
            border: 2px solid #e74c3c;
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            background-color: #fff5f5;
            font-family: Arial, sans-serif;
        ">
            {post_gerado.replace('\n', '<br>')}
        </div>
        """
        st.markdown(preview_html, unsafe_allow_html=True)

    # Seção de compartilhamento direto (adicione isto após a pré-visualização)
    st.markdown("---")
    st.subheader("📤 Compartilhar Diretamente")
    
    # Gera o post se os dados do produto existirem
    if st.session_state.dados_produto:
        dados = st.session_state.dados_produto
        post_gerado = gerar_post(dados, tags.split(','))
    
    # Se post_gerado estiver vazio, a seção de compartilhamento não deve ser exibida
    if post_gerado:
        st.markdown("---")
        st.subheader("📤 Compartilhar Diretamente")
    
        # Codificar texto e URL separadamente
        texto_compartilhamento = urllib.parse.quote(post_gerado)
        url_afiliado_encoded = urllib.parse.quote(dados['url_afiliado'])
    
        st.markdown(f"""
        <div style="margin-top: 20px;">
            <a href="https://twitter.com/intent/tweet?text={texto_compartilhamento}&url={url_afiliado_encoded}" target="_blank" style="text-decoration: none;">
                <button style="background-color: #1DA1F2; color: white; padding: 8px 16px; border: none; border-radius: 5px; margin-right: 10px;">
                    🐦 Twitter
                </button>
            </a>
        </div>
        <div style="margin-top: 20px;">   
            <a href="https://www.facebook.com/sharer/sharer.php?u={url_afiliado_encoded}&quote={texto_compartilhamento}" target="_blank" style="text-decoration: none;">
                <button style="background-color: #1877F2; color: white; padding: 8px 16px; border: none; border-radius: 5px; margin-right: 10px;">
                    📘 Facebook
                </button>
            </a>
        </div>
        <div style="margin-top: 20px;">     
            <a href="https://api.whatsapp.com/send?text={texto_compartilhamento}%20{url_afiliado_encoded}" target="_blank" style="text-decoration: none;">
                <button style="background-color: #25D366; color: white; padding: 8px 16px; border: none; border-radius: 5px;">
                    📱 WhatsApp
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    auto_post_app()
