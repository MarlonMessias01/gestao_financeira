# home.py
import tkinter as tk
from tkinter import ttk
import database

class HomeApp:
    def __init__(self, user_id):
        self.user_id = user_id
        self.master = tk.Tk()
        self.master.title("Controle Financeiro - Home")
        self.master.geometry('500x600')

        self.saldo_label = ttk.Label(self.master, text="Saldo: R$ 0.00", font=("Arial", 16))
        self.saldo_label.pack(pady=20)

        ttk.Button(self.master, text="Adicionar Entrada/Saída", command=self.abrir_entradas_saidas).pack(pady=10)
        ttk.Button(self.master, text="Gerenciar Cartões", command=self.abrir_cartoes).pack(pady=10)
        ttk.Button(self.master, text="Resumo Financeiro", command=self.abrir_resumo).pack(pady=10)

        self.listar_transacoes()

        self.master.mainloop()

    def listar_transacoes(self):
        conn = database.conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT descricao, valor, data FROM transacoes WHERE user_id=?", (self.user_id,))
        transacoes = cursor.fetchall()

        lista = tk.Listbox(self.master)
        lista.pack(pady=20, fill=tk.BOTH, expand=True)

        saldo = 0
        for desc, valor, data in transacoes:
            lista.insert(tk.END, f"{data} | {desc}: R$ {valor:.2f}")
            saldo += valor

        self.saldo_label.config(text=f"Saldo: R$ {saldo:.2f}")

        conn.close()

    def abrir_entradas_saidas(self):
        import entradas_saidas
        entradas_saidas.EntradasSaidasApp(self.user_id)

    def abrir_cartoes(self):
        import cartoes
        cartoes.CartoesApp(self.user_id)

    def abrir_resumo(self):
        import resumo
        resumo.ResumoApp(self.user_id)
