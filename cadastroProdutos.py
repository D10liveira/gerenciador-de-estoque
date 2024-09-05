import sqlite3


class GerenciadorEstoque:
    def __init__(self, db_name='estoque.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.criar_tabelas()

    def criar_tabelas(self):
        """Cria as tabelas no banco de dados, se não existirem."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Produtos (
                produto_id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT,
                quantidade INTEGER NOT NULL,
                preco REAL NOT NULL,
                estoque_minimo INTEGER NOT NULL,
                fornecedor_id INTEGER,
                FOREIGN KEY (fornecedor_id) REFERENCES Fornecedores(fornecedor_id)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Movimentacoes (
                movimentacao_id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto_id INTEGER NOT NULL,
                tipo TEXT NOT NULL, -- entrada ou saída
                quantidade INTEGER NOT NULL,
                data_movimentacao TEXT NOT NULL,
                FOREIGN KEY (produto_id) REFERENCES Produtos(produto_id)
            )
        ''')

        self.conn.commit()

    def adicionar_produto(self, nome, descricao, quantidade, preco, estoque_minimo, fornecedor_id):
        """Adiciona um novo produto ao banco de dados."""
        try:
            self.cursor.execute('''
                INSERT INTO Produtos (nome, descricao, quantidade, preco, estoque_minimo, fornecedor_id)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (nome, descricao, quantidade, preco, estoque_minimo, fornecedor_id))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Erro ao adicionar produto: {e}")

    def excluir_produto(self, produto_id):
        """Exclui um produto do banco de dados."""
        try:
            self.cursor.execute('''
                DELETE FROM Produtos
                WHERE produto_id = ?
            ''', (produto_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Erro ao excluir produto: {e}")

    def atualizar_quantidade(self, produto_id, quantidade_nova):
        """Atualiza a quantidade de um produto existente."""
        try:
            self.cursor.execute('''
                UPDATE Produtos
                SET quantidade = ?
                WHERE produto_id = ?
            ''', (quantidade_nova, produto_id))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Erro ao atualizar quantidade: {e}")

    def listar_produtos(self):
        """Consulta e retorna todos os produtos."""
        try:
            self.cursor.execute('SELECT * FROM Produtos')
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erro ao listar produtos: {e}")
            return []

    def verificar_estoque_baixo(self):
        """Consulta e retorna produtos com estoque abaixo do mínimo."""
        try:
            self.cursor.execute('''
                SELECT nome, quantidade, estoque_minimo
                FROM Produtos
                WHERE quantidade < estoque_minimo
            ''')
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erro ao verificar estoque baixo: {e}")
            return []

    def __del__(self):
        """Fecha a conexão com o banco de dados quando o objeto for destruído."""
        self.conn.close()
