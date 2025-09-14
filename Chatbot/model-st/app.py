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
        if hasattr(image_file, "read"):
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

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Define a configuração da página
st.set_page_config(
    page_title="Agente Comercial",
    page_icon=os.path.join(SCRIPT_DIR, "assets", "img", "NDados.png"),
    layout="centered",
    initial_sidebar_state="expanded",
)

# Aplica o CSS customizado diretamente
st.markdown(
    """
<style>
/* Importa fontes personalizadas */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Variáveis CSS personalizadas */
:root {
    --primary-purple: #8c52ff;
    --purple-light: #a06eff;
    --purple-dark: #6b3acc;
    --purple-ultra-light: rgba(140, 82, 255, 0.1);
    --purple-semi-light: rgba(140, 82, 255, 0.2);
    --background-gradient: linear-gradient(135deg, #f8f7ff 0%, #f0ebff 100%);
}

/* Fundo principal com padrão de dados */
.main .block-container {
    background: var(--background-gradient);
    position: relative;
    font-family: 'Inter', sans-serif;
    color: #333333;
}

.main .block-container::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: 
        /* Padrão de dados/pontos pequenos */
        radial-gradient(circle at 10% 10%, var(--purple-ultra-light) 1px, transparent 1px),
        radial-gradient(circle at 30% 20%, var(--purple-ultra-light) 1.5px, transparent 1.5px),
        radial-gradient(circle at 50% 15%, var(--purple-ultra-light) 1px, transparent 1px),
        radial-gradient(circle at 70% 25%, var(--purple-ultra-light) 2px, transparent 2px),
        radial-gradient(circle at 90% 10%, var(--purple-ultra-light) 1px, transparent 1px),
        radial-gradient(circle at 85% 30%, var(--purple-ultra-light) 1.5px, transparent 1.5px),
        
        /* Segunda camada de dados */
        radial-gradient(circle at 15% 40%, var(--purple-ultra-light) 1px, transparent 1px),
        radial-gradient(circle at 35% 45%, var(--purple-ultra-light) 2px, transparent 2px),
        radial-gradient(circle at 55% 35%, var(--purple-ultra-light) 1px, transparent 1px),
        radial-gradient(circle at 75% 50%, var(--purple-ultra-light) 1.5px, transparent 1.5px),
        radial-gradient(circle at 95% 45%, var(--purple-ultra-light) 1px, transparent 1px),
        
        /* Terceira camada de dados */
        radial-gradient(circle at 20% 70%, var(--purple-ultra-light) 2px, transparent 2px),
        radial-gradient(circle at 40% 65%, var(--purple-ultra-light) 1px, transparent 1px),
        radial-gradient(circle at 60% 75%, var(--purple-ultra-light) 1.5px, transparent 1.5px),
        radial-gradient(circle at 80% 70%, var(--purple-ultra-light) 1px, transparent 1px),
        
        /* Quarta camada de dados */
        radial-gradient(circle at 25% 90%, var(--purple-ultra-light) 1px, transparent 1px),
        radial-gradient(circle at 45% 95%, var(--purple-ultra-light) 1.5px, transparent 1.5px),
        radial-gradient(circle at 65% 85%, var(--purple-ultra-light) 1px, transparent 1px),
        radial-gradient(circle at 85% 95%, var(--purple-ultra-light) 2px, transparent 2px),
        
        /* Linhas sutis conectando dados */
        linear-gradient(45deg, transparent 45%, var(--purple-ultra-light) 47%, var(--purple-ultra-light) 48%, transparent 50%),
        linear-gradient(-45deg, transparent 45%, var(--purple-ultra-light) 47%, var(--purple-ultra-light) 48%, transparent 50%);
    
    background-size: 
        /* Tamanhos variados para simular dados dispersos */
        80px 80px, 120px 120px, 90px 90px, 110px 110px, 70px 70px, 100px 100px,
        95px 95px, 130px 130px, 85px 85px, 105px 105px, 75px 75px,
        140px 140px, 80px 80px, 115px 115px, 90px 90px,
        125px 125px, 95px 95px, 85px 85px, 135px 135px,
        /* Linhas de conexão */
        200px 200px, 180px 180px;
    
    background-position: 
        /* Posições aleatórias para simular distribuição de dados */
        0 0, 25px 25px, 50px 15px, 75px 35px, 100px 10px, 125px 30px,
        15px 40px, 45px 60px, 70px 45px, 95px 65px, 120px 50px,
        20px 80px, 50px 75px, 80px 85px, 110px 80px,
        30px 100px, 60px 105px, 90px 95px, 120px 110px,
        /* Linhas */
        0 0, 100px 100px;
    
    opacity: 0.4;
    z-index: -1;
    pointer-events: none;
}

/* Adiciona padrão extra de dados flutuantes */
.main .block-container::after {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: 
        /* Pequenos quadrados e retângulos representando dados */
        linear-gradient(45deg, var(--purple-ultra-light) 2px, transparent 2px),
        linear-gradient(-45deg, var(--purple-ultra-light) 1px, transparent 1px),
        /* Círculos maiores ocasionais */
        radial-gradient(circle at 33% 33%, var(--purple-ultra-light) 3px, transparent 3px),
        radial-gradient(circle at 66% 66%, var(--purple-ultra-light) 2.5px, transparent 2.5px);
    background-size: 150px 150px, 180px 180px, 300px 300px, 250px 250px;
    background-position: 0 0, 50px 50px, 75px 75px, 125px 125px;
    opacity: 0.2;
    z-index: -2;
    pointer-events: none;
}

/* Remove a borda padrão do topo do header */
header[data-testid="stHeader"] {
    border-top: none;
    background: linear-gradient(90deg, var(--primary-purple), var(--purple-light));
    height: 4px;
}

/* Estilização da sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffffff 0%, #faf9ff 100%);
    border-right: 2px solid var(--purple-ultra-light);
}

section[data-testid="stSidebar"] > div {
    background: transparent;
}

/* Força texto escuro em todos os elementos */
.stApp {
    color: #333333 !important;
}

/* Botões personalizados */
.stButton > button {
    background: linear-gradient(135deg, var(--primary-purple), var(--purple-light));
    color: white !important;
    border: none;
    border-radius: 12px;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(140, 82, 255, 0.3);
}

.stButton > button:hover {
    background: linear-gradient(135deg, var(--purple-dark), var(--primary-purple));
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(140, 82, 255, 0.4);
}

/* Selectbox personalizado */
.stSelectbox > div > div {
    background-color: white;
    border: 2px solid var(--purple-ultra-light);
    border-radius: 10px;
    transition: border-color 0.3s ease;
    color: #333333 !important;
}

.stSelectbox > div > div:focus-within {
    border-color: var(--primary-purple);
    box-shadow: 0 0 0 3px var(--purple-ultra-light);
}

/* Estiliza os containers das mensagens para se parecerem com os balões de chat */
[data-testid="stChatMessage"] {
    background: rgba(255, 255, 255, 0.9);
    border: 1px solid var(--purple-ultra-light);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 20px rgba(140, 82, 255, 0.1);
    transition: all 0.3s ease;
    color: #333333 !important;
}

[data-testid="stChatMessage"]:hover {
    box-shadow: 0 6px 25px rgba(140, 82, 255, 0.15);
    transform: translateY(-1px);
}

/* Mensagens do usuário */
[data-testid="stChatMessage"]:has(img[alt*="user"]) {
    background: linear-gradient(135deg, var(--primary-purple), var(--purple-light));
    color: white !important;
    margin-left: 2rem;
}

/* Mensagens do assistente */
[data-testid="stChatMessage"]:has(img[alt*="assistant"]) {
    background: rgba(255, 255, 255, 0.95);
    margin-right: 2rem;
    color: #333333 !important;
}

/* Estilo para avatares */
img[data-testid="stAvatar"] {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: 2px solid var(--primary-purple);
    box-shadow: 0 2px 10px rgba(140, 82, 255, 0.3);
}

/* Input de chat personalizado */
.stChatInput > div {
    background: white;
    border: 2px solid var(--purple-ultra-light);
    border-radius: 15px;
    transition: all 0.3s ease;
}

.stChatInput > div:focus-within {
    border-color: var(--primary-purple);
    box-shadow: 0 0 0 3px var(--purple-ultra-light);
}

/* Títulos personalizados */
h1, h2, h3 {
    color: var(--purple-dark) !important;
    font-family: 'Inter', sans-serif;
    font-weight: 700;
}

/* Texto geral */
p, div, span, label {
    color: #333333 !important;
}

/* Alertas e notificações */
.stAlert {
    background: rgba(255, 255, 255, 0.9);
    border-left: 4px solid var(--primary-purple);
    border-radius: 10px;
    backdrop-filter: blur(10px);
    color: #333333 !important;
}

/* Scrollbar personalizada */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: var(--purple-ultra-light);
}

::-webkit-scrollbar-thumb {
    background: var(--primary-purple);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--purple-dark);
}

/* Animação de loading */
@keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.6; }
    100% { opacity: 1; }
}

.loading-text {
    animation: pulse 1.5s ease-in-out infinite;
}

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

try:
    # Inicializa o cliente OpenAI usando as secrets do Streamlit
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception as e:
    st.error(
        "Chave da API da OpenAI não encontrada. Por favor, configure seus secrets no Streamlit Cloud.",
        icon="🚨",
    )
    st.stop()

# --- Inicialização do Estado da Sessão ---
# O st.session_state é o equivalente do Streamlit ao localStorage ou variáveis de classe do JS

if "session_id" not in st.session_state:
    st.session_state.session_id = (
        f"session_{int(time.time())}"  # ID único para a sessão
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

if "assistant_key" not in st.session_state:
    st.session_state.assistant_key = DEFAULT_ASSISTANT

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
    assistant_options = {
        key: assistant.name for key, assistant in AVAILABLE_ASSISTANTS.items()
    }

    selected_assistant_key = st.selectbox(
        label="🤖 Assistente:",
        options=assistant_options.keys(),
        format_func=lambda key: assistant_options[key],
        key="selected_assistant",
    )

    # Lógica para confirmar mudança de assistente no meio da conversa
    if selected_assistant_key != st.session_state.assistant_key:
        if st.session_state.messages:  # Se já houver mensagens
            st.warning("Mudar de assistente irá iniciar uma nova conversa.", icon="⚠️")
            if st.button("Confirmar e iniciar nova conversa", use_container_width=True):
                st.session_state.assistant_key = selected_assistant_key
                st.session_state.messages = []
                st.session_state.thread_id = None
                st.rerun()
        else:
            # Se não houver mensagens, apenas muda o assistente
            st.session_state.assistant_key = selected_assistant_key
            st.rerun()

    # Exibe a descrição do assistente selecionado
    assistant_info = AVAILABLE_ASSISTANTS[st.session_state.assistant_key]
    st.markdown(
        f"<small>*{assistant_info.description}*</small>", unsafe_allow_html=True
    )

    st.markdown("---")

    # Seção de upload de imagem
    st.header("📷 Anexar Imagem")

    # Componente para captura de câmera (funciona melhor em dispositivos móveis)
    camera_image = st.camera_input("📸 Capturar da câmera")

    # Upload de arquivo de imagem
    uploaded_file = st.file_uploader(
        "📁 Ou escolher da galeria",
        type=["png", "jpg", "jpeg", "gif", "bmp"],
        help="Formatos suportados: PNG, JPG, JPEG, GIF, BMP",
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
        st.image(
            st.session_state.uploaded_image,
            caption="Imagem anexada",
            use_column_width=True,
        )
        if st.button("🗑️ Remover imagem", use_container_width=True):
            st.session_state.uploaded_image = None
            st.session_state.image_data = None
            st.rerun()

    st.markdown("---")

    # Espaçador para empurrar os logos para o final
    st.markdown("<br>" * 5, unsafe_allow_html=True)

    # Centralizando os logos em uma coluna
    logo_col1, logo_col2, logo_col3 = st.columns([1, 2, 1])

    with logo_col2:
        # Container para posicionamento diagonal
        st.markdown(
            """
            <div style="position: relative; display: flex; justify-content: center;">
                <img src="data:image/png;base64,{}" width="100" />
                <img src="data:image/png;base64,{}" width="60" 
                     style="position: absolute; bottom: -30px; right: -40px;" />
            </div>
            """.format(
                base64.b64encode(
                    open(
                        os.path.join(SCRIPT_DIR, "assets", "img", "NDados.png"), "rb"
                    ).read()
                ).decode(),
                base64.b64encode(
                    open(
                        os.path.join(SCRIPT_DIR, "assets", "img", "Poli Junior.png"),
                        "rb",
                    ).read()
                ).decode(),
            ),
            unsafe_allow_html=True,
        )

    st.markdown(
        "<small>🚀 Agente Comercial - NDados & Poli Junior </small>",
        unsafe_allow_html=True,
    )

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
            st.image(
                st.session_state.uploaded_image, caption="Imagem enviada", width=300
            )
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
                        "text": f"Analise esta imagem e responda: {prompt}",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": st.session_state.image_data,
                            "detail": "high",
                        },
                    },
                ]
            else:
                # Mensagem apenas texto
                api_message_content = prompt

            # Adiciona a mensagem do usuário à thread
            client.beta.threads.messages.create(
                thread_id=st.session_state.thread_id,
                role="user",
                content=api_message_content,
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
