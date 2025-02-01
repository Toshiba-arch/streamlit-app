import streamlit as st
import requests
from bs4 import BeautifulSoup
from PIL import Image
import io
import urllib.parse
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
            "avaliacao": "Sem avaliação",
            "num_avaliacoes": "0 avaliações",
            "descricao": "Descrição não disponível",
            "imagem_url": "",
            "url_afiliado": url_afiliado  # Mantemos o URL original
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

        # Resto da extração mantido igual...
        # ... (mantenha o restante da função igual)

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

def gerar_post(data, tags):
    """Geração de post usando o URL de afiliado original"""
    desconto = calcular_desconto(data['preco_original'], data['preco_atual'])
    
    post = f"🔥 **{data['nome']}**\n\n"
    post += f"⭐ {data['avaliacao']}/5 ({data['num_avaliacoes']})\n"
    
    if data['preco_original'] > data['preco_atual']:
        post += f"~~€{data['preco_original']:.2f}~~ ➡️ **€{data['preco_atual']:.2f}** "
        post += f"({desconto}% OFF!)\n\n"
    else:
        post += f"**Preço: €{data['preco_atual']:.2f}**\n\n"
    
    if data['cupom']:
        post += f"🎟️ **Cupom:** `{data['cupom']}`\n\n"
    
    post += f"📌 {data['descricao']}\n\n"
    post += f"🛒 [COMPRAR AGORA]({data['url_afiliado']})\n\n"
    post += " ".join([f"#{tag.strip()}" for tag in tags])
    
    return post

def interface_usuario():
    st.title("🛒 Gerador de Posts para Afiliados")
    
    # Gerenciamento de estado
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
        
        # Seção de edição manual
        with st.expander("🔧 Editar Detalhes do Produto"):
            dados['preco_original'] = st.number_input("Preço Original (€):", 
                                                    value=dados['preco_original'],
                                                    min_value=0.0,
                                                    step=0.01)
            
            dados['preco_atual'] = st.number_input("Preço Atual (€):", 
                                                 value=dados['preco_atual'],
                                                 min_value=0.0,
                                                 step=0.01)
            
            dados['cupom'] = st.text_input("Código do Cupom:", value=dados['cupom'])
            tags = st.text_area("Tags (separar por vírgulas):", value="promoção, desconto, amazon")

        # Visualização do post
        st.divider()
        st.subheader("Pré-visualização do Post")
        
        if dados['imagem_url']:
            try:
                response = requests.get(dados['imagem_url'], timeout=10)
                imagem = Image.open(io.BytesIO(response.content))
                st.image(imagem, use_column_width=True)
            except:
                st.warning("Não foi possível carregar a imagem")
        
        post_gerado = gerar_post(dados, tags.split(','))
        st.markdown(post_gerado)
        
        # Opções de exportação
        st.download_button("📥 Baixar Post", post_gerado, file_name="post_afiliado.txt")
        
        # Compartilhamento direto
        st.markdown("**Compartilhar:**")
        texto_compartilhamento = urllib.parse.quote(post_gerado)
        st.markdown(f"""
        [Twitter](https://twitter.com/intent/tweet?text={texto_compartilhamento}) | 
        [Facebook](https://www.facebook.com/sharer/sharer.php?u={dados['url_afiliado']}) | 
        [WhatsApp](https://wa.me/?text={texto_compartilhamento})
        """)

if __name__ == "__main__":
    interface_usuario()
