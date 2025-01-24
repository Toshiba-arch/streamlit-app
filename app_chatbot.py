import streamlit as st
from openai import OpenAI

def run():
    # Título e descrição da aplicação
    st.title("💬 Chatbot com GPT e Mais Funcionalidades")
    st.write("Este é um chatbot simples alimentado pelo modelo GPT-4. Além disso, você pode analisar imagens, gerar haikus e baixar o histórico do chat.")

    # Obter a API Key dos secrets
    openai_api_key = st.secrets.get("openai_api_key")
    if not openai_api_key:
        st.error("API Key não configurada. Por favor, adicione-a em **Settings > Secrets**.", icon="🛑")
        return

    # Criar cliente OpenAI
    client = OpenAI(api_key=openai_api_key)

    # Inicializar histórico de mensagens
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Seleção de funcionalidades no topo do layout
    menu = st.selectbox(
        "Escolha a funcionalidade",
        ("Chatbot", "Análise de Imagens", "Gerar Haiku", "Baixar Histórico")
    )

    # Função do Chatbot
    if menu == "Chatbot":
        st.write("### 💬 Chatbot com GPT")
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        prompt = st.chat_input("Digite sua mensagem:")
        if prompt:
            if len(prompt) > 500:
                st.warning("Sua mensagem é muito longa. Por favor, seja mais breve!")
            else:
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)

                completion = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                )

                response = completion.choices[0].message.content
                with st.chat_message("assistant"):
                    st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

        # Botão para limpar o histórico
        if st.button("🧹 Limpar histórico"):
            st.session_state.messages = []
            st.info("Histórico de mensagens limpo!")

    # Função de Análise de Imagens
    elif menu == "Análise de Imagens":
        st.write("### Análise de Imagens com GPT")
        image_url = st.text_input("Insira a URL da imagem para análise:")
        if image_url:
            st.image(image_url, caption="Imagem carregada")
            st.write("Aqui você pode adicionar a lógica para analisar a imagem.")

    # Função de Gerador de Haiku
    elif menu == "Gerar Haiku":
        st.write("### Gerador de Haiku")
        haiku_theme = st.text_input("Tema do Haiku (opcional):", placeholder="Por exemplo: tecnologia, natureza, etc.")
        if st.button("📜 Gerar Haiku"):
            haiku_prompt = f"Escreva um haiku sobre {haiku_theme}" if haiku_theme else "Escreva um haiku sobre IA"
            haiku_completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": haiku_prompt}]
            )
            haiku = haiku_completion.choices[0].message.content
            st.markdown(f"**Haiku:**\n\n{haiku}")

    # Função para Baixar o Histórico
    elif menu == "Baixar Histórico":
        if st.download_button(
            "💾 Baixar histórico do chat",
            data="\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.messages]),
            file_name="chat_history.txt",
            mime="text/plain"
        ):
            st.success("Histórico baixado com sucesso!")
