import requests
from PIL import Image
from io import BytesIO

def criar_imagem_com_texto(imagem_url, nome_produto, preco_original, preco_atual, desconto, cupom=None):
    try:
        # Tentar fazer o download da imagem
        response = requests.get(imagem_url)
        
        # Verificar se a resposta foi bem-sucedida
        if response.status_code == 200:
            # Verificar se o conteúdo é uma imagem
            try:
                imagem = Image.open(BytesIO(response.content))
                imagem.verify()  # Verifica se a imagem é válida
                imagem = Image.open(BytesIO(response.content))  # Reabre a imagem após a verificação
            except (IOError, SyntaxError) as e:
                raise Exception("A URL fornecida não contém uma imagem válida.")
        else:
            raise Exception("Falha ao acessar a URL da imagem. Verifique o link.")
        
        # Processar a imagem (adicionar texto, etc.)
        draw = ImageDraw.Draw(imagem)
        font = ImageFont.load_default()

        texto_desconto = f"Desconto: {desconto}%"
        texto_valor = f"De €{preco_original:.2f} por €{preco_atual:.2f}"
        
        if cupom:
            texto_cupom = f"Use o código: {cupom}"
        else:
            texto_cupom = ""
        
        largura, altura = imagem.size

        # Posicionar o texto
        draw.text((10, altura - 50), texto_desconto, fill="white", font=font)
        draw.text((10, altura - 30), texto_valor, fill="white", font=font)
        if cupom:
            draw.text((10, altura - 10), texto_cupom, fill="white", font=font)

        return imagem

    except Exception as e:
        print(f"Erro ao carregar a imagem: {e}")
        return None
