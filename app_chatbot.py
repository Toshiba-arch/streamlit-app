import streamlit as st
from openai import OpenAI
import openai
import time

# Função para inicializar o cliente OpenAI
def initialize_openai_client():
    openai_api_key = st.secrets.get("openai_api_key")
    if not openai_api_key:
        st.error("API Key não configurada. Por favor, adicione-a em **Settings > Secrets**.", icon="🛑")
        return None
    return openai

# Função para exibir o título da aplicação
def show_app_title():
    st.title("💬 Chatbot Avançado com GPT")
    st.write("Este chatbot usa funcionalidades avançadas, como Saídas Estruturadas, Saídas Previsíveis e Chamadas de Funções!")

# Função para exibir o Chatbot
def show_chatbot(client):
    st.write("### 💬 Chatbot com GPT")
    if "messages" not in st.session_state:
        st.session_state.messages = []

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

            completion = client.Completion.create(
                model="gpt-4",
                prompt=prompt,
                max_tokens=150,
                temperature=0.7
            )
            response = completion.choices[0].text.strip()
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

    if st.button("🧹 Limpar histórico"):
        st.session_state.messages = []
        st.info("Histórico de mensagens limpo!")

# Função para exibir o Chatbot com Reasoning
def show_chatbot_with_reasoning(client):
    st.write("### 💬 Chatbot com GPT (Raciocínio Detalhado)")
    if "messages" not in st.session_state:
        st.session_state.messages = []

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

            reasoning_prompt = f"Explique detalhadamente a solução para: {prompt}"

            completion = client.Completion.create(
                model="gpt-4",
                prompt=reasoning_prompt,
                max_tokens=150,
                temperature=0.7
            )
            response = completion.choices[0].text.strip()
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

    if st.button("🧹 Limpar histórico"):
        st.session_state.messages = []
        st.info("Histórico de mensagens limpo!")

# Função para exibir o Chatbot com Saídas Estruturadas
def show_structured_output_chatbot(client):
    st.write("### 💬 Chatbot com Saídas Estruturadas")
    if "messages" not in st.session_state:
        st.session_state.messages = []

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

            response = get_structured_response(prompt)

            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

    if st.button("🧹 Limpar histórico"):
        st.session_state.messages = []
        st.info("Histórico de mensagens limpo!")

# Função para gerar uma resposta estruturada
def get_structured_response(prompt):
    response = openai.Completion.create(
        model="gpt-4",
        prompt=f"Estruture a resposta da seguinte forma: {{'informação': '{prompt}'}}",
        max_tokens=150,
        temperature=0.7
    )
    return response['choices'][0]['text'].strip()

# Função para exibir o Chatbot com Saídas Previsíveis
def show_predicted_output_chatbot(client):
    st.write("### 💬 Chatbot com Saídas Previsíveis")
    if "messages" not in st.session_state:
        st.session_state.messages = []

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

            response = get_predicted_output(prompt)

            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

    if st.button("🧹 Limpar histórico"):
        st.session_state.messages = []
        st.info("Histórico de mensagens limpo!")

# Função para gerar uma saída previsível
def get_predicted_output(prompt):
    response = openai.Completion.create(
        model="gpt-4",
        prompt=prompt,
        max_tokens=100,
        temperature=0.3
    )
    return response.choices[0].text.strip()

# Função para exibir o Chatbot com Chamadas de Funções
def show_function_calling_chatbot(client):
    st.write("### 💬 Chatbot com Chamadas de Funções")
    if "messages" not in st.session_state:
        st.session_state.messages = []

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

            response = process_function_call(prompt)

            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

    if st.button("🧹 Limpar histórico"):
        st.session_state.messages = []
        st.info("Histórico de mensagens limpo!")

# Função para processar uma entrada e chamar a função apropriada
def process_function_call(prompt):
    # Exemplo de função: Previsão do tempo
    if "previsão do tempo" in prompt.lower():
        return get_weather_forecast()
    else:
        return "Não entendi sua solicitação. Pode reformular?"

# Função fictícia para obter previsão do tempo
def get_weather_forecast():
    return "A previsão do tempo para hoje é ensolarada com temperaturas em torno de 25°C."

# Função principal para exibir a interface
def run():
    show_app_title()

    # Inicialização do cliente OpenAI
    client = initialize_openai_client()
    if not client:
        return  # Se a API key não estiver configurada, interrompe a execução

    # Menu de funcionalidades
    feature = st.selectbox(
        "Escolha a funcionalidade:",
        ("Chatbot", "Chatbot com Reasoning", "Chatbot com Saídas Estruturadas", "Chatbot com Saídas Previsíveis", "Chatbot com Chamadas de Funções",
         "Análise de Imagens", "Gerar Haiku", "Texto para Imagem", "Áudio para Texto", "Texto para Fala", "Fala para Texto", "Embeddings")
    )

    # Exibir a funcionalidade selecionada
    if feature == "Chatbot":
        show_chatbot(client)
    elif feature == "Chatbot com Reasoning":
        show_chatbot_with_reasoning(client)
    elif feature == "Chatbot com Saídas Estruturadas":
        show_structured_output_chatbot(client)
    elif feature == "Chatbot com Saídas Previsíveis":
        show_predicted_output_chatbot(client)
    elif feature == "Chatbot com Chamadas de Funções":
        show_function_calling_chatbot(client)
    elif feature == "Análise de Imagens":
        show_image_analysis(client)
    elif feature == "Gerar Haiku":
        show_haiku_generation(client)
    elif feature == "Texto para Imagem":
        show_text_to_image(client)
    elif feature == "Áudio para Texto":
        show_audio_to_text(client)
    elif feature == "Texto para Fala":
        show_text_to_speech(client)
    elif feature == "Fala para Texto":
        show_speech_to_text(client)
    elif feature == "Embeddings":
        show_embeddings(client)

# Rodar a aplicação
if __name__ == "__main__":
    run()

