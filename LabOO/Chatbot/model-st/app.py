import base64
import streamlit as st
import openai
import time
import os
from typing import Dict, List
from pydantic import BaseModel
from PIL import Image
import io


# --- Modelos de Configuração (de config.py) ---
class AssistantConfig(BaseModel):
    id: str
    name: str
    description: str


AVAILABLE_ASSISTANTS: Dict[str, AssistantConfig] = {
    "Testinhos_Eletronica": AssistantConfig(
        id="workflow",  # ID especial para o workflow
        name="Testinhos de eletronica",
        description="Indica testinhos de eletronica",
    )
}

DEFAULT_ASSISTANT = "Testinhos de eletronica"


# Usa o EventHandler para um streaming real e eficiente
from openai import AssistantEventHandler


class StreamingEventHandler(AssistantEventHandler):
    def __init__(self, text_placeholder):
        super().__init__()
        self.text_placeholder = text_placeholder
        self.full_response = ""

    def on_text_delta(self, delta, snapshot):
        # Adiciona o novo trecho de texto ao placeholder e atualiza o conteúdo
        self.full_response += delta.value
        self.text_placeholder.markdown(self.full_response + "▌")

    def on_end(self):
        # Exibe a resposta final sem o cursor
        self.text_placeholder.markdown(self.full_response)

    def get_full_response(self):
        return self.full_response


# --- Função para processar imagem ---
def process_image(image_file):
    """Processa a imagem e retorna em formato base64 para a API"""
    try:
        # Converte para PIL Image se necessário
        if hasattr(image_file, 'read'):
            image = Image.open(image_file)
        else:
            image = image_file
            
        # Redimensiona se muito grande (para economia de tokens)
        max_size = (1024, 1024)
        if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Converte para base64
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
    except Exception as e:
        st.error(f"Erro ao processar imagem: {e}")
        return None


# --- Configuração da Página e Estilos ---
// ...existing code...

# CSS adicional para componentes de imagem
st.markdown(
    """
<style>
/* ...existing CSS... */

/* Estilo para área de upload de imagem */
.stFileUploader > div {
    background: white;
    border: 2px dashed var(--purple-ultra-light);
    border-radius: 15px;
    transition: all 0.3s ease;
    padding: 1rem;
}

.stFileUploader > div:hover {
    border-color: var(--primary-purple);
    background: var(--purple-ultra-light);
}

/* Estilo para prévia da imagem */
.image-preview {
    border: 2px solid var(--purple-ultra-light);
    border-radius: 10px;
    padding: 0.5rem;
    margin: 0.5rem 0;
    background: white;
}

/* Estilo para botões de captura */
.capture-button {
    background: linear-gradient(135deg, #4CAF50, #45a049);
    color: white !important;
    border: none;
    border-radius: 12px;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
    margin: 0.25rem;
}

.capture-button:hover {
    background: linear-gradient(135deg, #45a049, #4CAF50);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
}
</style>
""",
    unsafe_allow_html=True,
)

# --- Lógica de Backend (Integrada do backend.py) ---
// ...existing code...

# --- Inicialização do Estado da Sessão ---
// ...existing code...

if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None

if "image_data" not in st.session_state:
    st.session_state.image_data = None


# --- Interface da Sidebar (de index.html) ---
with st.sidebar:
    st.title("💬 Agente POLI")

    if st.button("＋ Nova Conversa", use_container_width=True):
        # Reseta o estado da conversa para iniciar um novo chat
        st.session_state.messages = []
        st.session_state.thread_id = None
        st.session_state.uploaded_image = None
        st.session_state.image_data = None
        st.rerun()

    st.header("⚙️ Configurações")

    # Seletor de Assistente
    // ...existing code...

    st.markdown("---")
    
    # Seção de upload de imagem
    st.header("📷 Anexar Imagem")
    
    # Componente para captura de câmera (funciona melhor em dispositivos móveis)
    camera_image = st.camera_input("📸 Capturar da câmera")
    
    # Upload de arquivo de imagem
    uploaded_file = st.file_uploader(
        "📁 Ou escolher da galeria",
        type=['png', 'jpg', 'jpeg', 'gif', 'bmp'],
        help="Formatos suportados: PNG, JPG, JPEG, GIF, BMP"
    )
    
    # Processa a imagem capturada ou enviada
    current_image = camera_image or uploaded_file
    
    if current_image is not None:
        # Mostra prévia da imagem
        st.image(current_image, caption="Imagem selecionada", use_column_width=True)
        
        # Processa a imagem
        image_data = process_image(current_image)
        if image_data:
            st.session_state.image_data = image_data
            st.session_state.uploaded_image = current_image
            st.success("✅ Imagem pronta para envio!")
        
        # Botão para limpar imagem
        if st.button("🗑️ Remover imagem", use_container_width=True):
            st.session_state.uploaded_image = None
            st.session_state.image_data = None
            st.rerun()
    
    elif st.session_state.uploaded_image is not None:
        # Mostra a imagem já carregada
        st.image(st.session_state.uploaded_image, caption="Imagem anexada", use_column_width=True)
        if st.button("🗑️ Remover imagem", use_container_width=True):
            st.session_state.uploaded_image = None
            st.session_state.image_data = None
            st.rerun()

    st.markdown("---")

    # Espaçador para empurrar os logos para o final
    // ...existing code...


