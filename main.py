import tkinter as tk
from tkinter import ttk, messagebox
from database import (
    registrar_transacao,
    validar_login,
    cadastrar_usuario,
    criar_banco
)
from datetime import datetime

# Funções de registro
def registrar_entrada(descricao, valor):
    try:
        valor = float(valor)
        if descricao and valor > 0:
            registrar_transacao('entrada', descricao, valor)
            messagebox.showinfo("Sucesso", "Entrada registrada com sucesso!")
            return True
        else:
            messagebox.showwarning("Aviso", "Preencha todos os campos corretamente.")
            return False
    except ValueError:
        messagebox.showwarning("Aviso", "Insira um valor válido.")
        return False

def registrar_saida(descricao, valor):
    try:
        valor = float(valor)
        if descricao and valor > 0:
            registrar_transacao('saida', descricao, valor)
            messagebox.showinfo("Sucesso", "Saída registrada com sucesso!")
            return True
        else:
            messagebox.showwarning("Aviso", "Preencha todos os campos corretamente.")
            return False
    except ValueError:
        messagebox.showwarning("Aviso", "Insira um valor válido.")
        return False

# Tela de Login
class LoginScreen:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master)
        self.frame.pack(fill=tk.BOTH, expand=True)

        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#4CAF50", font=("Arial", 12))
        style.configure("TLabel", background="#f0f0f0", font=("Arial", 14))

        ttk.Label(self.frame, text="Tela de Login", font=("Arial", 16)).pack(pady=20)

        ttk.Label(self.frame, text="Nome de Usuário:").pack(pady=5)
        self.usuario_entry = ttk.Entry(self.frame, width=50)
        self.usuario_entry.pack(pady=5)

        ttk.Label(self.frame, text="Senha:").pack(pady=5)
        self.senha_entry = ttk.Entry(self.frame, width=50, show="*")
        self.senha_entry.pack(pady=5)

        ttk.Button(self.frame, text="Login", command=self.verificar_login).pack(pady=10)
        ttk.Button(self.frame, text="Cadastrar Novo Usuário", command=self.ir_para_cadastro).pack(pady=5)

    def verificar_login(self):
        usuario = self.usuario_entry.get()
        senha = self.senha_entry.get()

        if validar_login(usuario, senha):
            messagebox.showinfo("Sucesso", "Login bem-sucedido!")
            self.frame.pack_forget()
            HomeScreen(self.master)
        else:
            messagebox.showwarning("Erro", "Usuário ou senha inválidos!")

    def ir_para_cadastro(self):
        self.frame.pack_forget()
        CadastroUsuarioScreen(self.master)

# Tela de Cadastro
class CadastroUsuarioScreen:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master)
        self.frame.pack(fill=tk.BOTH, expand=True)

        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#4CAF50", font=("Arial", 12))
        style.configure("TLabel", background="#f0f0f0", font=("Arial", 14))

        ttk.Label(self.frame, text="Cadastro de Novo Usuário", font=("Arial", 16)).pack(pady=20)

        ttk.Label(self.frame, text="Novo Usuário:").pack(pady=5)
        self.novo_usuario_entry = ttk.Entry(self.frame, width=50)
        self.novo_usuario_entry.pack(pady=5)

        ttk.Label(self.frame, text="Nova Senha:").pack(pady=5)
        self.nova_senha_entry = ttk.Entry(self.frame, width=50, show="*")
        self.nova_senha_entry.pack(pady=5)

        ttk.Button(self.frame, text="Cadastrar", command=self.cadastrar).pack(pady=10)
        ttk.Button(self.frame, text="Voltar para Login", command=self.voltar_login).pack(pady=5)

    def cadastrar(self):
        usuario = self.novo_usuario_entry.get()
        senha = self.nova_senha_entry.get()

        if usuario and senha:
            if cadastrar_usuario(usuario, senha):
                messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
                self.frame.pack_forget()
                LoginScreen(self.master)
            else:
                messagebox.showwarning("Erro", "Usuário já existe.")
        else:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")

    def voltar_login(self):
        self.frame.pack_forget()
        LoginScreen(self.master)

