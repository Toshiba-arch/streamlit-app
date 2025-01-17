import streamlit as st
import random

# Função para gerar números aleatórios do Euromilhões
def gerar_numeros_aleatorios():
    numeros = random.sample(range(1, 51), 5)  # Escolher 5 números únicos de 1 a 50
    estrelas = random.sample(range(1, 13), 2)  # Escolher 2 estrelas únicas de 1 a 12
    return sorted(numeros), sorted(estrelas)

# Função para gerar números baseados em critérios (exemplo simplificado)
def gerar_numeros_probabilidade():
    # Exemplos de números e estrelas mais sorteados (dados fictícios)
    numeros_mais_sorteados = [10, 23, 25, 33, 44]
    estrelas_mais_sorteadas = [2, 8]
    
    # Combinar os mais sorteados com números aleatórios
    numeros = random.sample(numeros_mais_sorteados, 3) + random.sample(range(1, 51), 2)
    estrelas = random.sample(estrelas_mais_sorteadas, 1) + random.sample(range(1, 13), 1)
    
    return sorted(numeros), sorted(estrelas)

# Layout geral da aplicação
st.set_page_config(page_title="App de Ofertas e Euromilhões", layout="wide")
st.markdown("<h1 style='text-align: center;'>App de Ofertas e Euromilhões</h1>", unsafe_allow_html=True)
st.sidebar.title("Menu")

# Menu de navegação
opcao = st.sidebar.radio("Escolha uma funcionalidade", ["Gerar Post de Oferta", "Gerador de Números do Euromilhões"])

if opcao == "Gerar Post de Oferta":
    st.subheader("Gerar Post de Oferta")
    nome_produto = st.text_input("Nome do Produto")
    tem_desconto = st.radio("O produto tem desconto?", ["Sim", "Não"])
    if tem_desconto == "Sim":
        desconto_percentual = st.number_input("Porcentagem de Desconto (%)", min_value=0.0, step=0.01, format="%.2f")
        preco_atual = st.number_input("Preço Atual (€)", min_value=0.0, step=0.01, format="%.2f")
        preco_original = preco_atual / (1 - desconto_percentual / 100)
    else:
        preco_original = st.number_input("Preço Original (€)", min_value=0.0, step=0.01, format="%.2f")
        preco_atual = st.number_input("Preço Atual (€)", min_value=0.0, step=0.01, format="%.2f")

    cupom = st.text_input("Código de Cupom (se houver)")
    imagem_url = st.text_input("URL da Imagem do Produto")
    link_referencia = st.text_input("Link de Afiliado")
    tags = st.text_input("Insira tags separadas por vírgula (ex: #amazon, #oferta)")

    if st.button("Gerar Post"):
        if nome_produto and preco_atual > 0 and link_referencia and imagem_url:
            produto = {
                "nome": nome_produto,
                "preco_original": preco_original,
                "preco_atual": preco_atual,
                "imagem": imagem_url,
                "cupom": cupom
            }
            post_texto = f"""
            📢 **Oferta Imperdível!** 📢  
            🔹 **{nome_produto}**  
            💰 De **€{preco_original:.2f}** por apenas **€{preco_atual:.2f}**!  
            {f'💥 Use o código de cupom: **{cupom}** para mais descontos!' if cupom else ''}
            👉 [Compre agora]({link_referencia})
            {" ".join([f"#{tag.strip()}" for tag in tags.split(",")]) if tags else ''}
            """
            st.text_area("Post Gerado:", post_texto, height=200)
        else:
            st.error("Preencha todas as informações para gerar o post.")

elif opcao == "Gerador de Números do Euromilhões":
    st.subheader("Gerador de Números do Euromilhões")
    metodo = st.radio("Escolha o método de geração:", ["Aleatório", "Baseado em Probabilidade"])
    
    if st.button("Gerar Números"):
        if metodo == "Aleatório":
            numeros, estrelas = gerar_numeros_aleatorios()
        else:
            numeros, estrelas = gerar_numeros_probabilidade()

        st.success("Os seus números foram gerados!")
        st.write(f"**Números:** {', '.join(map(str, numeros))}")
        st.write(f"**Estrelas:** {', '.join(map(str, estrelas))}")
        st.info("Boa sorte! 🍀")
