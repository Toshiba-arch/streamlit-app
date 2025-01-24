import streamlit as st
from openai import OpenAI

def run():
    # Show title and description.
    st.title("💬 Chatbot")

    # Obter a API Key dos secrets
    openai_api_key = st.secrets.get("openai_api_key")
    
    if not openai_api_key:
        st.error("API Key não configurada. Por favor, adicione-a em **Settings > Secrets**.", icon="🛑")
        return

    # Criar cliente OpenAI
    client = OpenAI(api_key=openai_api_key)

    # Armazenar mensagens no session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Exibir mensagens anteriores
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Campo para entrada de mensagem
    if prompt := st.chat_input("Digite sua mensagem:"):
        # Adicionar mensagem do usuário
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Gerar resposta usando a API sem streaming
        completion = client.chat.completions.create(
            model="gpt-4o-mini",  # Modelo especificado
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        )

        # Extrair a resposta gerada
        response = completion.choices[0].message["content"]

        # Exibir a resposta gerada e salvar no session state
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Código com streaming comentado para fácil reativação
        # stream = client.chat.completions.create(
        #     model="gpt-4o-mini",  # Modelo especificado
        #     messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
        #     stream=True,
        # )
        # with st.chat_message("assistant"):
        #     response = st.write_stream(stream)
        # st.session_state.messages.append({"role": "assistant", "content": response})

    # Gerar e exibir um Haiku fixo como exemplo
    haiku_completion = client.chat.completions.create(
        model="gpt-4o-mini",  # Modelo especificado
        messages=[
            {"role": "user", "content": "Write a haiku about AI"}
        ]
    )

    # Exibir o Haiku gerado
    haiku = haiku_completion.choices[0].message["content"]
    st.write("### Haiku gerado:")
    st.markdown(haiku)
