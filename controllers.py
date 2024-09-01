# controllers.py
from database import Database


class Controller:
    def __init__(self):
        self.db = Database()

    def adicionar_cliente(self, nome, telefone, email):
        query = "INSERT INTO clientes (nome, telefone, email) VALUES (?, ?, ?)"
        self.db.execute_query(query, (nome, telefone, email))

    def adicionar_servico(self, nome):
        query = "INSERT INTO servicos (nome) VALUES (?)"
        self.db.execute_query(query, (nome,))

    def adicionar_agendamento(self, cliente_id, data, hora, servico_id):
        # Verifica se já existe um agendamento para o mesmo horário e data
        query_check = "SELECT * FROM agendamentos WHERE data = ? AND hora = ? AND cliente_id = ?"
        result = self.db.fetch_all(query_check, (data, hora, cliente_id))
        if result:
            raise Exception("Já existe um agendamento para este horário e data.")

        query = "INSERT INTO agendamentos (cliente_id, data, hora, servico_id, status) VALUES (?, ?, ?, ?, 'agendado')"
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

    def alterar_status_agendamento(self, agendamento_id, novo_status):
        query = "UPDATE agendamentos SET status = ? WHERE id = ?"
        self.db.execute_query(query, (novo_status, agendamento_id))