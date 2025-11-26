import streamlit as st
import re # Usado para formatação (máscara) de CPF/Telefone

# --- Funções de Máscara ---

# Função para remover caracteres não numéricos
def limpar_numero(numero):
    """Remove todos os caracteres não numéricos."""
    if numero is None:
        return ""
    return re.sub(r'\D', '', str(numero))

# Função para aplicar máscara de CPF (999.999.999-99)
def aplicar_mascara_cpf(cpf):
    """Aplica a máscara de CPF (999.999.999-99)."""
    numeros = limpar_numero(cpf)
    if len(numeros) <= 3:
        return numeros
    elif len(numeros) <= 6:
        return f"{numeros[:3]}.{numeros[3:]}"
    elif len(numeros) <= 9:
        return f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:]}"
    elif len(numeros) <= 11:
        return f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:9]}-{numeros[9:]}"
    return f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:9]}-{numeros[9:11]}" # Limita a 11 dígitos

# Função para aplicar máscara de Telefone (Ex: (99) 99999-9999 ou (99) 9999-9999)
def aplicar_mascara_telefone(tel):
    """Aplica a máscara de Telefone ((99) 99999-9999 ou (99) 9999-9999)."""
    numeros = limpar_numero(tel)
    if len(numeros) <= 2:
        return numeros
    elif len(numeros) <= 6:
        return f"({numeros[:2]}) {numeros[2:]}"
    elif len(numeros) <= 10: # Fixo (8 dígitos + 2 DDD)
        return f"({numeros[:2]}) {numeros[2:6]}-{numeros[6:]}"
    elif len(numeros) <= 11: # Celular (9 dígitos + 2 DDD)
        return f"({numeros[:2]}) {numeros[2:7]}-{numeros[7:]}"
    return f"({numeros[:2]}) {numeros[2:7]}-{numeros[7:11]}" # Limita a 11 dígitos


# --- Estrutura da Interface ---

st.set_page_config(layout="wide")

# Divisão principal em duas colunas (Sidebar verde e Área de Cadastro)
col_left, col_right = st.columns([1, 2.5], gap="large")

