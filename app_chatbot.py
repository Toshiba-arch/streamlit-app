import streamlit as st
from openai import OpenAI

def run():
    # Título e descrição da aplicação
    st.title("💬 Chatbot com GPT e Mais Funcionalidades")
    st.write("Este é um chatbot simples alimentado pelo modelo GPT-4. Além disso, você pode gerar posts automáticos, analisar imagens, gerar imagens, transcrever áudio, converter texto em fala, transcrever fala para texto e mais!")

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

    # Seleção de funcionalidades
    st.write("Escolha uma funcionalidade:")
    menu = st.selectbox(
        "Escolha a funcionalidade",
        ("Chatbot", "Geração de Imagens", "Análise de Imagens", "Análise de Áudio", "Texto para Fala", "Fala para Texto", "Gerar Haiku", "Baixar Histórico")
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

    # Função de Geração de Imagens
    elif menu == "Geração de Imagens":
        st.write("### Geração de Imagens com DALL·E")
        image_description = st.text_input("Descreva a imagem que você deseja gerar:")
        if st.button("Gerar Imagem") and image_description:
            try:
                # Chamada à API da OpenAI para gerar a imagem com base na descrição fornecida
                image_response = client.images.create(
                    prompt=image_description,
                    n=1,  # Número de imagens a serem geradas
                    size="1024x1024"  # Tamanho da imagem gerada
                )
                image_url = image_response['data'][0]['url']
                st.image(image_url, caption="Imagem gerada", use_column_width=True)
            except Exception as e:
                st.error(f"Erro ao gerar imagem: {e}")
            
    # Função de Análise de Imagens
    elif menu == "Análise de Imagens":
        st.write("### Análise de Imagens com GPT")
        image_url = st.text_input("Insira a URL da imagem para análise:")
        if image_url:
            st.image(image_url, caption="Imagem carregada")
            st.write("Aqui você pode adicionar a lógica para analisar a imagem.")

    # Função de Análise de Áudio
    elif menu == "Análise de Áudio":
        st.write("### Análise de Áudio com Whisper")
        audio_file = st.file_uploader("Carregue um arquivo de áudio", type=["mp3", "wav", "m4a"])
        if audio_file:
            st.audio(audio_file, format="audio/wav")
            if st.button("Transcrever Áudio"):
                try:
                    # Enviar o arquivo de áudio para a API Whisper para transcrição
                    transcription_response = client.audio.transcribe(
                        file=audio_file,
                        model="whisper-1"
                    )
                    transcription_text = transcription_response['text']
                    st.write("**Transcrição do Áudio:**")
                    st.write(transcription_text)
                except Exception as e:
                    st.error(f"Erro ao transcrever o áudio: {e}")

    # Função de Texto para Fala (Text-to-Speech)
    elif menu == "Texto para Fala":
        st.write("### Conversão de Texto para Fala")
        text_to_convert = st.text_area("Digite o texto para conversão em fala:")
        if st.button("Gerar Fala") and text_to_convert:
            try:
                # Chamada à API da OpenAI para gerar áudio a partir do texto
                audio_response = client.audio.create(
                    model="text-to-speech-1",
                    input=text_to_convert
                )
                audio_url = audio_response['data'][0]['url']
                st.audio(audio_url, format="audio/mp3")
            except Exception as e:
                st.error(f"Erro ao gerar fala: {e}")

    # Função de Fala para Texto (Speech-to-Text)
    elif menu == "Fala para Texto":
        st.write("### Conversão de Fala para Texto")
        audio_file = st.file_uploader("Carregue um arquivo de áudio para transcrição (MP3, WAV, M4A):", type=["mp3", "wav", "m4a"])
        if audio_file:
            st.audio(audio_file, format="audio/wav")
            if st.button("Transcrever Fala para Texto"):
                try:
                    # Chamada à API da OpenAI para transcrever fala para texto
                    transcription_response = client.audio.transcribe(
                        file=audio_file,
                        model="whisper-1"
                    )
                    transcription_text = transcription_response['text']
                    st.write("**Texto Transcrito:**")
                    st.write(transcription_text)
                except Exception as e:
                    st.error(f"Erro ao transcrever a fala: {e}")

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
