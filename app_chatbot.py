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
    return OpenAI(api_key=openai_api_key)

# Função para exibir o título da aplicação
def show_app_title():
    st.title("💬 Chatbot com GPT e Mais Funcionalidades")
    st.write("Este é um chatbot simples alimentado pelo modelo GPT-4. Além disso, você pode gerar imagens, transcrever áudio, gerar áudio a partir de texto e muito mais!")

# Função para exibir a descrição de cada funcionalidade
def show_feature_description(feature):
    descriptions = {
        "Chatbot Padrão": "O chatbot permite que você converse com um modelo GPT para obter respostas inteligentes sobre diversos temas.",
        "Chatbot com Raciocínio": "Este chatbot utiliza um modelo avançado da OpenAI com habilidades de raciocínio para resolver problemas mais complexos e oferecer soluções detalhadas.",
        "Análise de Imagens": "Você pode carregar uma URL de imagem para análise do conteúdo presente nela.",
        "Gerar Haiku": "Crie haikus personalizados sobre temas específicos com a ajuda da IA.",
        "Texto para Imagem": "Você pode gerar imagens a partir de descrições de texto, utilizando a API de imagens da OpenAI.",
        "Áudio para Texto": "Essa funcionalidade converte arquivos de áudio em texto, usando a API da OpenAI.",
        "Texto para Fala": "Gere áudio falado a partir de texto, criando falas realistas com a OpenAI.",
        "Fala para Texto": "Converta áudio gravado ou ao vivo para texto, útil para transcrições de conversa.",
        "Embeddings": "Crie embeddings para comparar textos semanticamente, útil para buscas e recomendações baseadas em conteúdo."
    }
    st.expander(f"🔍 Sobre {feature}", expanded=True).markdown(descriptions.get(feature, "Sem descrição disponível"))

# Função para exibir o Chatbot Padrão
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
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            )
            response = completion.choices[0].message.content
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

    # Botões de limpar histórico e baixar histórico
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🧹 Limpar histórico"):
            st.session_state.messages = []
            st.info("Histórico de mensagens limpo!")
    with col2:
        if st.download_button(
            "💾 Baixar histórico do chat",
            data="\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.messages]),
            file_name="chat_history.txt",
            mime="text/plain"
        ):
            st.success("Histórico baixado com sucesso!")

# Função para exibir o Chatbot com Raciocínio
def show_reasoning_chatbot(client):
    st.write("### 💬 Chatbot com Raciocínio (GPT-4 com Reasoning)")
    if "reasoning_messages" not in st.session_state:
        st.session_state.reasoning_messages = []
        
    for message in st.session_state.reasoning_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Digite sua mensagem para raciocínio:")
    if prompt:
        if len(prompt) > 500:
            st.warning("Sua mensagem é muito longa. Por favor, seja mais breve!")
        else:
            st.session_state.reasoning_messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Usar o modelo com raciocínio (Reasoning)
            reasoning_prompt = f"Para resolver este problema, siga um raciocínio passo a passo: {prompt}"
            completion = client.chat.completions.create(
                model="gpt-4",  # Usando modelo com raciocínio avançado
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.reasoning_messages]
            )
            response = completion.choices[0].message.content
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.reasoning_messages.append({"role": "assistant", "content": response})

    # Botões de limpar histórico e baixar histórico
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🧹 Limpar histórico"):
            st.session_state.reasoning_messages = []
            st.info("Histórico de mensagens limpo!")
    with col2:
        if st.download_button(
            "💾 Baixar histórico do chat",
            data="\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.reasoning_messages]),
            file_name="reasoning_chat_history.txt",
            mime="text/plain"
        ):
            st.success("Histórico baixado com sucesso!")

# Função para exibir a Análise de Imagens
def show_image_analysis(client):
    st.write("### Análise de Imagens com GPT")
    image_url = st.text_input("Insira a URL da imagem para análise:")
    if image_url:
        st.image(image_url, caption="Imagem carregada")
        # Chamada para a API para analisar a imagem (exemplo fictício)
        st.write("Aqui você pode adicionar a lógica para analisar a imagem.")

# Função para exibir o Gerador de Haiku
def show_haiku_generation(client):
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

# Função para gerar imagem a partir de texto
def show_text_to_image(client):
    st.write("### Gerar Imagem a partir de Texto")
    text_prompt = st.text_input("Digite a descrição da imagem desejada:")
    if text_prompt:
        response = client.images.create(prompt=text_prompt, n=1, size="1024x1024")
        image_url = response['data'][0]['url']
        st.image(image_url, caption="Imagem gerada pela IA")

# Função para converter áudio em texto
def show_audio_to_text(client):
    st.write("### Converter Áudio em Texto")
    audio_file = st.file_uploader("Envie um arquivo de áudio (MP3, WAV, etc.):", type=["mp3", "wav"])
    if audio_file:
        st.audio(audio_file, format='audio/wav')
        st.write("Convertendo áudio para texto...")
        # Substituir pelo código real para transcrição, se necessário.
        transcript = "Texto transcrito do áudio (exemplo)."
        st.write("Transcrição:", transcript)

# Função para gerar fala a partir de texto
def show_text_to_speech(client):
    st.write("### Gerar Fala a partir de Texto")
    text_input = st.text_input("Digite o texto para gerar a fala:")
    if text_input:
        # Gerar áudio de fala com a API de texto para fala
        st.audio("audio_output.mp3", format="audio/mp3")  # Exemplo fictício de áudio

# Função para converter fala em texto
def show_speech_to_text(client):
    st.write("### Converter Fala em Texto")
    audio_file = st.file_uploader("Envie um arquivo de áudio para transcrição:", type=["mp3", "wav"])
    if audio_file:
        st.audio(audio_file, format="audio/wav")
        st.write("Convertendo fala para texto...")
        # Aqui a API de transcrição de fala seria chamada.
        transcribed_text = "Texto transcrito da fala."
        st.write("Texto transcrito:", transcribed_text)

# Função para gerar embeddings de texto
def show_embeddings(client):
    st.write("### Gerar Embeddings de Texto")
    input_text = st.text_area("Digite o texto para gerar o embedding:")
    if input_text:
        embeddings = client.embeddings.create(input=[input_text])
        st.write("Embeddings gerados:", embeddings['data'][0]['embedding'])

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
        ("Chatbot Padrão", "Chatbot com Raciocínio", "Análise de Imagens", "Gerar Haiku", "Texto para Imagem", "Áudio para Texto", "Texto para Fala", "Fala para Texto", "Embeddings")
    )
    
    # Exibir a descrição
    show_feature_description(feature)

    # Exibir a funcionalidade selecionada
    if feature == "Chatbot Padrão":
        show_chatbot(client)
    elif feature == "Chatbot com Raciocínio":
        show_reasoning_chatbot(client)
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
