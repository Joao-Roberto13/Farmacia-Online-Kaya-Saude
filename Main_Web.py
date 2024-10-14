import Email, smtplib,hashlib, re
import dataBase as db
import streamlit as st
import HomePage, Cliente, Manager  # Importa o arquivo HomePage
from streamlit_option_menu import option_menu
from mysql.connector import errorcode
import mysql.connector

st.set_page_config(page_title="Kaya Saúde",page_icon="💊",layout="wide")

# Configuração da página principal
st.markdown("<h1 style='text-align: center; font-family: Times New Roman;'>Farmacia Kaya</h1>", unsafe_allow_html=True)

st.markdown("""<style>
                .button-container {
                    display: flex;
                    justify-content: space-between;
                    width: 100%;
                }
                
                .stButton button {
                    width: 100%;
                    padding: 10px;
                    font_size: 16px;
                }
            </style>""",unsafe_allow_html=True)

# Função para validar e-mails
def valid_email(email):
    padrao = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(padrao, email) is not None

# Função para validar os dados de registro
def validate_registration(name, email, contacto, password1, password2):
    if len(name) == 0 or len(email) == 0 or len(contacto) == 0 or len(password1) == 0:
        return "Considere preencher os campos restantes!"
    if len(name) < 8:
        return "Forneça o seu nome completo."
    if len(email) < 14:
        return "Por favor, forneça o seu endereço de email."
    if not valid_email(email):
        return "Forneça um endereço de email válido."
    if len(contacto) != 9:
        return "Verifique o seu número de telefone."
    if len(password1) < 5:
        return "A senha deve ter pelo menos 5 dígitos!"
    if password1 != password2:
        return "As senhas não coincidem. Tente novamente!"
    return None  # Tudo válido

# Função para processar o login
def login_form():
    with st.form(key="LogIn",clear_on_submit=True):
        email = st.text_input(label="Introduza o email",placeholder="Introduza o seu email...",label_visibility="collapsed").lower()
        password = st.text_input(label="Introduza o password", type="password",placeholder="Introduza o seu password...",label_visibility="collapsed")
        
        if st.form_submit_button("Entrar"):
            if db.verificar_password(email, password):
                st.session_state["email"] = email
                st.session_state.page = "loggedIn"
                st.success("Clique Entrar Novamente!🎉", icon="🚀")
            else:
                st.error("Incorreto, Tente Novamente!")

def managerForm():
    id_gestor = st.text_input("ID do Gestor", type="password")
    if st.button("Entrar"):
        if id_gestor == "12345":
            st.session_state.page = "Gestor"
            st.success("Clique Entrar Novamente!🎉", icon="🚀")

#retorna de que regiao é essa provincia...
def regiaodaProvincia(provincia):
    sul = ["Maputo", "Gaza", "Inhambane", "Cidade de Maputo"]
    centro = ["Zambézia", "Tete", "Manica", "Sofala"]
    norte = ["Niassa", "Cabo Delgado", "Nampula"]

    if provincia in sul:
        return "Sul"
    elif provincia in norte:
        return "Norte"
    elif provincia in centro:
        return "Centro"

# Função para processar o registro
def sign_in_form():
    with st.form(key="include_cliente"):
        name = st.text_input("nome",label_visibility="collapsed",placeholder="Introduza o seu nome...")
        email = st.text_input("email",label_visibility="collapsed",placeholder="Endereço de email (testemail@gmail.com)...").lower()
        contacto = st.text_input("numero de telefone",label_visibility="collapsed",placeholder="Numero de Telefone (Ex: 841234567)...")
        cidade = st.selectbox("Selecione a sua Provincia",["Cidade de Maputo", "Maputo", "Gaza", "Inhambane",
        "Manica", "Sofala", "Zambézia", "Tete", "Niassa", "Nampula", "Cabo Delgado"],label_visibility="collapsed",placeholder="Selecione a sua Provincia")
        password1 = st.text_input("password",label_visibility="collapsed",placeholder="Introduza o password", type="password")
        password2 = st.text_input("password",label_visibility="collapsed",placeholder="Confirme o password", type="password")
        register_submit_button = st.form_submit_button("Salvar")

    if register_submit_button:
        error = validate_registration(name, email, contacto, password1, password2)
        if error:
            st.error(error, icon="😵")
            st.session_state.clear()
            st.stop()

        try:
            # Armazenando os dados do cliente
            Cliente.nome = name
            Cliente.email = email
            Cliente.contacto = contacto
            Cliente.cidade = cidade
            Cliente.regiao = regiaodaProvincia(cidade)
            Cliente.password = hashlib.sha256(password1.encode()).hexdigest()  # Criptografa a senha
            db.inserirCliente(Cliente)

            info = f"""Bem Vindo(a) {name},\nObrigado(a) por se registar na Farmárcia Kaya!
    Estamos entusiamados em tê-lo(a) como parte da nossa comunidade.\nAqui estão os detalhes do seu registo:\n
            Nome: {name}
            email: {email}
            Contacto: {contacto}

    Se precisar de ajuda ou tiver alguma dúvida, nossa equipe está a disposição. 
    Basta responder a este email ou visitar a nossa página de suporte.

    Seja bem-vindo(a)!
    Atenciosamente,
    Grupo Kaya Saúde"""

            Email.enviar_Email(email, info, "Bem-Vindo(a) a Farmacia Kaya!\nConfirmacao de Registo","Conta criada com sucesso.")
            st.success("Submetido com sucesso! 🎉", icon="🚀")

        except smtplib.SMTPAuthenticationError:  
            st.session_state.clear() 
            st.error("Erro de autenticação: por favor, verifique as credenciais de email.",icon="🔑")

        except smtplib.SMTPConnectError: 
            st.session_state.clear()
            st.error("Erro de conexão: não foi possível conectar ao servidor SMTP.",icon="🌍")

        except smtplib.SMTPException as e: 
            st.session_state.clear()
            st.error(f"Ocorreu um erro durante o envio do e-mail: {str(e)}",icon="📧")

        except mysql.connector.Error as e:
            st.session_state.clear()
            if e.errno == errorcode.ER_DUP_ENTRY:
                st.error(" ERRO: o Email ou número do telefone já está registrado.", icon="⚠️")
            else:
                st.error(f"Ocorreu um erro: {str(e)}", icon="😨")

def isLogged():
    # Verifica se o usuário está logado...
    if "page" in st.session_state and st.session_state.page == "loggedIn":
        if "email" in st.session_state:
            HomePage.render(st.session_state["email"])
        else:
            st.write("Não há e-mail no estado da sessão.")
    elif "page" in st.session_state and st.session_state.page == "Gestor":
        Manager.render()
    else:
        # Menu de navegação só é mostrado se o usuário não estiver logado
        button = option_menu(
            menu_title=None, 
            options=["LogIn", "SignIn", "Gestor"],
            icons=["house", "book", "person"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal",
        )
        # Lógica para o botão de LogIn
        if button == "LogIn":
            login_form()  # Chama o formulário de login

        # Lógica para o botão de SignIn
        if button == "SignIn":
            sign_in_form()  # Chama o formulário de cadastro

        # Lógica para o botão de Gestor
        if button == "Gestor":
            managerForm()

# Chama a função principal para exibir o conteúdo apropriado
isLogged()
