import streamlit as st
from openai import OpenAI

def run():
    # Título e descrição
    st.title("💬 Chatbot com GPT")
    st.write("Este é um chatbot simples alimentado pelo modelo GPT-4. Insira sua mensagem e receba respostas inteligentes!")

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

    # Botão para limpar o histórico
    if st.button("🧹 Limpar histórico"):
        st.session_state.messages = []
        st.info("Histórico de mensagens limpo!")

    # Exibir histórico de mensagens
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Entrada de mensagem do usuário
    prompt = st.chat_input("Digite sua mensagem:")
    if prompt:
        # Validação de entrada
        if len(prompt) > 500:
            st.warning("Sua mensagem é muito longa. Por favor, seja mais breve!")
        else:
            # Adicionar mensagem do usuário ao histórico
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Gerar resposta usando a API
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            )

            # Extrair a resposta gerada
            response = completion.choices[0].message.content

            # Exibir e salvar a resposta no histórico
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

    # Gerar um Haiku personalizado
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

    # Baixar histórico de chat
    if st.download_button(
        "💾 Baixar histórico do chat",
        data="\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.messages]),
        file_name="chat_history.txt",
        mime="text/plain"
    ):
        st.success("Histórico baixado com sucesso!")
