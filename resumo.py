# resumo.py
import tkinter as tk
from tkinter import ttk
import database
from datetime import datetime, timedelta

class ResumoApp:
    def __init__(self, user_id):
        self.user_id = user_id

        self.win = tk.Toplevel()
        self.win.title("Resumo Financeiro")
        self.win.geometry("400x400")

        ttk.Label(self.win, text="Resumo:").pack(pady=10)

        ttk.Button(self.win, text="Resumo Semanal", command=self.resumo_semanal).pack(pady=5)
        ttk.Button(self.win, text="Resumo Mensal", command=self.resumo_mensal).pack(pady=5)
        ttk.Button(self.win, text="Resumo Anual", command=self.resumo_anual).pack(pady=5)

        self.texto = tk.Text(self.win, height=15)
        self.texto.pack(pady=10, fill=tk.BOTH, expand=True)

    def resumo_semanal(self):
        hoje = datetime.now()
        inicio_semana = hoje - timedelta(days=7)
        self.mostrar_resumo(inicio_semana, hoje)

    def resumo_mensal(self):
        hoje = datetime.now()
        inicio_mes = hoje.replace(day=1)
        self.mostrar_resumo(inicio_mes, hoje)

    def resumo_anual(self):
        hoje = datetime.now()
        inicio_ano = hoje.replace(month=1, day=1)
        self.mostrar_resumo(inicio_ano, hoje)

    def mostrar_resumo(self, data_inicio, data_fim):
        conn = database.conectar()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT tipo, SUM(valor) FROM transacoes
            WHERE user_id = ? AND data BETWEEN ? AND ?
            GROUP BY tipo
        ''', (self.user_id, data_inicio.strftime('%Y-%m-%d'), data_fim.strftime('%Y-%m-%d')))
        resumo = cursor.fetchall()
        conn.close()

        entradas = 0
        saidas = 0

        for tipo, valor in resumo:
            if tipo == "receita":
                entradas += valor
            else:
                saidas += abs(valor)

        saldo = entradas - saidas

        self.texto.delete(1.0, tk.END)
        self.texto.insert(tk.END, f"Entradas: R$ {entradas:.2f}\n")
        self.texto.insert(tk.END, f"Saídas: R$ {saidas:.2f}\n")
        self.texto.insert(tk.END, f"Saldo: R$ {saldo:.2f}")
