import time
import kaya
import dataBase as db
from fpdf import FPDF
from PyQt5.QtCore import QTime, QTimer
from PyQt5 import uic, QtWidgets
from PyQt5 import uic, QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox, QApplication

def barra():
    cont = 0
    points = 0

    for i in range(100):
        cont += 1
        time.sleep(0.01)
        splash.progressBar.setValue(cont)
        splash.percentage.setText(str(cont) + "%")
        splash.status.setText("Status: Loading" + "." * points)
        
        #Para o qtwidgets funcionar ao mesmo tempo com o ciclo...
        QApplication.processEvents()
        
        #se o points for igual a 3, reinicia os pontos...
        if points == 3:
            points = 0
        points += 1

        if cont == 100:
            #Se a percentagem for 100% coloca Completed:) a cor verde....
            splash.status.setStyleSheet("QLabel { color: Green; }")
            splash.status.setText("Status: Completed :)")
            #Para não separar os eventos...
            QApplication.processEvents()
            #2segundos e fecha a tela de login e abre a main_tela...
            time.sleep(4)
            splash.close()
            screenLogin.setWindowFlag(QtCore.Qt.FramelessWindowHint)
            screenLogin.show()
            preencherTabela()

        elif cont in [10, 20, 30, 40, 50, 60]:
            time.sleep(0.31)
        elif cont in [15, 25, 35, 70, 79, 85, 90, 95]:
            time.sleep(0.07)
        elif cont in [ 2, 3, 22, 23, 31, 32, 41, 43, 70, 72, 73 , 91, 92, 93]:
            time.sleep(0.03)

def preencherTabela():
    #Para o qtwidgets funcionar ao mesmo tempo com o ciclo...
    QApplication.processEvents()
    dados_lidos = db.selecionarEstadoPedidos()



    screen.tableWidget.setRowCount(len(dados_lidos))
    screen.tableWidget.setColumnCount(8)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 8):
            screen.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j]))) 

def alterarEstado():
    tipo = screen.comboBox.currentText()
    id = screen.lineEdit_2.text()
    db.atualizarEstado(tipo,id)
    preencherTabela()

    screen.comboBox.setCurrentIndex(-1)
    screen.lineEdit_2.setText("")

def visualizarReceita():
    val = round(db.selecionarReceita(), 2)
    msg = "O Valor Total recebido é de: "+str(val)+" MZN..."
    QMessageBox.information(screen, "Receita", msg)
    preencherTabela()

def atualizarRelogio():
    hora = QTime.currentTime().toString('HH:mm:ss')
    screen.label_2.setText(hora)

def exportarPedidos():
    preencherTabela()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)

    pdf.cell(200, 10, txt="Relatório dos Pedidos", ln=True, align='C')

    pdf.cell(30, 10, txt="ID do Cliente", border=1)
    pdf.cell(30, 10, txt="Data", border=1)
    pdf.cell(30, 10, txt="Descrição", border=1)
    pdf.cell(30, 10, txt="Endereço", border=1)
    pdf.cell(30, 10, txt="Estado", border=1)
    pdf.cell(30, 10, txt="Quantidade", border=1)
    pdf.cell(30, 10, txt="Preço", border=1)

    resultado = db.selecionarTodosPedidos()

    for pedido in resultado:
        id = str(pedido[0])
        data = str(pedido[1])
        descricao = str(pedido[2])
        endereco = str(pedido[3])
        estado = str(pedido[4])
        quantidade = str(pedido[5])
        preco = str(pedido[6])

        pdf.cell(30, 10, txt=id, border=1)
        pdf.cell(30, 10, txt=data, border=1)
        pdf.cell(30, 10, txt=descricao, border=1)
        pdf.cell(30, 10, txt=endereco, border=1)
        pdf.cell(30, 10, txt=estado, border=1)
        pdf.cell(30, 10, txt=quantidade, border=1)
        pdf.cell(30, 10, txt=preco, border=1)
        pdf.ln()


    pdf.output("Relatorio_Pedidos.pdf")
    QMessageBox.information(screen,"Concluido","Pedidos Exportados com Sucesso!")

