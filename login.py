# login.py
import tkinter as tk
from tkinter import ttk, messagebox
import database

class LoginApp:
    def __init__(self, master):
        self.master = master
        self.master.title('Login - Controle Financeiro')
        self.master.geometry('300x400')

        ttk.Label(master, text="Usuário:").pack(pady=10)
        self.entry_user = ttk.Entry(master)
        self.entry_user.pack()

        ttk.Label(master, text="Senha:").pack(pady=10)
        self.entry_pass = ttk.Entry(master, show="*")
        self.entry_pass.pack()

        ttk.Button(master, text="Login", command=self.login).pack(pady=10)
        ttk.Button(master, text="Cadastrar", command=self.cadastrar).pack(pady=5)

    def login(self):
        usuario = self.entry_user.get()
        senha = self.entry_pass.get()

        conn = database.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username=? AND senha=?", (usuario, senha))
        result = cursor.fetchone()
        conn.close()

        if result:
            user_id = result[0]
            self.master.destroy()
            import home
            home.HomeApp(user_id)
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos.")

    def cadastrar(self):
        usuario = self.entry_user.get()
        senha = self.entry_pass.get()

        conn = database.conectar()
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users (username, senha) VALUES (?, ?)", (usuario, senha))
            conn.commit()
            messagebox.showinfo("Sucesso", "Usuário cadastrado!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Usuário já existe.")
        conn.close()