# --- Interface Principal do Chat ---

# Header do Chat
st.markdown(f"### {assistant_info.name}")

# Indicador se há imagem anexada
if st.session_state.image_data:
    st.info("📷 Imagem anexada - será enviada com a próxima mensagem", icon="ℹ️")

# Exibe mensagens do histórico
if not st.session_state.messages:
    st.info(f"Como posso te ajudar hoje como {assistant_info.name}?", icon="👋")

for msg in st.session_state.messages:
    # Usa avatares customizados para replicar o visual
    avatar_img = (
        os.path.join(SCRIPT_DIR, "assets", "img", "user.png")
        if msg["role"] == "user"
        else os.path.join(SCRIPT_DIR, "assets", "img", "gpt.png")
    )
    with st.chat_message(msg["role"], avatar=avatar_img):
        # Se a mensagem tem imagem, mostra ela primeiro
        if "image" in msg:
            st.image(msg["image"], caption="Imagem enviada", width=300)
        st.markdown(msg["content"])


# Input do usuário (substitui o <textarea> e <button>)
if prompt := st.chat_input("Digite sua mensagem aqui..."):
    # Prepara o conteúdo da mensagem
    message_content = prompt
    message_data = {"role": "user", "content": message_content}
    
    # Se há imagem anexada, adiciona à mensagem
    if st.session_state.image_data:
        message_data["image"] = st.session_state.uploaded_image
        # Adiciona contexto sobre a imagem na mensagem
        message_content = f"[Imagem anexada] {prompt}"
    
    # Adiciona e exibe a mensagem do usuário
    st.session_state.messages.append(message_data)
    with st.chat_message(
        "user", avatar=os.path.join(SCRIPT_DIR, "assets", "img", "user.png")
    ):
        if st.session_state.image_data:
            st.image(st.session_state.uploaded_image, caption="Imagem enviada", width=300)
        st.markdown(prompt)
    
    # Prepara para receber a resposta do assistente
    with st.chat_message(
        "assistant", avatar=os.path.join(SCRIPT_DIR, "assets", "img", "gpt.png")
    ):
        # Se não houver um thread, cria um novo
        if not st.session_state.thread_id:
            try:
                thread = client.beta.threads.create()
                st.session_state.thread_id = thread.id
            except Exception as e:
                st.error(f"Erro ao criar a thread: {e}", icon="🚨")
                st.stop()

        try:
            # Prepara o conteúdo da mensagem para a API
            if st.session_state.image_data:
                # Mensagem com imagem para visão
                api_message_content = [
                    {
                        "type": "text",
                        "text": f"Analise esta imagem e responda: {prompt}"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": st.session_state.image_data,
                            "detail": "high"
                        }
                    }
                ]
            else:
                # Mensagem apenas texto
                api_message_content = prompt

            # Adiciona a mensagem do usuário à thread
            client.beta.threads.messages.create(
                thread_id=st.session_state.thread_id,
                role="user",
                content=api_message_content
            )

            # Cria o placeholder para a resposta em streaming
            response_placeholder = st.empty()

            # Inicializa o handler de streaming
            handler = StreamingEventHandler(response_placeholder)

            # Cria e faz o streaming da run
            with client.beta.threads.runs.stream(
                thread_id=st.session_state.thread_id,
                assistant_id=assistant_info.id,
                event_handler=handler,
            ) as stream:
                # O stream é processado pelo handler em tempo real
                stream.until_done()

            # Adiciona a resposta completa do assistente ao histórico
            assistant_response = handler.get_full_response()
            st.session_state.messages.append(
                {"role": "assistant", "content": assistant_response}
            )

            # Limpa a imagem após envio
            if st.session_state.image_data:
                st.session_state.uploaded_image = None
                st.session_state.image_data = None

        except Exception as e:
            st.error(
                f"Ocorreu um erro ao se comunicar com a API da OpenAI: {e}",
                icon="🚨",
            )
            # Remove a última mensagem do usuário para que ele possa tentar novamente
            st.session_state.messages.pop()