# --- Coluna da Esquerda (Sidebar Verde) ---
with col_left:
    st.markdown(
        """
        <style>
        .sidebar-nutriai {
            background-color: #00A693; /* Verde principal da NutriAi */
            padding: 30px;
            border-radius: 10px;
            height: 100vh; /* Ocupa a altura total da viewport */
            color: white;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
        }
        .header-nutriai {
            color: white;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 50px;
        }
        .welcome-text {
            margin-top: 50px;
            font-size: 20px;
        }
        .footer-text {
            margin-top: auto; /* Empurra para o rodapé */
            font-size: 14px;
        }
        </style>
        """, unsafe_allow_html=True
    )

    # Usa um container para aplicar o estilo CSS da sidebar
    with st.container():
        st.markdown('<div class="sidebar-nutriai">', unsafe_allow_html=True)
        st.markdown("←", unsafe_allow_html=True) # Ícone de voltar
        st.markdown('<div class="header-nutriai">NutriAi</div>', unsafe_allow_html=True)

        st.markdown(
            """
            <div class="welcome-text">
                Bem-vindo(a)!<br><br>
                Crie planos alimentares<br>
                personalizados para<br>
                suas necessidades e<br>
                viva com mais saúde.
            </div>
            """, unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="footer-text">
                Preencha os campos ao lado<br>
                e desfruta da ferramenta<br>
                criada especialmente para<br>
                você.
            </div>
            """, unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

# --- Coluna da Direita (Área de Cadastro) ---
with col_right:
    st.title("CADASTRO")

    # Inicializa o estado da aplicação (se é Paciente ou Nutricionista)
    if 'tipo_usuario' not in st.session_state:
        st.session_state.tipo_usuario = 'PACIENTE'

    # Botões de seleção (Paciente / Nutricionista)
    col_pat, col_nut, col_dummy = st.columns([1, 1.5, 5])

    # Estilo dos botões de seleção
    style_paciente = "background-color: #00A693; color: white;" if st.session_state.tipo_usuario == 'PACIENTE' else "background-color: #D3D3D3; color: black;"
    style_nutricionista = "background-color: #00A693; color: white;" if st.session_state.tipo_usuario == 'NUTRICIONISTA' else "background-color: #D3D3D3; color: black;"

    # Botão PACIENTE
    if col_pat.button("PACIENTE", key="btn_paciente", use_container_width=True):
        st.session_state.tipo_usuario = 'PACIENTE'
        st.rerun()

    # Texto "OU"
    col_nut.markdown("<p style='text-align: center; margin-top: 10px; font-weight: bold;'>OU</p>", unsafe_allow_html=True)

    # Botão NUTRICIONISTA
    if col_nut.button("NUTRICIONISTA", key="btn_nutricionista", use_container_width=True):
        st.session_state.tipo_usuario = 'NUTRICIONISTA'
        st.rerun()

    st.markdown("---")

    # --- Formulário de Cadastro ---
    st.subheader("1. DADOS PESSOAIS")
    st.markdown('<hr style="border: 4px solid #00A693; margin-top: -15px; margin-bottom: 20px; width: 300px;">', unsafe_allow_html=True) # Linha verde de destaque

    # Campos obrigatórios (Comuns a ambos)
    nome_completo = st.text_input("Nome Completo:", placeholder="Digite seu nome")
    
    col_cpf, col_telefone = st.columns(2)
    
    # Campo CPF com máscara em tempo real
    cpf_input = col_cpf.text_input("CPF:", placeholder="Digite seu CPF", max_chars=14)
    cpf_mascarado = aplicar_mascara_cpf(cpf_input)
    # Exibe o valor mascarado, mas armazena o valor bruto (apenas para exibição)
    if cpf_input and cpf_input != cpf_mascarado:
        col_cpf.text_input("CPF:", value=cpf_mascarado, disabled=True, label_visibility="hidden")
        
    # Campo Telefone com máscara em tempo real
    telefone_input = col_telefone.text_input("Telefone:", placeholder="Digite seu telefone", max_chars=15)
    telefone_mascarado = aplicar_mascara_telefone(telefone_input)
    # Exibe o valor mascarado
    if telefone_input and telefone_input != telefone_mascarado:
        col_telefone.text_input("Telefone:", value=telefone_mascarado, disabled=True, label_visibility="hidden")

    email = st.text_input("Email:", placeholder="Digite seu email")
    
    # --- Campos Específicos para Nutricionista ---
    if st.session_state.tipo_usuario == 'NUTRICIONISTA':
        col_crn, col_especialidade = st.columns(2)
        
        crn = col_crn.text_input("CRN:", placeholder="Digite seu CRN")
        
        especialidades = ["Selecione seu diagnóstico", "ONCOLOGIA", "ENDOCRINOLOGIA", "FUNCIONAL"]
        especialidade = col_especialidade.selectbox("Especialidade:", options=especialidades, index=0, help="Selecione sua área de especialização")
        
    # Campo Senha
    senha = st.text_input("Senha:", type="password", placeholder="Digite sua senha")

    # --- Botão e Links Finais ---
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Centraliza o botão de cadastro e o link
    st.markdown("""
        <style>
        .stButton>button {
            background-color: #00A693;
            color: white;
            font-weight: bold;
            padding: 10px 30px;
            border-radius: 5px;
            border: none;
            cursor: pointer;
        }
        </style>
    """, unsafe_allow_html=True)

    col_btn_center, col_login_center = st.columns([1, 10])

    if col_btn_center.button("CADASTRAR", key="btn_cadastro"):
        # Lógica de cadastro aqui
        st.success(f"Cadastro de {st.session_state.tipo_usuario} efetuado com sucesso (simulado)! Dados enviados.")
        
    st.markdown(
        """
        <div style="text-align: center; margin-top: 10px;">
            Já possui uma conta? <a href="#" style="color: #00A693; text-decoration: none; font-weight: bold;">ENTRAR</a>
        </div>
        """, unsafe_allow_html=True
    )
    
    
# --- Explicação do Código ---
st.sidebar.title("Notas sobre o Código")
st.sidebar.markdown(
    """
    Este código Streamlit utiliza as funções de **colunas** (`st.columns`) e **containers** (`st.container`) para simular o layout de duas colunas do seu design no Figma.

    * **Layout:** A coluna da esquerda (verde) usa **CSS Injectado** com `st.markdown(..., unsafe_allow_html=True)` para aplicar a cor de fundo e posicionar o texto, imitando o design fixo.
    * **Seleção de Usuário:** O estado do usuário (`PACIENTE` ou `NUTRICIONISTA`) é gerenciado com `st.session_state` e o clique nos botões recarrega o app (`st.rerun()`) para exibir os campos específicos do nutricionista (CRN e Especialidade).
    * **Máscaras:** As funções `aplicar_mascara_cpf` e `aplicar_mascara_telefone` usam expressões regulares (`re`) para formatar a entrada de texto, simulando o efeito de máscara.
    """
)