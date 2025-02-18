import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
from io import BytesIO
import urllib.parse

# Configurações globais
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1"
}

def extrair_preco(texto):
    """Extrai valores numéricos de strings de preço"""
    try:
        return float(re.sub(r'[^\d.,]', '', texto).replace(',', '.'))
    except:
        return 0.0

def extrair_dados_produto(url_afiliado):
    """Função melhorada com seletores atualizados para Amazon ES"""
    try:
        response = requests.get(url_afiliado, headers=HEADERS, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extração do título
        title = soup.find('span', {'id': 'productTitle'}) or soup.find('h1', {'class': 'a-size-large a-spacing-none'})
        title = title.get_text(strip=True) if title else "Produto sem nome"

        # Extração de preços
        price_wrapper = soup.find('div', {'class': 'a-section a-spacing-none aok-align-center'})
        preco_atual = 0.0
        preco_original = 0.0

        if price_wrapper:
            current_price = price_wrapper.find('span', {'class': 'a-price-whole'})
            if current_price:
                preco_atual = extrair_preco(current_price.get_text())
            
            original_price = price_wrapper.find('span', {'class': 'a-price a-text-price'})
            if original_price:
                preco_original = extrair_preco(original_price.find('span', {'class': 'a-offscreen'}).get_text())

        # Extração de imagens
        image_urls = []
        image_thumbs = soup.select('li.imageThumbnail img')
        for img in image_thumbs:
            if 'src' in img.attrs:
                high_res_url = img['src'].replace('_SL36_', '_SL500_')
                image_urls.append(high_res_url)

        if not image_urls:
            main_image = soup.find('img', {'id': 'landingImage'})
            if main_image and 'src' in main_image.attrs:
                image_urls.append(main_image['src'])

        # Extração de cupons
        cupom = ""
        coupon_badge = soup.find('span', {'class': 'a-size-base a-color-success'})
        if coupon_badge and 'cupón' in coupon_badge.text.lower():
            cupom = coupon_badge.find_next('span').get_text(strip=True)

        return {
            "nome": title,
            "preco_original": preco_original,
            "preco_atual": preco_atual,
            "cupom": cupom,
            "url_afiliado": url_afiliado,
            "imagens_url": image_urls
        }

    except Exception as e:
        st.error(f"Erro na extração: {str(e)}")
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
    
    if desconto > 0:
        preco_original_formatado = formatar_moeda(data['preco_original'])
        preco_atual_formatado = formatar_moeda(data['preco_atual'])
        post.append(f"\n💵 Preço anterior: ~~{preco_original_formatado}~~\n💸 AGORA: {preco_atual_formatado}\n🎉 POUPAS: {desconto}%!")
    else:
        post.append(f"\n💵 Preço: {formatar_moeda(data['preco_atual'])}")
    
    if data['cupom']:
        post.append(f"\n🎁 CUPOM para usar no checkout: {data['cupom'].upper()} 🎁")
    
    post.append(f"\n🛒 Clica no link: {data['url_afiliado']}")
    post.append("\n📌 " + "  ".join([f"#{tag.strip()}" for tag in tags]))
    
    return "\n".join(post)

def auto_post_app():
    st.title("🛒 Gerador de Posts para Afiliados")
    
    # Inicialização de estados
    if 'dados_produto' not in st.session_state:
        st.session_state.dados_produto = None
    if 'selected_images' not in st.session_state:
        st.session_state.selected_images = []
    if 'temp_data' not in st.session_state:
        st.session_state.temp_data = {}

    url_afiliado = st.text_input("URL Amazon de afiliado:", key="url_input")
    
    if st.button("Carregar Produto"):
        with st.spinner("A extrair dados..."):
            dados = extrair_dados_produto(url_afiliado)
            if dados:
                st.session_state.dados_produto = dados
                st.session_state.temp_data = dados.copy()
                st.session_state.selected_images = dados['imagens_url'][:1]
                st.success("Dados carregados!")
            else:
                st.error("Erro ao carregar dados. Verifique o link ou preencha manualmente.")

    if st.session_state.dados_produto:
        dados = st.session_state.dados_produto
        
        with st.expander("🔧 Editar Detalhes", expanded=True):
            with st.form(key='edit_form'):
                col1, col2 = st.columns(2)
                with col1:
                    novo_titulo = st.text_input("Título:", 
                                             value=st.session_state.temp_data.get('nome', ''), 
                                             key='edit_title')
                    
                    novo_preco_original = st.number_input("Preço Original:", 
                                                       value=st.session_state.temp_data.get('preco_original', 0.0),
                                                       min_value=0.0,
                                                       step=0.01,
                                                       key='edit_original')
                    
                    novo_preco_atual = st.number_input("Preço Atual:", 
                                                    value=st.session_state.temp_data.get('preco_atual', 0.0),
                                                    min_value=0.0,
                                                    step=0.01,
                                                    key='edit_atual')
                
                with col2:
                    novo_cupom = st.text_input("Código do Cupom:", 
                                            value=st.session_state.temp_data.get('cupom', ''), 
                                            key='edit_cupom')
                    
                    # Dropdown multiselect para hashtags
                    tags_populares = [
                        "promoção", "desconto", "oferta", "amazon", "preço", "superdesconto", "shopping", 
                        "vendas", "tech", "eletrônicos", "gadgets", "livros", "roupas", "sapatos"
                    ]
                    
                    novas_tags = st.multiselect("Selecione as Hashtags populares:", 
                                               options=tags_populares, 
                                               default=["promoção", "desconto"], 
                                               key='edit_tags')

                # Botão para submissão do formulário
                if st.form_submit_button("💾 Atualizar Dados"):
                    st.session_state.dados_produto.update({
                        'nome': novo_titulo,
                        'preco_original': novo_preco_original,
                        'preco_atual': novo_preco_atual,
                        'cupom': novo_cupom
                    })
                    st.success("Dados atualizados!")

        # Seção de imagens
        if dados['imagens_url']:
            st.subheader("📸 Imagem do Produto")
            
            # Exibe apenas a primeira imagem em tamanho reduzido
            img_url = dados['imagens_url'][0]
            st.image(img_url, width=300)  # Tamanho reduzido da imagem
            
            # Seleção de imagem (apenas uma, pois só há uma disponível)
            if st.checkbox("Selecionar Imagem", 
                           key="img_select", 
                           value=img_url in st.session_state.selected_images):
                st.session_state.selected_images = [img_url]
            else:
                st.session_state.selected_images = []
        
        if st.session_state.selected_images:
            st.subheader("🖼️ Imagem Selecionada para Edição")
            
            # Exibe a imagem selecionada em tamanho menor com botão de download
            img_url = st.session_state.selected_images[0]
            st.image(img_url, width=300)
            
            # Botão de download da imagem
            response = requests.get(img_url)
            if response.status_code == 200:
                img_data = response.content
                st.download_button(
                    label="📥 Fazer Download da Imagem",
                    data=img_data,
                    file_name="imagem_produto.png",
                    mime="image/png"
                )
            
            # Botão para abrir o editor
            if st.button("🖌️ Editar Imagem", key="edit_img"):
                st.session_state.img_url_edicao = img_url
                st.session_state.img_url_download = img_url

        st.subheader("💬 Gerar Post")
        if st.button("Gerar Post"):
            if dados:
                post = gerar_post(dados, novas_tags)
                st.text_area("Post Gerado", post, height=300)
                st.download_button("📥 Baixar Post", post, "post.txt")                            

        # Geração do post
        tags = novas_tags
        post_gerado = gerar_post(st.session_state.dados_produto, tags)

        st.subheader("📋 Post Formatado para Copiar")
        st.text_area("Clique para selecionar e copiar:", 
                   value=post_gerado, 
                   height=250,
                   key="post_area")
        
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

        # Compartilhamento
        st.markdown("---")
        st.subheader("📤 Partilhar Diretamente Por:")
    
        texto_compartilhamento = urllib.parse.quote(post_gerado)
        url_afiliado_encoded = urllib.parse.quote(dados['url_afiliado'])
        url_da_imagem = urllib.parse.quote(st.session_state.selected_images[0]) if st.session_state.selected_images else ""
    
        st.markdown(f"""
            <div style="margin-top: 20px;">
                <a href="https://twitter.com/intent/tweet?text={texto_compartilhamento}&url={url_afiliado_encoded}" target="_blank">
                    <button style="background-color: #1DA1F2; color: white; padding: 8px 16px; border: none; border-radius: 5px; margin-right: 10px;">
                        🐦 Twitter
                    </button>
                </a>
                <a href="https://www.facebook.com/sharer/sharer.php?u={url_afiliado_encoded}&quote={texto_compartilhamento}" target="_blank">
                    <button style="background-color: #1877F2; color: white; padding: 8px 16px; border: none; border-radius: 5px; margin-right: 10px;">
                        📘 Facebook
                    </button>
                </a>
                <a href="https://api.whatsapp.com/send?text={texto_compartilhamento}%20{url_afiliado_encoded}" target="_blank">
                    <button style="background-color: #25D366; color: white; padding: 8px 16px; border: none; border-radius: 5px; margin-right: 10px;">
                        📱 WhatsApp
                    </button>
                </a>
                <a href="https://www.pinterest.com/pin/create/button/?url={url_afiliado_encoded}&description={texto_compartilhamento}&media={url_da_imagem}" target="_blank">
                    <button style="background-color: #BD081C; color: white; padding: 8px 16px; border: none; border-radius: 5px;">
                        📌 Pinterest
                    </button>
                </a>
            </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    auto_post_app()
