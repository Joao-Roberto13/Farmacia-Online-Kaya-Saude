import Email
import dataBase as db
import streamlit as st
from streamlit_option_menu import option_menu

def contact_form(mail):
    st.image("img_About.png",)
    
    st.write("""
        Somos uma farmácia online que combina tecnologia e atendimento humanizado para oferecer a você uma experiência de compra segura e eficiente.
        Trabalhamos com uma vasta gama de medicamentos, produtos de bem-estar e cuidados pessoais, sempre com foco na sua saúde.
        Nossa equipe de profissionais está comprometido em garantir que você receba o melhor atendimento, com suporte especializado e entrega rápida, onde quer que você esteja. 
        Além disso, nossa plataforma foi projetada para tornar o processo de encomenda simples e acessível, com uma interface intuitiva e serviços personalizados para atender às suas necessidades.

        \n\nTrazemos a saúde até a si, porque cuidar de você também é parte do nosso algoritmo.
    """)

    st.subheader("Missão", anchor=False)
    st.write("""Levar produtos farmacêuticos de qualidade até a sua casa, 
            com a rapidez e a segurança que você merece.""")
    
    st.subheader("Visão", anchor=False)
    st.write("""Ser referência no mercado de farmácias online,
            utilizando a tecnologia para facilitar o acesso à saúde, 
            sempre com foco no bem-estar do cliente.""")
    
    st.subheader("Valores", anchor=False)
    st.write(""" 
            - Cuidado: Colocamos sua saúde em primeiro lugar.
            - Inovação: Integramos a tecnologia para oferecer um serviço ágil e confiável.
            - Confiança: Trabalhamos com produtos certificados eatendimento transparente.
            - Proximidade: Mesmo online, estamos sempre perto de você.
        """)

    with st.form("contact_form",clear_on_submit=True,):
        email = mail
        mensagem = st.text_area("Digite a sua Mensagem",placeholder="Digite a sua mensagem....",label_visibility="collapsed")
        button = st.form_submit_button("Enviar")

        if button:
            Email.enviar_Email("farmaciakaya@gmail.com", mensagem, "Sobre",f"Enviado com sucesso, entraremos em contacto no Email: {email}")

def render(email):
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
    #st.markdown('<div class = "button-container">', unsafe_allow_html=True)

    button = option_menu (
        menu_title=None,
        options=["Pedidos","Encomendar","Sobre",],
        icons=["house","book","envelope"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
    )

    if button == "Encomendar":
        with st.form(key = "LogIn",clear_on_submit=True):
            descricao = st.selectbox("Selecione um Produto",db.medicamentos())
            quantidade = st.number_input("Introduza a quantidade.",min_value=1,max_value=15,step=1,format="%d") 
            pagamento = st.selectbox("Forma de Pagamento",['Seguradora','Carteira Movel(M-Pesa/E-Mola)','POS','Banco'])
            endereco = st.text_input("Endereço",placeholder="Introduza o seu endereço bem detalhado.",label_visibility="collapsed")
            buttonPedir = st.form_submit_button("Fazer Pedido")

            med = ""
            for item in descricao:
                med += item

            info = "Acaba de realizar uma encomenda na Farmacia Kaya de: \n\n"+med+\
            "\nQuantidade: "+str(quantidade)+\
            "\nForma de Pagamento: "+pagamento+\
            "\nPara o seguinte endereço: "+endereco+\
            "\n\nAguarde pela nossa confirmação.\n Atenciosamente Grupo Kaya"

        if buttonPedir:
            dado = ""
            for item in descricao:
                dado += item
            db.fazerEncomenda(email,dado,quantidade,pagamento,endereco)
            Email.enviar_Email(email, info, "Encomenda realizado com sucesso!","Encomenda realizado com sucesso!")

    if button == "Pedidos": #verificar pedidos passados...
        cols = st.columns((1, 1, 1, 2, 1, 1, 1, 1), vertical_alignment="center")
        campos = ['Data do Pedido','Descrição','Pagamento', 'Endereço','Estado','Quantidade','Valor','',''] 

        for col, campo in zip(cols, campos):
            col.write(campo)

        for item in db.selecionarPedidos(email):
            col1, col2, col3, col4, col5, col6, col7, col8 = st.columns((1, 1, 1, 2, 1, 1, 1, 1),vertical_alignment="center")

            col1.write(item.data)
            col2.write(item.descricao)
            col3.write(item.pagamento)
            col4.write(item.endereco)
            col5.write(item.estado)
            col6.write(item.quantidade)
            col7.write(item.valor)

            button_Excluir = col8.empty()#cria uma coluna vazia...
            on_click_Excluir = button_Excluir.button('Excluir', 'btnExluir'+str(item.id)) #Uma vez que o botao exluir estará para cada linha da tabela, o identificador btnExluir vamos concatenar com o id naquela posição para tornar unico

            if on_click_Excluir:
                db.excluirPedido(item.id)

    if button == "Sobre":
        contact_form(email)
