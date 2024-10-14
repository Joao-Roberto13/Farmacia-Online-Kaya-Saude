import mysql.connector
import hashlib
import Pedido

banco = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    passwd="@Junior2005",
    database="farmacia_kaya" )

def inserirCliente(cliente):
    cursor = banco.cursor()
    comando_SQL = "INSERT INTO cliente (`nome`, `email`, `contacto`, `cidade`, `regiao`,`senha`)  VALUES (%s,%s,%s,%s,%s,%s)"
    dados = (str(cliente.nome), str(cliente.email), str(cliente.contacto), str(cliente.cidade), str(cliente.regiao), str(cliente.password))
    cursor.execute(comando_SQL,dados)
    banco.commit()
    cursor.close()

def excluirPedido(id):
    cursor = banco.cursor()
    cursor.execute("DELETE FROM pedido WHERE pedido_id = %s",(id,))
    banco.commit()

def verificar_password(email, password):
        cursor = banco.cursor()
        cursor.execute('SELECT `senha` FROM cliente WHERE email = %s', (email,))
        dados_lidos = cursor.fetchone()
        cursor.close()   

        if dados_lidos:
            input_senha_criptografada = hashlib.sha256(password.encode()).hexdigest() #criptografa a senha inserida para ver se é igual...
            if dados_lidos[0] == input_senha_criptografada:
            #if dados_lidos[0] == password:
                return True
            else:
                return False
        else:
            return False

def medicamentos():
    cursor = banco.cursor()
    cursor.execute('SELECT nome FROM produto')
    dados_lidos = cursor.fetchall()
    cursor.close()

    dados = [item[0] for item in dados_lidos]

    return dados

def fazerEncomenda(email,descricao, quantidade, pagamento, endereco):
    cursor = banco.cursor()
    cursor.execute("SELECT id FROM cliente WHERE email = %s", (email,))
    id = cursor.fetchone()
    id = id[0]
    comando_SQL = "INSERT INTO pedido (cliente_id, descricao, pagamento, endereco, estado, quantidade)  VALUES (%s,%s,%s,%s,%s,%s)"
    dados = (id, str(descricao), str(pagamento), str(endereco), str("N/A"), str(quantidade))
    cursor.execute(comando_SQL,dados)
    banco.commit()
    cursor.close()

def selecionarPedidos(email):
    cursor = banco.cursor() 
    cursor.execute("SELECT * FROM farmacia_kaya.pedido where pedido.cliente_id = (SELECT cliente.id from farmacia_kaya.cliente where cliente.email = %s) ORDER BY pedido.data DESC",(email,))
    dados_lidos = cursor.fetchall()
    cursor.close()

    lista = []
    for row in dados_lidos:
        lista.append(Pedido.Pedido(row[0],row[2],row[3],row[4],row[5],row[6],row[7],row[8]))

    return lista

def selecionarTodosProdutos():
    cursor = banco.cursor() 
    cursor.execute("SELECT * FROM produto")
    dados_lidos = cursor.fetchall()
    cursor.close()

    """lista = []
    for row in dados_lidos:
        lista.append(Produto.Produto(row[1],row[2],row[3],row[4],row[5],row[6]))"""


    return dados_lidos

def selecionarTodosClientes():
    cursor = banco.cursor() 
    cursor.execute("SELECT nome, email, contacto, cidade, regiao FROM cliente")
    dados_lidos = cursor.fetchall()
    cursor.close()

    return dados_lidos

def selecionarTodosPedidos():
    cursor = banco.cursor() 
    cursor.execute("SELECT data, descricao, pagamento, endereco, estado, quantidade, preco_unitario FROM pedido")
    dados_lidos = cursor.fetchall()
    cursor.close()

    return dados_lidos

def selecionarEstadoPedidos():
    cursor = banco.cursor() 
    cursor.execute("SELECT pedido_id, data, descricao, pagamento, endereco, estado, quantidade, preco_unitario FROM pedido WHERE estado <> 'Recebido' ORDER BY estado")
    dados_lidos = cursor.fetchall()
    cursor.close()

    return dados_lidos

def atualizarEstado(tipo, id):
    cursor = banco.cursor()
    comando = "UPDATE pedido SET  estado = %s WHERE pedido_id = %s;"
    valores = (tipo,id)
    cursor.execute(comando, valores)
    banco.commit()

def selecionarReceita():
    cursor = banco.cursor()
    cursor.execute("SELECT sum(preco_unitario) FROM pedido;")
    dados_lidos = cursor.fetchall()
    cursor.close()

    dados_lidos = dados_lidos[0][0]
    return dados_lidos
