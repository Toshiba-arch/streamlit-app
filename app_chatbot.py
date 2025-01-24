import streamlit as st
from openai import OpenAI

def run():
    # Título e descrição da aplicação
    st.title("💬 Chatbot com GPT e Mais Funcionalidades")
    st.write("Este é um chatbot simples alimentado pelo modelo GPT-4. Além disso, você pode gerar posts automáticos, analisar imagens, gerar imagens, transcrever áudio, converter texto em fala, transcrever fala para texto, gerar embeddings e mais!")

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
    menu = st.selectbox(
        "Escolha a funcionalidade",
        ("Chatbot", "Geração de Imagens", "Análise de Imagens", "Análise de Áudio", "Texto para Fala", "Fala para Texto", "Gerar Haiku", "Embeddings", "Baixar Histórico", "Sobre as Funcionalidades")
    )

    # Descrições Explicativas sobre as funcionalidades
    if menu == "Sobre as Funcionalidades":
        st.write("### Descrição das Funcionalidades")
        with st.expander("💬 Chatbot com GPT"):
            st.write("""
                Este chatbot é alimentado pelo modelo GPT-4 e pode conversar com você sobre qualquer tópico. 
                Ele gera respostas automatizadas com base nas suas mensagens, permitindo uma interação natural e fluida. 
                **Quando usar?**: Ideal para conversar sobre tópicos gerais, obter respostas rápidas ou até mesmo testar o poder do GPT.
            """)
        
        with st.expander("🖼 Geração de Imagens"):
            st.write("""
                Utilize a geração de imagens para criar imagens a partir de descrições de texto. O modelo DALL·E da OpenAI transforma palavras em imagens visuais. 
                **Quando usar?**: Útil quando você precisa de imagens criativas para apresentações, designs ou qualquer conteúdo visual.
            """)
        
        with st.expander("🖼 Análise de Imagens"):
            st.write("""
                A análise de imagens permite que você envie uma URL de imagem para ser analisada. Embora o modelo não ofereça uma análise detalhada 
                como um ser humano faria, ele pode fornecer insights e interpretações interessantes.
                **Quando usar?**: Ideal para examinar imagens e obter descrições ou possíveis informações sobre o conteúdo visual.
            """)
        
        with st.expander("🎧 Análise de Áudio"):
            st.write("""
                Utilize a análise de áudio para transcrever arquivos de áudio em texto. O modelo Whisper da OpenAI converte áudio gravado em texto.
                **Quando usar?**: Útil para transcrever gravações de reuniões, entrevistas ou qualquer outro tipo de áudio que precise ser convertido para texto.
            """)
        
        with st.expander("🔊 Texto para Fala"):
            st.write("""
                Converta texto em fala com o modelo de Text-to-Speech da OpenAI. Você fornece um texto, e ele gera o áudio correspondente.
                **Quando usar?**: Ideal para criar áudios a partir de textos, como para podcasts, livros falados ou assistentes virtuais.
            """)
        
        with st.expander("🗣 Fala para Texto"):
            st.write("""
                A transcrição de fala para texto converte áudio gravado (MP3, WAV, M4A) em texto, utilizando o modelo Whisper.
                **Quando usar?**: Útil quando você tem gravações de voz e precisa transcrever para texto, como transcrições de entrevistas ou reuniões.
            """)
        
        with st.expander("📜 Gerador de Haiku"):
            st.write("""
                O gerador de Haiku cria poemas curtos e simétricos baseados em um tema que você fornece. Haikus são uma forma poética tradicional japonesa.
                **Quando usar?**: Para fins criativos, como escrever poesias sobre temas específicos, ou até mesmo para se inspirar.
            """)
        
        with st.expander("🔢 Embeddings"):
            st.write("""
                Geração de Embeddings converte textos em vetores numéricos, que são úteis para comparação semântica e outras aplicações de aprendizado de máquina.
                **Quando usar?**: Essencial para criar sistemas de busca, recomendações ou qualquer aplicação que precise comparar a semelhança de textos.
            """)
        
        with st.expander("💾 Baixar Histórico"):
            st.write("""
                Baixe o histórico das interações do chatbot em um arquivo de texto. Útil se você precisar manter um registro ou analisar as conversas mais tarde.
                **Quando usar?**: Quando você deseja salvar ou revisar o histórico de suas interações com o chatbot.
            """)

    # Funções do Chatbot
    elif menu == "Chatbot":
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
        audio_file = st.file_uploader("Carregue um arquivo de áudio (MP3, WAV, M4A) para transcrição:", type=["mp3", "wav", "m4a"])
        if audio_file:
            try:
                audio_response = client.audio.transcribe(model="whisper-1", file=audio_file)
                st.write("Texto transcrito do áudio:")
                st.write(audio_response["text"])
            except Exception as e:
                st.error(f"Erro ao transcrever áudio: {e}")

    # Função de Texto para Fala
    elif menu == "Texto para Fala":
        st.write("### Texto para Fala com OpenAI")
        text_input = st.text_area("Digite o texto que você deseja converter em fala:")
        if st.button("Converter Texto em Fala") and text_input:
            try:
                audio_response = client.audio.create(
                    model="text-to-speech",
                    input={"text": text_input}
                )
                audio_url = audio_response['data'][0]['url']
                st.audio(audio_url, format='audio/mp3')
            except Exception as e:
                st.error(f"Erro ao converter texto em fala: {e}")

    # Função de Fala para Texto
    elif menu == "Fala para Texto":
        st.write("### Fala para Texto com Whisper")
        audio_file = st.file_uploader("Carregue um arquivo de áudio (MP3, WAV, M4A) para transcrição:", type=["mp3", "wav", "m4a"])
        if audio_file:
            try:
                audio_response = client.audio.transcribe(model="whisper-1", file=audio_file)
                st.write("Texto transcrito do áudio:")
                st.write(audio_response["text"])
            except Exception as e:
                st.error(f"Erro ao transcrever áudio: {e}")

    # Função de Gerar Haiku
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

    # Função de Embeddings
    elif menu == "Embeddings":
        st.write("### Geração de Embeddings")
        text_input = st.text_area("Digite o texto para gerar o embedding:")
        if st.button("Gerar Embedding") and text_input:
            try:
                embedding_response = client.embeddings.create(model="text-embedding-ada-002", input=[text_input])
                st.write("Embedding gerado:", embedding_response['data'][0]['embedding'])
            except Exception as e:
                st.error(f"Erro ao gerar embedding: {e}")

    # Função para Baixar o Histórico
    elif menu == "Baixar Histórico":
        if st.download_button(
            "💾 Baixar histórico do chat",
            data="\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.messages]),
            file_name="chat_history.txt",
            mime="text/plain"
        ):
            st.success("Histórico baixado com sucesso!")

# Executar a aplicação
if __name__ == "__main__":
    run()
