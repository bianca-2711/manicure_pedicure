import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from controllers import Controller


class App:
    def __init__(self, root):
        self.controller = Controller()
        self.root = root
        self.root.title("Sistema de Manicure/Pedicure")
        self.root.geometry("800x600")

        self.create_menu()
        self.create_main_screen()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)

        menu_cliente = tk.Menu(menu_bar, tearoff=0)
        menu_cliente.add_command(label="Cadastrar Cliente", command=self.cadastrar_cliente)
        menu_bar.add_cascade(label="Cadastro de Clientes", menu=menu_cliente)

        menu_servico = tk.Menu(menu_bar, tearoff=0)
        menu_servico.add_command(label="Cadastrar Serviço", command=self.cadastrar_servico)
        menu_bar.add_cascade(label="Cadastro de Serviços", menu=menu_servico)

        menu_agendamento = tk.Menu(menu_bar, tearoff=0)
        menu_agendamento.add_command(label="Novo Agendamento", command=self.cadastrar_agendamento)
        menu_bar.add_cascade(label="Agendamento", menu=menu_agendamento)

        self.root.config(menu=menu_bar)

    def create_main_screen(self):
        logo = tk.Label(self.root, text="LOGO", font=("Arial", 24), bg="gray")
        logo.pack(pady=20)

        welcome_label = tk.Label(self.root, text="Bem-vindo ao sistema", font=("Arial", 16))
        welcome_label.pack(pady=20)

        self.create_agendamentos_table()

    def create_agendamentos_table(self):
        if hasattr(self, 'frame_agendamentos'):
            self.frame_agendamentos.destroy()

        self.frame_agendamentos = tk.Frame(self.root)
        self.frame_agendamentos.pack(fill=tk.BOTH, expand=True, pady=20)

        columns = ("ID", "Cliente", "Data", "Hora", "Serviço", "Status", "Ações")
        self.tree = ttk.Treeview(self.frame_agendamentos, columns=columns, show='headings')

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, minwidth=0, width=100)

        self.update_agendamentos_table()

        self.tree.pack(fill=tk.BOTH, expand=True)

    def update_agendamentos_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        agendamentos = self.controller.listar_agendamentos()

        for agendamento in agendamentos:
            self.tree.insert("", "end", values=agendamento + (self.create_action_buttons(self.tree, agendamento[0]),))

    def create_action_buttons(self, tree, agendamento_id):
        frame = tk.Frame(tree)
        edit_button = tk.Button(frame, text="Editar", command=lambda: self.editar_agendamento(agendamento_id))
        edit_button.pack()
        return frame

    def cadastrar_cliente(self):
        def salvar_cliente():
            nome = entry_nome.get()
            telefone = entry_telefone.get()
            email = entry_email.get()

            if nome and telefone and email:
                self.controller.adicionar_cliente(nome, telefone, email)
                messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
                janela_cliente.destroy()
            else:
                messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")

        janela_cliente = tk.Toplevel(self.root)
        janela_cliente.title("Cadastrar Cliente")
        janela_cliente.geometry("400x300")

        label_nome = tk.Label(janela_cliente, text="Nome:")
        label_nome.pack(pady=10)
        entry_nome = tk.Entry(janela_cliente)
        entry_nome.pack(pady=10)

        label_telefone = tk.Label(janela_cliente, text="Telefone:")
        label_telefone.pack(pady=10)
        entry_telefone = tk.Entry(janela_cliente)
        entry_telefone.pack(pady=10)

        label_email = tk.Label(janela_cliente, text="Email:")
        label_email.pack(pady=10)
        entry_email = tk.Entry(janela_cliente)
        entry_email.pack(pady=10)

        btn_salvar = tk.Button(janela_cliente, text="Salvar", command=salvar_cliente)
        btn_salvar.pack(pady=20, side=tk.LEFT)

    def cadastrar_servico(self):
        def salvar_servico():
            nome = entry_nome.get()

            if nome:
                self.controller.adicionar_servico(nome)
                messagebox.showinfo("Sucesso", "Serviço cadastrado com sucesso!")
                janela_servico.destroy()
            else:
                messagebox.showerror("Erro", "O nome do serviço deve ser preenchido.")

        janela_servico = tk.Toplevel(self.root)
        janela_servico.title("Cadastrar Serviço")
        janela_servico.geometry("400x200")

        label_nome = tk.Label(janela_servico, text="Nome do Serviço:")
        label_nome.pack(pady=10)
        entry_nome = tk.Entry(janela_servico)
        entry_nome.pack(pady=10)

        btn_salvar = tk.Button(janela_servico, text="Salvar", command=salvar_servico)
        btn_salvar.pack(pady=20, side=tk.LEFT)

    def cadastrar_agendamento(self):
        def salvar_agendamento():
            cliente_id = combo_cliente.get().split(" - ")[0]
            servico_id = combo_servico.get().split(" - ")[0]
            data = entry_data.get_date().strftime("%Y-%m-%d")
            hora = entry_hora.get()

            if cliente_id and servico_id and data and hora:
                try:
                    # Chama o método para adicionar agendamento
                    self.controller.adicionar_agendamento(cliente_id, data, hora, servico_id)
                    messagebox.showinfo("Sucesso", "Agendamento cadastrado com sucesso!")
                    janela_agendamento.destroy()
                    self.update_agendamentos_table()  # Atualiza a tabela de agendamentos
                except Exception as e:
                    messagebox.showerror("Erro", str(e))
            else:
                messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")

        janela_agendamento = tk.Toplevel(self.root)
        janela_agendamento.title("Novo Agendamento")
        janela_agendamento.geometry("400x400")

        # Obtém a lista de clientes e serviços do banco de dados
        clientes = self.controller.db.fetch_all("SELECT id, nome FROM clientes")
        servicos = self.controller.db.fetch_all("SELECT id, nome FROM servicos")

        # Popula o combobox de clientes
        label_cliente = tk.Label(janela_agendamento, text="Cliente:")
        label_cliente.pack(pady=10)
        combo_cliente = ttk.Combobox(janela_agendamento, values=[f"{c[0]} - {c[1]}" for c in clientes])
        combo_cliente.pack(pady=10)

        # Popula o combobox de serviços
        label_servico = tk.Label(janela_agendamento, text="Serviço:")
        label_servico.pack(pady=10)
        combo_servico = ttk.Combobox(janela_agendamento, values=[f"{s[0]} - {s[1]}" for s in servicos])
        combo_servico.pack(pady=10)

        # Adiciona o campo de data
        label_data = tk.Label(janela_agendamento, text="Data:")
        label_data.pack(pady=10)
        entry_data = DateEntry(janela_agendamento, date_pattern='dd/mm/yyyy')
        entry_data.pack(pady=10)

        # Adiciona o campo de hora
        label_hora = tk.Label(janela_agendamento, text="Hora (HH:MM):")
        label_hora.pack(pady=10)
        entry_hora = tk.Entry(janela_agendamento)
        entry_hora.pack(pady=10)

        # Adiciona o botão de salvar
        btn_salvar = tk.Button(janela_agendamento, text="Salvar", command=salvar_agendamento)
        btn_salvar.pack(pady=20, side=tk.LEFT)
