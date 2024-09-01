# controllers.py
from database import Database

class Controller:
    def __init__(self):
        self.db = Database()

    def adicionar_cliente(self, nome, telefone, email):
        query = "INSERT INTO clientes (nome, telefone, email) VALUES (?, ?, ?)"
        self.db.execute_query(query, (nome, telefone, email))

    def alterar_cliente(self, cliente_id, nome, telefone, email):
        query = "UPDATE clientes SET nome = ?, telefone = ?, email = ? WHERE id = ?"
        self.db.execute_query(query, (nome, telefone, email, cliente_id))

    def adicionar_servico(self, nome):
        query = "INSERT INTO servicos (nome) VALUES (?)"
        self.db.execute_query(query, (nome,))

    def adicionar_agendamento(self, cliente_id, data, hora, servico_id):
        query_check = "SELECT * FROM agendamentos WHERE data = ? AND hora = ? AND cliente_id = ?"
        result = self.db.fetch_all(query_check, (data, hora, cliente_id))
        if result:
            raise Exception("Já existe um agendamento para este horário e data.")

        query = "INSERT INTO agendamentos (cliente_id, data, hora, servico_id, status) VALUES (?, ?, ?, ?, 'Agendado')"
        self.db.execute_query(query, (cliente_id, data, hora, servico_id))

    def listar_agendamentos(self, limit=10, offset=0):
        query = """
            SELECT a.id, c.nome, a.data, a.hora, s.nome, a.status
            FROM agendamentos a
            JOIN clientes c ON a.cliente_id = c.id
            JOIN servicos s ON a.servico_id = s.id
            ORDER BY a.data DESC, a.hora DESC
            LIMIT ? OFFSET ?
        """
        return self.db.fetch_all(query, (limit, offset))

    def obter_agendamento(self, agendamento_id):
        query = "SELECT cliente_id, data, hora, servico_id, status FROM agendamentos WHERE id = ?"
        result = self.db.fetch_one(query, (agendamento_id,))
        if result:
            return result
        else:
            raise Exception("Agendamento não encontrado.")

    def atualizar_agendamento(self, agendamento_id, cliente_id, data, hora, servico_id, status):
        query = """
            UPDATE agendamentos
            SET cliente_id = ?, data = ?, hora = ?, servico_id = ?, status = ?
            WHERE id = ?
        """
        self.db.execute_query(query, (cliente_id, data, hora, servico_id, status, agendamento_id))
