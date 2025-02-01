import streamlit as st
import requests
from bs4 import BeautifulSoup
from PIL import Image
import io
import urllib.parse
import time
import random
import re

def ():
    st.title("\U0001F6CD️ Gerador de Ofertas Amazon")

# Configurações globais
HEADERS_LIST = [
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": "https://www.google.com/",
    },
    {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15",
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }
]

def get_random_headers():
    return random.choice(HEADERS_LIST)

def expandir_link(url_encurtado):
    try:
        response = requests.head(url_encurtado, headers=get_random_headers(), allow_redirects=True, timeout=10)
        return response.url
    except Exception as e:
        st.error(f"Erro ao expandir link: {str(e)}")
        return None

def fetch_with_retry(url, max_retries=3):
    for _ in range(max_retries):
        try:
            response = requests.get(url, headers=get_random_headers(), timeout=15)
            response.raise_for_status()
            
            if "Parece que você está offline" in response.text:
                raise requests.exceptions.RequestException("Bloqueio detectado pela Amazon")
                
            return response
        except requests.exceptions.RequestException as e:
            time.sleep(5)
    return None

def processar_preco(preco_text):
    try:
        preco_text = preco_text.replace('\xa0', '').replace(',', '.').strip()
        numeros = [float(s) for s in re.findall(r'\d+\.\d+|\d+', preco_text)]
        
        if len(numeros) == 0:
            return {'original': 0.0, 'atual': 0.0}
        
        if len(numeros) > 1:
            return {
                'original': max(numeros),
                'atual': min(numeros) if min(numeros) > 0 else max(numeros)
            }
        else:
            return {'original': numeros[0], 'atual': numeros[0]}
        
    except:
        return {'original': 0.0, 'atual': 0.0}

def extrair_dados_produto(url):
    try:
        response = fetch_with_retry(url)
        if not response:
            return None
            
        soup = BeautifulSoup(response.content, 'html.parser')
        
        nome = soup.find('span', {'id': 'productTitle'}) or soup.find('h1', {'id': 'title'})
        nome = nome.get_text(strip=True) if nome else "Produto Desconhecido"

        # Extração de preços
        preco_data = {'original': 0.0, 'atual': 0.0}
        price_selectors = [
            ('span', {'id': 'priceblock_ourprice'}),
            ('span', {'id': 'priceblock_dealprice'}),
            ('span', {'class': 'a-price-whole'}),
            ('span', {'class': 'a-offscreen'})
        ]
        
        for tag, attrs in price_selectors:
            element = soup.find(tag, attrs)
            if element:
                preco_text = element.get_text(strip=True)
                preco_data = processar_preco(preco_text)
                break

        # Demais extrações
        cupom = ""
        coupon_section = soup.find('div', {'id': 'promoPriceBlockMessage'})
        if coupon_section:
            cupom_badge = coupon_section.find('span', {'class': 'couponBadge'})
            if cupom_badge:
                cupom = cupom_badge.get_text(strip=True)

        moeda_symbol = soup.find('span', {'class': 'a-price-symbol'})
        moeda = moeda_symbol.get_text(strip=True) if moeda_symbol else "€"

        caracteristicas = []
        bullet_points = soup.find('div', {'id': 'feature-bullets'})
        if bullet_points:
            for li in bullet_points.find_all('li'):
                caracteristicas.append(li.get_text(strip=True))

        avaliacao = soup.find('span', {'class': 'a-icon-alt'})
        avaliacao = avaliacao.get_text(strip=True).split()[0] if avaliacao else "N/A"

        imagem_url = ""
        img_container = soup.find('div', {'id': 'imgTagWrapperId'})
        if img_container:
            img = img_container.find('img')
            if img and 'src' in img.attrs:
                imagem_url = img['src']

        return {
            "nome": nome,
            "preco_original": preco_data['original'],
            "preco_atual": preco_data['atual'],
            "moeda": moeda,
            "cupom": cupom,
            "caracteristicas": caracteristicas,
            "avaliacao": avaliacao,
            "imagem_url": imagem_url
        }

    except Exception as e:
        st.error(f"Erro crítico: {str(e)}")
        return None

