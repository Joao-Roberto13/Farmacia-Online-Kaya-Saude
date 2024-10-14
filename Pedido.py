class Pedido:
    def __init__(self, id,data, descricao, pagamento, endereco, estado, quantidade, valor):
        self.id = id
        self.data = data
        self.descricao = descricao
        self.pagamento = pagamento
        self.endereco =  endereco
        self.estado = estado
        self.quantidade = quantidade
        self.valor = valor

