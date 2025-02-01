import streamlit as st
import requests
from bs4 import BeautifulSoup
from PIL import Image
import io
import urllib.parse
import time
import random
import re

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
            return response
        except requests.exceptions.RequestException:
            st.warning(f"Tentativa {_+1} falhou. Aguardando 5 segundos...")
            time.sleep(5)
    return None

def extrair_dados_produto(url):
    try:
        response = fetch_with_retry(url)
        if not response:
            return None
            
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extração do título
        nome = soup.find('span', {'id': 'productTitle'})
        nome = nome.get_text(strip=True) if nome else "Produto Desconhecido"

        # Extração de preço
        preco_data = {}
        price_text = soup.find('span', {'class': 'a-price-whole'})
        if price_text:
            preco_data = processar_preco(price_text.get_text())

        # Extração de cupom
        cupom = ""
        coupon_section = soup.find('div', {'id': 'promoPriceBlockMessage'})
        if coupon_section:
            cupom_badge = coupon_section.find('span', {'class': 'couponBadge'})
            if cupom_badge:
                cupom = cupom_badge.get_text(strip=True)

        # Características do produto
        caracteristicas = []
        bullet_points = soup.find('div', {'id': 'feature-bullets'})
        if bullet_points:
            for li in bullet_points.find_all('li'):
                caracteristicas.append(li.get_text(strip=True))

        # Avaliação
        avaliacao = soup.find('span', {'class': 'a-icon-alt'})
        avaliacao = avaliacao.get_text(strip=True).split()[0] if avaliacao else "N/A"

        # Imagem
        imagem_url = ""
        img_container = soup.find('div', {'id': 'imgTagWrapperId'})
        if img_container:
            img = img_container.find('img')
            if img and 'src' in img.attrs:
                imagem_url = img['src']

        return {
            "nome": nome,
            "preco_original": preco_data.get('original', 0),
            "preco_atual": preco_data.get('atual', 0),
            "moeda": "€",
            "cupom": cupom,
            "caracteristicas": caracteristicas,
            "avaliacao": avaliacao,
            "imagem_url": imagem_url,
            "url": url
        }

    except Exception as e:
        st.error(f"Erro crítico: {str(e)}")
        return None

def processar_preco(preco_text):
    try:
        preco_text = preco_text.replace('\xa0', '').replace(',', '.')
        numeros = [float(s) for s in re.findall(r'\d+\.\d+|\d+', preco_text)]
        
        if len(numeros) > 1:
            return {'original': max(numeros), 'atual': min(numeros)}
        elif numeros:
            return {'original': numeros[0], 'atual': numeros[0]}
        return {}
    except:
        return {}

def calcular_desconto(preco_original, preco_atual):
    try:
        if preco_original > 0:
            return round(((preco_original - preco_atual) / preco_original) * 100, 2)
        return 0
    except ZeroDivisionError:
        return 0

def gerar_post(produto, tags):
    post = f"🔥 **Oferta Especial!** 🔥\n\n"
    post += f"📌 **{produto['nome']}**\n\n"

    if produto['avaliacao'] != "N/A":
        post += f"⭐ **Avaliação:** {produto['avaliacao']}/5\n"
    
    post += "\n🚀 **Características Principais:**\n"
    for feature in produto['caracteristicas'][:3]:
        post += f"✔️ {feature}\n"

    post += f"\n💵 **Preço Original:** {produto['moeda']}{produto['preco_original']:.2f}\n"
    post += f"💥 **Preço Atual:** {produto['moeda']}{produto['preco_atual']:.2f}\n"

    desconto = calcular_desconto(produto['preco_original'], produto['preco_atual'])
    if desconto > 0:
        post += f"🎯 **Desconto:** {desconto}% OFF!\n"

    if produto['cupom']:
        post += f"\n🎁 **Cupom de Desconto:** `{produto['cupom']}`\n"

    post += f"\n🛒 [Compre Agora]({produto['url']})\n\n"
    post += " ".join([f"#{tag.strip()}" for tag in tags])

    return post

def auto_post_app():
    st.title("🛍️ Gerador de Ofertas Amazon")

    url = st.text_input("Cole o link do produto Amazon:", "")

    if st.button("Analisar Produto"):
        if not url.startswith(('http', 'www')):
            st.error("Link inválido!")
            return
            
        with st.spinner("🔍 Analisando o produto..."):
            expanded_url = expandir_link(url)
            if not expanded_url:
                return
                
            produto = extrair_dados_produto(expanded_url)
            
            if produto:
                st.session_state.produto = produto
                st.success("✅ Produto analisado com sucesso!")

                if produto['imagem_url']:
                    st.image(produto['imagem_url'], use_column_width=True)

                st.markdown(f"**{produto['nome']}**")
                st.markdown(f"**Preço:** {produto['moeda']}{produto['preco_atual']:.2f}")
                if produto['preco_original'] > produto['preco_atual']:
                    st.markdown(f"~~{produto['moeda']}{produto['preco_original']:.2f}~~")

    if 'produto' in st.session_state:
        tags = st.text_input("Tags para redes sociais (separadas por vírgula):", "oferta, promoção, amazon")

        if st.button("Gerar Post Final"):
            post = gerar_post(st.session_state.produto, tags.split(','))

            st.subheader("📝 Preview do Post")
            st.code(post, language=None)

            texto_share = urllib.parse.quote(post)
            st.markdown(f"[Compartilhar no WhatsApp](https://wa.me/?text={texto_share})")

auto_post_app()
