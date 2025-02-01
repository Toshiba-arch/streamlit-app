import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

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
            "url_afiliado": url_afiliado
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
    post.append(f"🔥 {data['nome']}")
    
    # Linha de preços
    if desconto > 0:
        preco_original_formatado = formatar_moeda(data['preco_original'])
        preco_atual_formatado = formatar_moeda(data['preco_atual'])
        post.append(f"~~{preco_original_formatado}~~ ➡️ {preco_atual_formatado} (-{desconto}%)")
    else:
        post.append(f"Preço: {formatar_moeda(data['preco_atual'])}")
    
    # Cupom
    if data['cupom']:
        post.append(f"🎟 Cupom: {data['cupom']}")
    
    # Link de afiliado
    post.append(f"🔗 {data['url_afiliado']}")
    
    # Hashtags
    post.append(" ".join([f"#{tag.strip()}" for tag in tags]))
    
    return "\n".join(post)

def auto_post_app():
    st.title("🛒 Gerador de Posts para Afiliados")
    
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
                tags = st.text_input("Hashtags (separar por vírgulas):", value="promoção, desconto, amazon")

        post_gerado = gerar_post(dados, tags.split(','))
        
        # Área copiável
        st.subheader("📋 Post Formatado para Copiar")
        st.text_area("Clique para selecionar e copiar:", 
                    value=post_gerado, 
                    height=200,
                    key="post_area")
        
        # Visualização estilizada
        st.subheader("👀 Pré-visualização")
        preview_lines = []
        for line in post_gerado.split('\n'):
            if '➡️' in line:
                preview_lines.append(f"<div style='color: #e74c3c; font-weight: bold;'>{line}</div>")
            elif '🎟' in line:
                preview_lines.append(f"<div style='color: #2ecc71;'>{line}</div>")
            else:
                preview_lines.append(f"<div>{line}</div>")
        
        st.markdown("\n".join(preview_lines), unsafe_allow_html=True)

if __name__ == "__main__":
    auto_post_app()
