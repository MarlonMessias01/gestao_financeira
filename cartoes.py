# cartoes.py
import tkinter as tk
from tkinter import ttk, messagebox
import database
from datetime import datetime, timedelta

class CartoesApp:
    def __init__(self, user_id):
        self.user_id = user_id

        self.win = tk.Toplevel()
        self.win.title("Gestão de Cartões")
        self.win.geometry("400x500")

        ttk.Label(self.win, text="Nome do Cartão:").pack(pady=5)
        self.entry_nome = ttk.Entry(self.win)
        self.entry_nome.pack()

        ttk.Label(self.win, text="Limite:").pack(pady=5)
        self.entry_limite = ttk.Entry(self.win)
        self.entry_limite.pack()

        ttk.Button(self.win, text="Adicionar Cartão", command=self.adicionar_cartao).pack(pady=10)

        ttk.Label(self.win, text="Cartões cadastrados:").pack(pady=5)
        self.lista_cartoes = tk.Listbox(self.win)
        self.lista_cartoes.pack(pady=10, fill=tk.BOTH, expand=True)

        ttk.Button(self.win, text="Excluir Cartão", command=self.excluir_cartao).pack(pady=5)
        ttk.Button(self.win, text="Registrar Compra", command=self.registrar_compra).pack(pady=5)

        self.listar_cartoes()

    def adicionar_cartao(self):
        nome = self.entry_nome.get()
        limite = float(self.entry_limite.get())

        conn = database.conectar()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO cartoes (user_id, nome_cartao, limite)
            VALUES (?, ?, ?)
        ''', (self.user_id, nome, limite))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Cartão adicionado!")
        self.listar_cartoes()

    def listar_cartoes(self):
        self.lista_cartoes.delete(0, tk.END)

        conn = database.conectar()
        cursor = conn.cursor()
        cursor.execute('SELECT id, nome_cartao FROM cartoes WHERE user_id=?', (self.user_id,))
        cartoes = cursor.fetchall()
        conn.close()

        for cartao in cartoes:
            self.lista_cartoes.insert(tk.END, f"{cartao[0]} - {cartao[1]}")

    def excluir_cartao(self):
        selecionado = self.lista_cartoes.get(tk.ACTIVE)
        if not selecionado:
            return
        id_cartao = int(selecionado.split(' - ')[0])

        conn = database.conectar()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM cartoes WHERE id=?', (id_cartao,))
        conn.commit()
        conn.close()

        self.listar_cartoes()

    def registrar_compra(self):
        selecionado = self.lista_cartoes.get(tk.ACTIVE)
        if not selecionado:
            return
        id_cartao = int(selecionado.split(' - ')[0])

        self.nova_win = tk.Toplevel()
        self.nova_win.title("Nova Compra")
        self.nova_win.geometry("300x300")

        ttk.Label(self.nova_win, text="Descrição:").pack(pady=5)
        self.entry_desc = ttk.Entry(self.nova_win)
        self.entry_desc.pack()

        ttk.Label(self.nova_win, text="Valor total:").pack(pady=5)
        self.entry_valor = ttk.Entry(self.nova_win)
        self.entry_valor.pack()

        ttk.Label(self.nova_win, text="Parcelas:").pack(pady=5)
        self.entry_parcelas = ttk.Entry(self.nova_win)
        self.entry_parcelas.pack()
        self.entry_parcelas.insert(0, "1")

        ttk.Button(self.nova_win, text="Salvar Compra", command=lambda: self.salvar_compra(id_cartao)).pack(pady=10)

    def salvar_compra(self, id_cartao):
        descricao = self.entry_desc.get()
        valor_total = float(self.entry_valor.get())
        parcelas = int(self.entry_parcelas.get())
        data_inicial = datetime.now()

        valor_parcela = valor_total / parcelas

        conn = database.conectar()
        cursor = conn.cursor()

        for parcela in range(1, parcelas + 1):
            data_parcela = (data_inicial + timedelta(days=30 * (parcela-1))).strftime("%Y-%m-%d")
            cursor.execute('''
                INSERT INTO transacoes (user_id, descricao, valor, data, tipo, categoria, cartao_id, parcelas, parcela_atual)
                VALUES (?, ?, ?, ?, 'despesa', 'Cartão de Crédito', ?, ?, ?)
            ''', (self.user_id, f"{descricao} ({parcela}/{parcelas})", -valor_parcela, data_parcela, id_cartao, parcelas, parcela))

        conn.commit()
        conn.close()

        self.nova_win.destroy()
        messagebox.showinfo("Sucesso", "Compra registrada!")