def novaCompra():
    med = screenCompra.comboBox.currentText()
    pay = screenCompra.comboBox_2.currentText()
    endereco = screenCompra.lineEdit.text()
    quantidade = screenCompra.spinBox.value() 

    db.fazerEncomenda("famaricakaya@gmail.com",med,quantidade,pay,endereco)
    QMessageBox.information(screen,"Done","Concluído!!!")

    screenCompra.close()
    preencherTabela()

def windowsCompra():
    screenCompra.show()
    d = db.medicamentos()
    screenCompra.comboBox.addItems(d)
    preencherTabela()

def update_clock():
    current_time = time.strftime('%H:%M:%S')
    screen.label_2.setText(current_time)

def ajuda():
    ajuda_text = (
        "Bem-vindo ao sistema de gestao de clientes da Farmacia Kaya!\n\n"
        "Para navegar pelo programa, utilize o menu lateral esquerdo.\n"
        "- Home: Acesse as principais funcionalidades.\n"
        "- Histórico: Veja o histórico de pedidos.\n"
        "- Stock: Gerencie o estoque de produtos.\n"
        "- Configurações: Ajuste as preferências do sistema.\n"
        "- Ajuda: Obtenha assistência sobre como usar o programa.\n"
        "- Sair: Feche o aplicativo.\n\n"
        "Clique nos botões correspondentes para interagir com cada seção."
    )
    QMessageBox.information(screen, "Ajuda",ajuda_text)

def historico():
    hist.show()
    dados_lidos = db.selecionarTodosPedidos()
    hist.tableWidget.setRowCount(len(dados_lidos))
    hist.tableWidget.setColumnCount(7)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 7):
            hist.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

def sair():
    app.closeAllWindows()

def login():
    user = screenLogin.lineEdit.text()
    password = screenLogin.lineEdit_2.text()

    if user == "20201234" and password == "1234":
        screenLogin.close()        
        screen.show()
        preencherTabela()
        
    else:
        QMessageBox.warning(screenLogin,"Incorreto!!!","Os dados introduzidos estão incorretos!!!")

def stock():
    screenStock.show()

def sobre():
    info = "Desenvolvido a 17 de setembro de 2024 por:\nMariamo Narotam-20220985\nMichelle Boane-20200266\nKeny Muchanga-20210410\nJoão Roberto-20220852"
    QMessageBox.information(screen,"Sobre",info)

# Configurando o GUI e conectando os botões as funções...
app = QtWidgets.QApplication([])
screen = uic.loadUi("InterfaceG.ui")
splash = uic.loadUi("splash_screen.ui")
screenCompra = uic.loadUi("InterfacePedido.ui")
screenLogin = uic.loadUi("InterfaceLogin.ui")
hist = uic.loadUi("interface_Historico.ui")
screenStock = uic.loadUi("interface_Stock.ui")

screen.pushButton_2.clicked.connect(alterarEstado)#Não aceita usar diretamente o preencherTabela então vamos usar alterarEstado que aceita...
screen.pushButton_3.clicked.connect(alterarEstado)
screen.pushButton_8.clicked.connect(visualizarReceita)
screen.actionSair.triggered.connect(lambda: app.closeAllWindows())
screen.actionPedidos_2.triggered.connect(exportarPedidos)
screen.pushButton_6.clicked.connect(windowsCompra)
screenCompra.pushButton_3.clicked.connect(novaCompra)
screenLogin.pushButton.clicked.connect(login)
screen.actionSobre_3.triggered.connect(sobre)


screen.pushButton_5.clicked.connect(ajuda)
screen.pushButton_7.clicked.connect(sair)
screen.pushButton.clicked.connect(historico)
screen.pushButton_4.clicked.connect(stock)

splash.setWindowFlag(QtCore.Qt.FramelessWindowHint)
splash.setAutoFillBackground(False)
splash.show()
barra()

timer = QtCore.QTimer()
timer.timeout.connect(update_clock)
timer.start(1000)

app.exec_()

