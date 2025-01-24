import streamlit as st
from openai import OpenAI

def run():
    # Show title and description.
    st.title("💬 Chatbot")
   #st.write(
        #"This is a simple chatbot that uses OpenAI's GPT-3.5 model to generate responses. "
        #"To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
        #"You can also learn how to build this app step by step by [following our tutorial](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)."
   #)

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

        # Gerar resposta usando a API
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": m["role"], "content": m["Content"]} for m in st.session_state.messages],
            stream=True,
        )
#        completion = client.chat.completions.create(
#           model="gpt-4o-mini",
#            store=True,
#           messages=[
#                {"role": "user", "content": "write a haiku about ai"}
#            ]
#        )    

#        print(completion.choices[0].message);

   #Exibir a resposta gerada e salvar no session state
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
