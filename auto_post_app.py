import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
from io import BytesIO
import urllib.parse
from PIL import Image, ImageDraw, ImageFont

# =============================================================================
# Configurações Globais e Funções de Utilidade
# =============================================================================

# Cabeçalhos para requisições HTTP
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "es-ES,es;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive"
}

def extrair_preco(texto):
    """Extrai valores numéricos de strings de preço."""
    try:
        return float(re.sub(r'[^\d.,]', '', texto).replace(',', '.'))
    except:
        return 0.0

def extrair_dados_produto(url_afiliado):
    """
    Extrai dados do produto (título, preços, imagens e cupom)
    a partir da URL do afiliado.
    Altere os seletores se a estrutura da página mudar.
    """
    try:
        response = requests.get(url_afiliado, headers=HEADERS, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extração do título do produto
        title = soup.find('span', {'id': 'productTitle'}) or soup.find('h1', {'class': 'a-size-large a-spacing-none'})
        title = title.get_text(strip=True) if title else "Produto sem nome"

        # Extração dos preços (atual e original)
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

        # Extração das URLs das imagens
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

        # Extração do cupom, se existir
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
    """Calcula o percentual de desconto."""
    try:
        if original > 0 and atual < original:
            return round(((original - atual) / original) * 100, 2)
        return 0.0
    except ZeroDivisionError:
        return 0.0

def formatar_moeda(valor):
    """Formata o valor monetário para exibição."""
    return f"€{valor:,.2f}".replace(',', ' ').replace('.', ',')

def gerar_post(data, tags):
    """
    Gera o texto do post combinando os dados do produto com as hashtags.
    Altere a formatação conforme a necessidade de cada rede social.
    """
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

def adicionar_overlay(imagem_bytes, texto, font_size=32, margin=10):
    """
    Adiciona sobreposição de texto na parte inferior da imagem com fundo preto.
    
    Parâmetros:
      - imagem_bytes: bytes da imagem original.
      - texto: o texto a ser sobreposto.
      - font_size: tamanho da fonte.
      - margin: margem em pixels a partir da borda da imagem.
    
    O texto é desenhado com fonte bold (Arial Bold) se disponível, em branco, sobre um retângulo preto.
    """
    # Abre a imagem e garante o modo RGBA
    imagem = Image.open(BytesIO(imagem_bytes)).convert("RGBA")
    
    # Cria uma camada transparente com as mesmas dimensões da imagem
    overlay = Image.new("RGBA", imagem.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)
    
    try:
        # Tenta carregar a fonte Arial Bold; caso não encontre, usa a fonte padrão
        font = ImageFont.truetype("arialbd.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()
    
    # Calcula o tamanho do texto para criar o fundo
    text_width, text_height = draw.textsize(texto, font=font)
    
    # Define a posição no canto inferior esquerdo com margem
    x = margin
    y = imagem.height - text_height - margin
    
    # Define um padding para o retângulo de fundo
    padding = 5
    rect_coords = [x - padding, y - padding, x + text_width + padding, y + text_height + padding]
    
    # Desenha o retângulo preto (com opacidade 200) como fundo do texto
    draw.rectangle(rect_coords, fill=(0, 0, 0, 200))
    
    # Desenha o texto em branco sobre o retângulo
    draw.text((x, y), texto, font=font, fill=(255, 255, 255, 255))
    
    # Combina a imagem original com o overlay
    imagem_editada = Image.alpha_composite(imagem, overlay)
    
    output = BytesIO()
    imagem_editada.save(output, format="PNG")
    return output.getvalue()

# =============================================================================
# Função Principal: auto_post_app
# =============================================================================
def auto_post_app():
    st.title("🛒 Gerador de Posts para Afiliados")
    
    # Inicialização dos estados (session_state)
    if 'dados_produto' not in st.session_state:
        st.session_state.dados_produto = None
    if 'selected_images' not in st.session_state:
        st.session_state.selected_images = []
    if 'temp_data' not in st.session_state:
        st.session_state.temp_data = {}
    if 'img_url_edicao' not in st.session_state:
        st.session_state.img_url_edicao = None
    if 'trending_hashtags' not in st.session_state:
        st.session_state.trending_hashtags = []  # Armazena as trending hashtags selecionadas

    # =========================================================================
    # 1. Inserir URL do Produto
    # =========================================================================
    url_afiliado = st.text_input("URL Amazon de afiliado:", key="url_input")
    
    # =========================================================================
    # 2. Extrair Dados do Produto
    # =========================================================================
    if st.button("Carregar Produto"):
        with st.spinner("A extrair dados..."):
            dados = extrair_dados_produto(url_afiliado)
            if dados:
                st.session_state.dados_produto = dados
                st.session_state.temp_data = dados.copy()
                st.session_state.selected_images = dados['imagens_url'][:1]  # Seleciona a primeira imagem
                st.success("Dados carregados!")
            else:
                st.error("Erro ao carregar dados. Verifique o link ou preencha manualmente.")
    
    # =========================================================================
    # 3. Editar Dados do Produto (incluindo Trending Hashtags)
    # =========================================================================
    if st.session_state.dados_produto:
        dados = st.session_state.dados_produto
        with st.expander("🔧 Editar Detalhes", expanded=True):
            with st.form(key='edit_form'):
                col1, col2 = st.columns(2)
                with col1:
                    novo_titulo = st.text_input("Título:", value=st.session_state.temp_data.get('nome', ''), key='edit_title')
                    novo_preco_original = st.number_input("Preço Original:", 
                                                          value=st.session_state.temp_data.get('preco_original', 0.0),
                                                          min_value=0.0, step=0.01, key='edit_original')
                    novo_preco_atual = st.number_input("Preço Atual:", 
                                                       value=st.session_state.temp_data.get('preco_atual', 0.0),
                                                       min_value=0.0, step=0.01, key='edit_atual')
                with col2:
                    novo_cupom = st.text_input("Código do Cupom:", value=st.session_state.temp_data.get('cupom', ''), key='edit_cupom')
                    # Campo para hashtags adicionais (digitadas pelo usuário)
                    novas_tags = st.text_input("Hashtags adicionais (separar por vírgulas):", 
                                               value="promoção, desconto, amazon, oferta", key='edit_tags')
                    # Trending hashtags integradas na edição
                    trending_options = ["oferta", "desconto", "promoção", "Amazon", "economize", "compreagora"]
                    trending_selected = st.multiselect("Trending Hashtags:", trending_options, default=st.session_state.trending_hashtags)
                
                if st.form_submit_button("💾 Atualizar Dados"):
                    st.session_state.dados_produto.update({
                        'nome': novo_titulo,
                        'preco_original': novo_preco_original,
                        'preco_atual': novo_preco_atual,
                        'cupom': novo_cupom
                    })
                    # Atualiza as trending hashtags selecionadas
                    st.session_state.trending_hashtags = trending_selected
                    st.success("Dados atualizados!")
    
    # =========================================================================
    # 4. Geração e Visualização da Imagem para Edição e Download
    # =========================================================================
    if st.session_state.dados_produto:
        dados = st.session_state.dados_produto
        if dados['imagens_url']:
            st.subheader("📸 Imagem do Produto")
            img_url = dados['imagens_url'][0]  # Usa a primeira imagem
            st.image(img_url, width=300)
            # Seleção da imagem (única)
            if st.checkbox("Selecionar Imagem", key="img_select", value=img_url in st.session_state.selected_images):
                st.session_state.selected_images = [img_url]
            else:
                st.session_state.selected_images = []
        
        if st.session_state.selected_images:
            st.subheader("🖼️ Imagem Selecionada para Edição")
            img_url = st.session_state.selected_images[0]
            # Cria um container vazio para a imagem (que será atualizado)
            image_container = st.empty()
            # Exibe a imagem original no container
            image_container.image(img_url, width=300)
            
            # Botão para download da imagem original
            response = requests.get(img_url)
            if response.status_code == 200:
                st.download_button(
                    label="📥 Fazer Download da Imagem",
                    data=response.content,
                    file_name="imagem_produto.png",
                    mime="image/png"
                )
            
            # Seção para aplicar sobreposição de texto na imagem
            overlay_text = st.text_input("Texto para sobreposição (ex: Desconto 20%)", value="")
            if overlay_text and st.button("Aplicar Sobreposição"):
                imagem_editada = adicionar_overlay(response.content, overlay_text, position=(20,20), font_size=32)
                # Atualiza o container com a imagem editada (substituindo a original)
                image_container.image(imagem_editada, width=300)
                st.download_button(
                    label="📥 Fazer Download da Imagem Editada",
                    data=imagem_editada,
                    file_name="imagem_editada.png",
                    mime="image/png"
                )
            
            # Botão para abrir o editor integrado (Photopea)
            if st.button("🖌️ Editar Imagem", key="edit_img"):
                st.session_state.img_url_edicao = img_url
        
            if 'img_url_edicao' in st.session_state and st.session_state.img_url_edicao:
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
    
    # =========================================================================
    # 5. Geração do Post
    # =========================================================================
    if st.session_state.dados_produto:
        # Combina as hashtags adicionais digitadas com as trending selecionadas
        tags_manually = st.session_state.edit_tags if "edit_tags" in st.session_state else "promoção, desconto, amazon, oferta"
        tags_adicionais = [tag.strip() for tag in tags_manually.split(',') if tag.strip()] + st.session_state.trending_hashtags
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
    
    # =========================================================================
    # 6. Botões de Partilha
    # =========================================================================
    if st.session_state.dados_produto:
        st.markdown("---")
        st.subheader("📤 Partilhar Diretamente Por:")
        texto_compartilhamento = urllib.parse.quote(post_gerado)
        url_afiliado_encoded = urllib.parse.quote(st.session_state.dados_produto['url_afiliado'])
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
