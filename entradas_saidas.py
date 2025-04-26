# entradas_saidas.py
import tkinter as tk
from tkinter import ttk
import database
from datetime import date

class EntradasSaidasApp:
    def __init__(self, user_id):
        self.user_id = user_id

        self.win = tk.Toplevel()
        self.win.title("Adicionar Entrada/Saída")
        self.win.geometry("400x400")

        ttk.Label(self.win, text="Descrição:").pack(pady=5)
        self.entry_desc = ttk.Entry(self.win)
        self.entry_desc.pack()

        ttk.Label(self.win, text="Valor:").pack(pady=5)
        self.entry_valor = ttk.Entry(self.win)
        self.entry_valor.pack()

        ttk.Label(self.win, text="Tipo:").pack(pady=5)
        self.tipo_var = tk.StringVar()
        self.tipo_var.set("receita")
        ttk.Combobox(self.win, textvariable=self.tipo_var, values=["receita", "despesa"]).pack()

        ttk.Label(self.win, text="Categoria:").pack(pady=5)
        self.entry_categoria = ttk.Entry(self.win)
        self.entry_categoria.pack()

        ttk.Button(self.win, text="Salvar", command=self.salvar).pack(pady=20)

    def salvar(self):
        desc = self.entry_desc.get()
        valor = float(self.entry_valor.get())
        tipo = self.tipo_var.get()
        categoria = self.entry_categoria.get()
        data_transacao = date.today().strftime("%Y-%m-%d")

        if tipo == "despesa":
            valor = -valor

        conn = database.conectar()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO transacoes (user_id, descricao, valor, data, tipo, categoria)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (self.user_id, desc, valor, data_transacao, tipo, categoria))
        conn.commit()
        conn.close()

        self.win.destroy()
