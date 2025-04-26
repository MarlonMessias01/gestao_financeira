import sqlite3

# Função para conectar e criar tabelas se não existirem
def criar_banco():
    conn = sqlite3.connect('financeiro.db')
    cursor = conn.cursor()

    # Tabela de transações (já existente)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT,
            descricao TEXT,
            valor REAL,
            data TEXT
        )
    ''')

    # Tabela de usuários (nova)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE,
            senha TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Função para registrar uma transação
def registrar_transacao(tipo, descricao, valor):
    conn = sqlite3.connect('financeiro.db')
    cursor = conn.cursor()
    data_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO transacoes (tipo, descricao, valor, data) 
        VALUES (?, ?, ?, ?)
    ''', (tipo, descricao, valor, data_atual))
    conn.commit()
    conn.close()

# Função para cadastrar usuário
def cadastrar_usuario(usuario, senha):
    try:
        conn = sqlite3.connect('financeiro.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO usuarios (usuario, senha) VALUES (?, ?)', (usuario, senha))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False  # Já existe esse usuário

# Função para validar login
def validar_login(usuario, senha):
    conn = sqlite3.connect('financeiro.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE usuario=? AND senha=?', (usuario, senha))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None
