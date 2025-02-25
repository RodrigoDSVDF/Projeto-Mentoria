import time
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

# ========== BASE DE CONHECIMENTO ==========
MENTORIA_INFO = {
    "titulo": "Crie Uma Mentoria Lucrativa",
    "autor": "Instituto Vida FERA",
    "conteudo": {
        "topicos": [
            "O que é uma Mentoria de Alto Impacto?",
            "Por que criar uma mentoria agora?",
            "Passo 1: Encontrar seu nicho e diferencial",
            "Passo 2: Definir objetivos e metas com o método SMART",
            "Passo 3: Criar um plano de ação estruturado",
            "Passo 4: Construir sua marca pessoal",
            "Como monetizar e escalar sua mentoria",
            "Automação e IA para mentorias"
        ],
        "beneficios": [
            "Aceleração de resultados dos mentorados",
            "Fortalecimento da marca pessoal e autoridade",
            "Modelo escalável, permitindo atender mais clientes",
            "Uso de IA e automação para reduzir esforço",
            "Facilidade na estruturação e venda de mentorias",
            "Conversão de conhecimento em renda recorrente"
        ],
        "estrategias": [
            "Uso de redes sociais e tráfego pago",
            "Método SMART para definir metas",
            "Criação de uma página de vendas atrativa",
            "Modelos de atração e conversão de clientes",
            "Lançamento digital em até 35 dias"
        ]
    }
}

# ========== CLASSE PRINCIPAL ==========
class MentoriaFunnel:
    def __init__(self):
        self.llm_chain = LLMChain(
            llm=ChatOpenAI(
                model="gpt-4o-mini",
                temperature=0.7,
                openai_api_key=os.getenv("OPENAI_API_KEY")
            ),
            prompt=ChatPromptTemplate.from_messages([
                ("system",
                 f"""Você é o FERA Mentor, especialista no guia '{MENTORIA_INFO['titulo']}'.
                 Seu objetivo é ajudar e motivar o usuário a estruturar e vender sua mentoria.
                 Sempre destaque os benefícios da mentoria, como:
                 - Aceleração de resultados dos mentorados.
                 - Maior autoridade e posicionamento no mercado.
                 - Monetização escalável sem precisar trocar tempo por dinheiro.
                 - Uso de automação e IA para tornar o processo mais eficiente.

                 Guie a conversa para que o usuário entenda como a mentoria pode transformar seu conhecimento em um negócio lucrativo.
                 Após algumas interações, sugira um contato mais aprofundado via WhatsApp."""  
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
            ]),
            memory=ConversationBufferWindowMemory(
                memory_key="chat_history",
                input_key="input",
                k=5,
                return_messages=True
            )
        )

    def generate_response(self, user_input: str) -> str:
        response = self.llm_chain.invoke({"input": user_input})
        return response['text']

# ========== INTERFACE ==========
st.set_page_config(
    page_title=f"FERA Mentor - {MENTORIA_INFO['titulo']}",
    page_icon="📘",
    layout="centered"
)

# --- Imagem de Apresentação ---
st.image("Fera.jpeg", caption=MENTORIA_INFO['titulo'])

# Inicialização do chatbot na primeira execução
if "funnel" not in st.session_state:
    st.session_state.funnel = MentoriaFunnel()
    st.session_state.chat_history = []
    st.session_state.interaction_count = 0  # Contador de interações

# **Mensagem Inicial Fixa** (Aparece antes da interação do usuário)
if len(st.session_state.chat_history) == 0:
    with st.chat_message("AI"):
        st.write("📘 Olá! Sou o FERA Mentor, especialista em mentorias digitais! Qual é o seu nome?")

# Caixa de entrada do usuário
user_input = st.chat_input("Escreva sua pergunta sobre mentorias aqui...")

if user_input:
    st.session_state.chat_history.append(HumanMessage(content=user_input))
    st.session_state.interaction_count += 1  # Atualiza o contador de interações

    with st.chat_message("Human"):
        st.write(user_input)

    with st.chat_message("AI"):
        response = st.session_state.funnel.generate_response(user_input)
        response_placeholder = st.empty()
        full_response = ""

        for char in response:
            full_response += char
            response_placeholder.markdown(full_response)
            time.sleep(0.03)

    st.session_state.chat_history.append(AIMessage(content=full_response))

    # Exibir o link do WhatsApp após 5 interações
    if st.session_state.interaction_count >= 5:
        st.markdown("### 🚀 Quer criar sua mentoria de sucesso e transformar seu conhecimento em um negócio lucrativo?")
        st.markdown("Podemos te ajudar a estruturar um programa de alto impacto e vender de forma escalável!")
        st.link_button("Conversar no WhatsApp", "https://api.whatsapp.com/send?phone=5561991151740&text=Quero%20ajuda%20para%20estruturar%20minha%20mentoria!")