def gerar_post(produto, tags, url_afiliado):
    post = f"🔥 **Oferta Especial!** 🔥\n\n"
    post += f"📌 **{produto['nome']}**\n\n"
    
    if produto['avaliacao'] != "N/A":
        post += f"⭐ **Avaliação:** {produto['avaliacao']}/5\n"
    
    if produto['caracteristicas']:
        post += "\n🚀 **Características Principais:**\n"
        for feature in produto['caracteristicas'][:3]:
            post += f"✔️ {feature}\n"
    
    # Preços
    if produto['preco_original'] > 0 and produto['preco_original'] > produto['preco_atual']:
        post += f"\n💵 **Preço Original:** {produto['moeda']}{produto['preco_original']:.2f}"
        post += f"\n💥 **Preço Atual:** {produto['moeda']}{produto['preco_atual']:.2f}"
        
        try:
            desconto = ((produto['preco_original'] - produto['preco_atual'])/produto['preco_original'])*100
            post += f" (⬇️ {desconto:.0f}% de desconto!)\n"
        except ZeroDivisionError:
            post += "\n"
    else:
        post += f"\n💰 **Preço Atual:** {produto['moeda']}{produto['preco_atual']:.2f}\n"
    
    if produto['cupom']:
        post += f"\n🎟️ **Cupom de Desconto:** `{produto['cupom']}`\n"
    
    post += f"\n🛒 [Compre Agora]({url_afiliado}) 🔗\n\n"
    post += " ".join([f"#{tag.strip()}" for tag in tags])
    
    return post

def main():
    st.title("🛍️ Gerador de Posts para Afiliados Amazon")
    
    # Inicializar estado da sessão
    if 'produto' not in st.session_state:
        st.session_state.produto = None
    if 'url_afiliado' not in st.session_state:
        st.session_state.url_afiliado = ""
    
    # Entrada do URL
    url_input = st.text_input("Cole seu link de afiliado Amazon:", value=st.session_state.url_afiliado)
    
    if st.button("Validar Link"):
        with st.spinner("Analisando produto..."):
            expanded_url = expandir_link(url_input) if url_input.startswith(('http', 'www')) else url_input
            st.session_state.url_afiliado = url_input  # Guarda o URL original de afiliado
            
            if expanded_url:
                produto = extrair_dados_produto(expanded_url)
                if produto:
                    st.session_state.produto = produto
                    st.success("Dados do produto carregados!")
                else:
                    st.error("Não foi possível extrair dados automaticamente. Preencha manualmente abaixo.")
            else:
                st.error("Link inválido ou não pôde ser expandido.")

    # Seção de edição manual
    if st.session_state.produto:
        st.divider()
        st.subheader("Editar Informações do Produto")
        
        col1, col2 = st.columns(2)
        with col1:
            novo_preco_original = st.number_input("Preço Original:", 
                                                value=st.session_state.produto['preco_original'],
                                                min_value=0.0,
                                                step=0.01)
            
            novo_preco_atual = st.number_input("Preço Atual:", 
                                             value=st.session_state.produto['preco_atual'],
                                             min_value=0.0,
                                             step=0.01)
            
            novo_cupom = st.text_input("Cupom de Desconto:", 
                                     value=st.session_state.produto['cupom'])
        
        with col2:
            novas_tags = st.text_area("Tags (separadas por vírgula):", 
                                    value="promoção, oferta, amazon")
            
            nova_imagem = st.text_input("URL da Imagem (opcional):", 
                                      value=st.session_state.produto['imagem_url'])
        
        # Atualizar dados
        st.session_state.produto.update({
            'preco_original': novo_preco_original,
            'preco_atual': novo_preco_atual,
            'cupom': novo_cupom,
            'imagem_url': nova_imagem
        })
        
        # Gerar preview
        st.divider()
        st.subheader("Pré-visualização do Post")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.session_state.produto['imagem_url']:
                st.image(st.session_state.produto['imagem_url'], use_column_width=True)
        
        with col2:
            st.markdown(f"**Nome:** {st.session_state.produto['nome']}")
            st.markdown(f"**Preço Atual:** {st.session_state.produto['moeda']}{st.session_state.produto['preco_atual']:.2f}")
            if st.session_state.produto['preco_original'] > st.session_state.produto['preco_atual']:
                st.markdown(f"~~{st.session_state.produto['moeda']}{st.session_state.produto['preco_original']:.2f}~~")
            st.markdown(f"**Avaliação:** {st.session_state.produto['avaliacao']}/5")
        
        # Gerar post final
        if st.button("Gerar Post Final"):
            post = gerar_post(st.session_state.produto, novas_tags.split(','), st.session_state.url_afiliado)
            
            st.code(post, language=None)
            
            # Botões de download
            col1, col2 = st.columns(2)
            with col1:
                st.download_button("Baixar Texto", post, file_name="post_afiliado.txt")
            with col2:
                if st.session_state.produto['imagem_url']:
                    st.download_button("Baixar Imagem", 
                                     requests.get(st.session_state.produto['imagem_url']).content,
                                     file_name="imagem_produto.jpg")
            
            # Compartilhamento
            st.markdown("**Compartilhar:**")
            texto_share = urllib.parse.quote(post)
            st.markdown(f"""
            [Twitter](https://twitter.com/intent/tweet?text={texto_share}) | 
            [Facebook](https://www.facebook.com/sharer/sharer.php?u={st.session_state.url_afiliado}) | 
            [WhatsApp](https://wa.me/?text={texto_share})
            """)

if __name__ == "__main__":
    main()
