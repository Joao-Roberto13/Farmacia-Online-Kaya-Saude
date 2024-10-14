import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
import dataBase as db
import time

target = 15000

def render():
    st.subheader("🔔 Visão Geral da Farmácia")

    #Todas infos da SideBar 
    st.sidebar.image("Farmacia Kaya.png")
    st.sidebar.subheader("")
    with st.sidebar:
        selected = option_menu(
            menu_title="MENU",
            options=["Home","Progresso"],
            icons=["house","eye"],
            menu_icon="cast",
            default_index=0
        )

    #Pega os dados do cliente da BD...
    resultCliente = db.selecionarTodosClientes()
    resultPedido = db.selecionarTodosPedidos()
    resultProduto = db.selecionarTodosProdutos()

    dfC = pd.DataFrame(resultCliente, columns=["Nome","Email","Contacto","Cidade","Região"])
    dfP = pd.DataFrame(resultPedido, columns=["Data", "Descrição", "Pagamento", "Endereço", "Estado", "Quantidade", "Valor"])
    dfProd = pd.DataFrame(resultProduto, columns = ["ID","Nome","Tipo","Via de Administração","Prescrição","Stock","Valor"])

    with st.sidebar.expander("Filtrar Dados"):
        #Adicionando Switcher a sidebar...
        st.write("Quantidade de Clientes:")
        regiao = st.multiselect("Selecione a região", options=dfC["Região"].unique(), default=dfC["Região"].unique())
        cidade = st.multiselect("Selecione a Cidade", options=dfC["Cidade"].unique(), default=dfC["Cidade"].unique())

        st.write("Quantidade de Pedidos/Valor")
        estado = st.multiselect("Selecione o estado", options=dfP["Estado"].unique(), default=dfP["Estado"].unique())
        pagamento = st.multiselect("Selecione o pagamento", options=dfP["Pagamento"].unique(), default=dfP["Pagamento"].unique())

    #Vai para a query que é usada para criar a BD e filtra...
    selecionadoCliente = dfC.query("Região==@regiao & Cidade==@cidade")#O @cidade é para indicar variavel...

    #Vai para a query que é usada para criar a BD e filtra...
    selecionadoPedido = dfP.query("Estado==@estado & Pagamento==@pagamento")

    def Home():    
        totalPago = selecionadoPedido["Valor"].astype(float).sum()
        totalPagoMedia = selecionadoPedido["Valor"].astype(float).mean()
        quantPedidos = selecionadoPedido["Data"].count()
        quantClientes = selecionadoCliente["Nome"].count()
        
        total1,total2,total3,total4 = st.columns(4,gap='large')

        with total1:
            st.info("Valor Total",icon="📌")
            st.metric("Valor recebido em MZN",value=numerize(totalPago),help = f""" Valor total que foi recebido em vendas. {totalPago} Meticais""")

        with total2:
            st.info("Média",icon="📌")
            st.metric("Valor medio em MZN",value=f"{totalPagoMedia:,.2f}",help=f""" Média do valor recebido {totalPagoMedia:,.2f} Meticais""")
        
        with total3:
            st.info("Clientes",icon="📌")
            st.metric("Clientes da Farmacia",value = f""" {numerize(float(quantClientes))} """, help = f"""Quantidade de clientes inscritos na Farmácia Kaya: {quantClientes} """)

        with total4:
            st.info("Pedidos",icon="📌")
            st.metric("Pedidos da Farmacia",value = f""" {numerize(float(quantPedidos))} """, help = f""" Quantidade de pedidos/encomendas feitos a Farmácia Kaya: {quantPedidos} """)

        with st.expander(label="Clientes"):
            dados = st.multiselect("Filtrar: ",selecionadoCliente.columns,default=["Nome","Email","Contacto","Cidade","Região"])
            st.write(selecionadoCliente[dados])
        
        with st.expander("Pedidos"):
            dados = st.multiselect("Filtrar: ",selecionadoPedido.columns,default=["Data", "Descrição", "Pagamento", "Endereço", "Estado", "Quantidade", "Valor"])
            st.write(selecionadoPedido[dados])

    def progressBar():
        st.markdown("""<style>.stProgress > div > div > div > div { background-image: linear-gradient(to right, rgb(229, 63, 99), rgb(114, 232, 210))} </style>""",unsafe_allow_html=True )
        global target
        current = selecionadoPedido["Valor"].sum()
        percent = round((current/target*100))
        bar = st.progress(0)

        if percent>= 100:
            st.subheader("Meta Alcançada!")
        else:
            st.write("Meta da Farmácia: ",percent,"% ","concluída de ", numerize(target), "MZN...")
            for x in range(percent):
                time.sleep(0.1)
                bar.progress(x+1)

    def graficos():
        col1, col2 = st.columns(2)
        col3, col4, col5 =st.columns(3)

        graficoDataValor = px.bar(selecionadoPedido, x="Data", y="Valor", color="Estado", title="Faturação por Dia")
        col1.plotly_chart(graficoDataValor, use_container_width=True)

        graficoTipoProduto = px.bar(dfProd, x="Valor", y="Via de Administração", color="Tipo", orientation="h",title="Faturação por Via de Administração")
        col2.plotly_chart(graficoTipoProduto, use_container_width=True)

        df_quantC = selecionadoCliente['Região'].value_counts().reset_index()
        df_quantC.columns = ['Região','Quantidade']
        graficoCliente = px.bar(df_quantC, x="Quantidade", y="Região", orientation="h", title="Quantidade de Clientes por Região")
        col3.plotly_chart(graficoCliente, use_container_width=True)

        graficoTipoPagamento = px.pie(selecionadoPedido, values="Valor", names="Pagamento", title="Faturação por Tipo de Pagamento")
        col4.plotly_chart(graficoTipoPagamento, use_container_width=True)

        df_quantP = selecionadoPedido.groupby('Data').size().reset_index(name='Quantidade')
        df_quantP = df_quantP.sort_values(by="Data")
        #df_quantP.columns = ["Data","Quantidade"]
        gradicoDataPedido = px.line(df_quantP, x = "Data", y = "Quantidade", title="Pedidos Por dia")
        col5.plotly_chart(gradicoDataPedido, use_container_width=True)

    #Tratametno dos botoes do menu...
    if selected == "Home":
        Home()
        #graficos()
    if selected == "Progresso":
        progressBar()
        graficos()