# Tela Principal (Home)
class HomeScreen:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master)
        self.frame.pack(fill=tk.BOTH, expand=True)

        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#4CAF50", font=("Arial", 12))
        style.configure("TLabel", background="#f0f0f0", font=("Arial", 14))

        ttk.Label(self.frame, text="Bem-vindo ao Controle Financeiro", font=("Arial", 16)).pack(pady=20)

        ttk.Button(self.frame, text="Gestão de Entradas", command=self.ir_para_entradas).pack(pady=5)
        ttk.Button(self.frame, text="Gestão de Saídas", command=self.ir_para_saidas).pack(pady=5)
        ttk.Button(self.frame, text="Resumo Financeiro", command=self.ir_para_resumo).pack(pady=5)

    def ir_para_entradas(self):
        self.frame.pack_forget()
        EntradasScreen(self.master)

    def ir_para_saidas(self):
        self.frame.pack_forget()
        SaidasScreen(self.master)

    def ir_para_resumo(self):
        self.frame.pack_forget()
        ResumoScreen(self.master)

# Tela de Gestão de Entradas
class EntradasScreen:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master)
        self.frame.pack(fill=tk.BOTH, expand=True)

        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#4CAF50", font=("Arial", 12))
        style.configure("TLabel", background="#f0f0f0", font=("Arial", 14))

        ttk.Label(self.frame, text="Gestão de Entradas", font=("Arial", 16)).pack(pady=20)

        ttk.Label(self.frame, text="Descrição da Entrada:").pack(pady=5)
        self.descricao_entry = ttk.Entry(self.frame, width=50)
        self.descricao_entry.pack(pady=5)

        ttk.Label(self.frame, text="Valor da Entrada:").pack(pady=5)
        self.valor_entry = ttk.Entry(self.frame, width=50)
        self.valor_entry.pack(pady=5)

        ttk.Button(self.frame, text="Registrar Entrada", command=self.registrar).pack(pady=10)
        ttk.Button(self.frame, text="Voltar", command=self.voltar).pack(pady=5)

    def registrar(self):
        descricao = self.descricao_entry.get()
        valor = self.valor_entry.get()
        if registrar_entrada(descricao, valor):
            self.descricao_entry.delete(0, tk.END)
            self.valor_entry.delete(0, tk.END)

    def voltar(self):
        self.frame.pack_forget()
        HomeScreen(self.master)

# Tela de Gestão de Saídas
class SaidasScreen:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master)
        self.frame.pack(fill=tk.BOTH, expand=True)

        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#4CAF50", font=("Arial", 12))
        style.configure("TLabel", background="#f0f0f0", font=("Arial", 14))

        ttk.Label(self.frame, text="Gestão de Saídas", font=("Arial", 16)).pack(pady=20)

        ttk.Label(self.frame, text="Descrição da Saída:").pack(pady=5)
        self.descricao_entry = ttk.Entry(self.frame, width=50)
        self.descricao_entry.pack(pady=5)

        ttk.Label(self.frame, text="Valor da Saída:").pack(pady=5)
        self.valor_entry = ttk.Entry(self.frame, width=50)
        self.valor_entry.pack(pady=5)

        ttk.Button(self.frame, text="Registrar Saída", command=self.registrar).pack(pady=10)
        ttk.Button(self.frame, text="Voltar", command=self.voltar).pack(pady=5)

    def registrar(self):
        descricao = self.descricao_entry.get()
        valor = self.valor_entry.get()
        if registrar_saida(descricao, valor):
            self.descricao_entry.delete(0, tk.END)
            self.valor_entry.delete(0, tk.END)

    def voltar(self):
        self.frame.pack_forget()
        HomeScreen(self.master)

# Tela de Resumo Financeiro (inicial, esqueleto)
class ResumoScreen:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master)
        self.frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.frame, text="Resumo Financeiro", font=("Arial", 16)).pack(pady=20)

        ttk.Label(self.frame, text="(Em breve exibiremos o resumo aqui)").pack(pady=20)

        ttk.Button(self.frame, text="Voltar", command=self.voltar).pack(pady=5)

    def voltar(self):
        self.frame.pack_forget()
        HomeScreen(self.master)

# Inicializar o app
def run_app():
    criar_banco()
    root = tk.Tk()
    root.title("Controle Financeiro")
    root.geometry("800x600")
    LoginScreen(root)
    root.mainloop()

if __name__ == "__main__":
    run_app()
