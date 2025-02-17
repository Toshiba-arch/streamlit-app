import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import urllib.parse
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

# Configurações globais
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "es-ES,es;q=0.9",
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
    post = [f"🚨🔥 OFERTA RELÂMPAGO! 🔥🚨\n📦 {data['nome']}"]
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

def adicionar_overlay(imagem_bytes, texto, posicao=(20,20), font_size=32):
    """Adiciona sobreposição de texto à imagem usando Pillow"""
    imagem = Image.open(BytesIO(imagem_bytes)).convert("RGBA")
    txt = Image.new("RGBA", imagem.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()
    draw.text(posicao, texto, font=font, fill=(255, 0, 0, 255))
    imagem_editada = Image.alpha_composite(imagem, txt)
    output = BytesIO()
    imagem_editada.save(output, format="PNG")
    return output.getvalue()

def auto_post_app():
    st.title("🛒 Gerador de Posts para Afiliados")
    
    # Inicialização de estados
    if 'dados_produto' not in st.session_state:
        st.session_state.dados_produto = None
    if 'selected_images' not in st.session_state:
        st.session_state.selected_images = []
    if 'temp_data' not in st.session_state:
        st.session_state.temp_data = {}
    if 'img_url_edicao' not in st.session_state:
        st.session_state.img_url_edicao = None

    # Entrada do URL de afiliado
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

    # Trending hashtags simuladas
    trending_tags = ["oferta", "desconto", "promoção", "Amazon", "economize", "compreagora"]
    st.markdown("### Trending Hashtags")
    tags_trending = st.multiselect("Selecione hashtags trending:", trending_tags)
    
    # Hashtags adicionais inseridas pelo usuário
    novas_tags = st.text_input("Hashtags adicionais (separar por vírgulas):", value="promoção, desconto, amazon, oferta", key='edit_tags')

    if st.session_state.dados_produto:
        dados = st.session_state.dados_produto
        
        # Seção de imagem
        if dados['imagens_url']:
            st.subheader("📸 Imagem do Produto")
            img_url = dados['imagens_url'][0]
            st.image(img_url, width=300)
            # Checkbox para selecionar a imagem (única)
            if st.checkbox("Selecionar Imagem", key="img_select", value=img_url in st.session_state.selected_images):
                st.session_state.selected_images = [img_url]
            else:
                st.session_state.selected_images = []

        if st.session_state.selected_images:
            st.subheader("🖼️ Imagem Selecionada para Edição")
            img_url = st.session_state.selected_images[0]
            st.image(img_url, width=300)
            # Botão para download da imagem original
            response = requests.get(img_url)
            if response.status_code == 200:
                st.download_button(
                    label="📥 Fazer Download da Imagem Original",
                    data=response.content,
                    file_name="imagem_produto.png",
                    mime="image/png"
                )
            # Seção para sobreposição de texto
            overlay_text = st.text_input("Texto para sobreposição (ex: Desconto 20%)", value="")
            if overlay_text and st.button("Aplicar Sobreposição"):
                imagem_editada = adicionar_overlay(response.content, overlay_text, posicao=(20,20), font_size=32)
                st.image(imagem_editada, width=300)
                st.download_button(
                    label="📥 Fazer Download da Imagem Editada",
                    data=imagem_editada,
                    file_name="imagem_editada.png",
                    mime="image/png"
                )
            # Botão para abrir o editor (Photopea)
            if st.button("🖌️ Editar Imagem", key="edit_img"):
                st.session_state.img_url_edicao = img_url

            if st.session_state.img_url_edicao:
                st.subheader("🖌️ Editor de Imagens Integrado (Photopea)")
                photopea_url = f"https://www.photopea.com/#open:{st.session_state.img_url_edicao}"
                st.markdown("""
                🔧 **Dicas de Edição:**  
                - Adicione o preço do produto usando a ferramenta de texto.  
                - Ajuste cores, tamanhos e posição conforme necessário.  
                - Faça o download manual da imagem usando **File > Export As > PNG**.
                """)
                st.markdown(
                    f"""
                    <style>
                        .iframe-container {{
                            text-align: center;
                        }}
                        .iframe-container iframe {{
                            border: none;
                            width: 80%;
                            height: 700px;
                            border-radius: 10px;
                            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
                        }}
                    </style>
                    <div class="iframe-container">
                        <iframe src="{photopea_url}"></iframe>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # Geração do post combinando trending e hashtags adicionais
        tags_adicionais = [tag.strip() for tag in novas_tags.split(',') if tag.strip()] + tags_trending
        post_gerado = gerar_post(st.session_state.dados_produto, tags_adicionais)
        
        st.subheader("📋 Post Formatado para Copiar")
        st.text_area("Clique para selecionar e copiar:", value=post_gerado, height=250, key="post_area")
        
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
        st.markdown(
            f"""
            <div style="margin-top: 20px;">
                <a href="https://twitter.com/intent/tweet?text={texto_compartilhamento}&url={url_afiliado_encoded}" target="_blank">
                    <button style="background-color: #1DA1F2; color: white; padding: 8px 16px; border: none; border-radius: 5px; margin-right: 10px;">🐦 Twitter</button>
                </a>
                <a href="https://www.facebook.com/sharer/sharer.php?u={url_afiliado_encoded}&quote={texto_compartilhamento}" target="_blank">
                    <button style="background-color: #1877F2; color: white; padding: 8px 16px; border: none; border-radius: 5px; margin-right: 10px;">📘 Facebook</button>
                </a>
                <a href="https://api.whatsapp.com/send?text={texto_compartilhamento}%20{url_afiliado_encoded}" target="_blank">
                    <button style="background-color: #25D366; color: white; padding: 8px 16px; border: none; border-radius: 5px; margin-right: 10px;">📱 WhatsApp</button>
                </a>
                <a href="https://www.pinterest.com/pin/create/button/?url={url_afiliado_encoded}&description={texto_compartilhamento}&media={url_da_imagem}" target="_blank">
                    <button style="background-color: #BD081C; color: white; padding: 8px 16px; border: none; border-radius: 5px;">📌 Pinterest</button>
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    auto_post_app()
