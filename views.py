# views.py

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
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
        if hasattr(self, 'frame_agendamentos'):
            self.frame_agendamentos.destroy()

        self.frame_agendamentos = tk.Frame(self.root)
        self.frame_agendamentos.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        columns = ("ID", "Cliente", "Data", "Hora", "Serviço", "Status")
        tree = ttk.Treeview(self.frame_agendamentos, columns=columns, show='headings')

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, minwidth=0, width=100)

        agendamentos = self.controller.listar_agendamentos()

        for agendamento in agendamentos:
            tree.insert("", "end", values=agendamento)

        tree.bind("<Double-1>", self.on_item_double_click)
        tree.pack(fill=tk.BOTH, expand=True)

    def on_item_double_click(self, event):
        item = self.frame_agendamentos.winfo_children()[0]
        selected_item = item.selection()
        if selected_item:
            agendamento_id = item.item(selected_item[0])['values'][0]
            if messagebox.askyesno("Confirmar", "Deseja alterar as informações deste agendamento?"):
                self.editar_agendamento(agendamento_id)

    def editar_agendamento(self, agendamento_id):
        try:
            agendamento = self.controller.obter_agendamento(agendamento_id)
        except Exception as e:
            messagebox.showerror("Erro", str(e))
            return

        def salvar_edicao():
            cliente_id = combo_cliente.get().split(" - ")[0]
            servico_id = combo_servico.get().split(" - ")[0]
            data = entry_data.get_date().strftime("%Y-%m-%d")  # Data no formato YYYY-MM-DD
            hora = entry_hora.get()
            status = combo_status.get()

            if cliente_id and servico_id and data and hora and status:
                try:
                    self.controller.atualizar_agendamento(agendamento_id, cliente_id, data, hora, servico_id, status)
                    messagebox.showinfo("Sucesso", "Agendamento atualizado com sucesso!")
                    janela_edicao.destroy()
                    self.create_main_screen()  # Atualiza a tabela de agendamentos
                except Exception as e:
                    messagebox.showerror("Erro", str(e))
            else:
                messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")

        janela_edicao = tk.Toplevel(self.root)
        janela_edicao.title("Editar Agendamento")
        janela_edicao.geometry("500x500")

        clientes = self.controller.db.fetch_all("SELECT id, nome FROM clientes")
        servicos = self.controller.db.fetch_all("SELECT id, nome FROM servicos")

        tk.Label(janela_edicao, text="Cliente:", anchor="w").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        combo_cliente = ttk.Combobox(janela_edicao, values=[f"{c[0]} - {c[1]}" for c in clientes], width=50)
        combo_cliente.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        combo_cliente.set(f"{agendamento[0]} - {self.get_cliente_nome(agendamento[0])}")

        tk.Label(janela_edicao, text="Serviço:", anchor="w").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        combo_servico = ttk.Combobox(janela_edicao, values=[f"{s[0]} - {s[1]}" for s in servicos], width=50)
        combo_servico.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        combo_servico.set(f"{agendamento[3]} - {self.get_servico_nome(agendamento[3])}")

        tk.Label(janela_edicao, text="Data:", anchor="w").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        entry_data = DateEntry(janela_edicao, date_pattern='dd/mm/yyyy', width=50)
        entry_data.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        try:
            # Converta a data para o formato DD/MM/YYYY
            data_agendamento = datetime.strptime(agendamento[1], "%Y-%m-%d")
            entry_data.set_date(data_agendamento.strftime("%d/%m/%Y"))
        except ValueError:
            entry_data.set_date(datetime.today().strftime("%d/%m/%Y"))  # Define uma data padrão se o valor estiver incorreto

        tk.Label(janela_edicao, text="Hora (HH:MM):", anchor="w").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        entry_hora = tk.Entry(janela_edicao, width=50)
        entry_hora.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        entry_hora.insert(0, agendamento[2])

        tk.Label(janela_edicao, text="Status:", anchor="w").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        combo_status = ttk.Combobox(janela_edicao, values=["Agendado", "Atendido", "Cancelado"], width=50)
        combo_status.grid(row=4, column=1, padx=10, pady=5, sticky="w")
        combo_status.set(agendamento[4])

        btn_salvar = tk.Button(janela_edicao, text="Salvar", command=salvar_edicao)
        btn_salvar.grid(row=5, column=1, padx=10, pady=20, sticky="e")

    def get_cliente_nome(self, cliente_id):
        cliente = self.controller.db.fetch_one("SELECT nome FROM clientes WHERE id = ?", (cliente_id,))
        return cliente[0] if cliente else ""

    def get_servico_nome(self, servico_id):
        servico = self.controller.db.fetch_one("SELECT nome FROM servicos WHERE id = ?", (servico_id,))
        return servico[0] if servico else ""

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

        tk.Label(janela_cliente, text="Nome:").pack(pady=10)
        entry_nome = tk.Entry(janela_cliente, width=50)
        entry_nome.pack(pady=10)

        tk.Label(janela_cliente, text="Telefone:").pack(pady=10)
        entry_telefone = tk.Entry(janela_cliente, width=50)
        entry_telefone.pack(pady=10)

        tk.Label(janela_cliente, text="Email:").pack(pady=10)
        entry_email = tk.Entry(janela_cliente, width=50)
        entry_email.pack(pady=10)

        btn_salvar = tk.Button(janela_cliente, text="Salvar", command=salvar_cliente)
        btn_salvar.pack(pady=20)

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
        janela_servico.geometry("400x300")

        tk.Label(janela_servico, text="Nome:").pack(pady=10)
        entry_nome = tk.Entry(janela_servico, width=50)
        entry_nome.pack(pady=10)

        btn_salvar = tk.Button(janela_servico, text="Salvar", command=salvar_servico)
        btn_salvar.pack(pady=20)

    def cadastrar_agendamento(self):
        def salvar_agendamento():
            cliente_id = combo_cliente.get().split(" - ")[0]
            servico_id = combo_servico.get().split(" - ")[0]
            data = entry_data.get_date().strftime("%Y-%m-%d")  # Data no formato YYYY-MM-DD
            hora = entry_hora.get()
            status = combo_status.get()

            if cliente_id and servico_id and data and hora and status:
                try:
                    self.controller.adicionar_agendamento(cliente_id, data, hora, servico_id)
                    messagebox.showinfo("Sucesso", "Agendamento cadastrado com sucesso!")
                    janela_agendamento.destroy()
                    self.create_main_screen()  # Atualiza a tabela de agendamentos
                except Exception as e:
                    messagebox.showerror("Erro", str(e))
            else:
                messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")

        janela_agendamento = tk.Toplevel(self.root)
        janela_agendamento.title("Cadastrar Agendamento")
        janela_agendamento.geometry("500x500")

        clientes = self.controller.db.fetch_all("SELECT id, nome FROM clientes")
        servicos = self.controller.db.fetch_all("SELECT id, nome FROM servicos")

        tk.Label(janela_agendamento, text="Cliente:", anchor="w").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        combo_cliente = ttk.Combobox(janela_agendamento, values=[f"{c[0]} - {c[1]}" for c in clientes], width=50)
        combo_cliente.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        tk.Label(janela_agendamento, text="Serviço:", anchor="w").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        combo_servico = ttk.Combobox(janela_agendamento, values=[f"{s[0]} - {s[1]}" for s in servicos], width=50)
        combo_servico.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        tk.Label(janela_agendamento, text="Data:", anchor="w").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        entry_data = DateEntry(janela_agendamento, date_pattern='dd/mm/yyyy', width=50)
        entry_data.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        tk.Label(janela_agendamento, text="Hora (HH:MM):", anchor="w").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        entry_hora = tk.Entry(janela_agendamento, width=50)
        entry_hora.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        tk.Label(janela_agendamento, text="Status:", anchor="w").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        combo_status = ttk.Combobox(janela_agendamento, values=["Agendado", "Atendido", "Cancelado"], width=50)
        combo_status.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        btn_salvar = tk.Button(janela_agendamento, text="Salvar", command=salvar_agendamento)
        btn_salvar.grid(row=5, column=1, padx=10, pady=20, sticky="e")

