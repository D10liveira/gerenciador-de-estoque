import tkinter as tk
from tkinter import messagebox
from cadastroProdutos import GerenciadorEstoque


class AplicativoEstoque:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Estoque")
        self.gerenciador = GerenciadorEstoque()

        # Cria interface
        self.create_widgets()

    def create_widgets(self):
        # Adicionar Produto
        self.frame_adicionar = tk.Frame(self.root)
        self.frame_adicionar.pack(padx=10, pady=10)

        tk.Label(self.frame_adicionar, text="Nome:").grid(row=0, column=0)
        self.entry_nome = tk.Entry(self.frame_adicionar)
        self.entry_nome.grid(row=0, column=1)

        tk.Label(self.frame_adicionar, text="Descrição:").grid(row=1, column=0)
        self.entry_descricao = tk.Entry(self.frame_adicionar)
        self.entry_descricao.grid(row=1, column=1)

        tk.Label(self.frame_adicionar, text="Quantidade:").grid(
            row=2, column=0)
        self.entry_quantidade = tk.Entry(self.frame_adicionar)
        self.entry_quantidade.grid(row=2, column=1)

        tk.Label(self.frame_adicionar, text="Preço:").grid(row=3, column=0)
        self.entry_preco = tk.Entry(self.frame_adicionar)
        self.entry_preco.grid(row=3, column=1)

        tk.Label(self.frame_adicionar, text="Estoque Mínimo:").grid(
            row=4, column=0)
        self.entry_estoque_minimo = tk.Entry(self.frame_adicionar)
        self.entry_estoque_minimo.grid(row=4, column=1)

        tk.Label(self.frame_adicionar, text="Fornecedor ID:").grid(
            row=5, column=0)
        self.entry_fornecedor_id = tk.Entry(self.frame_adicionar)
        self.entry_fornecedor_id.grid(row=5, column=1)

        self.btn_adicionar = tk.Button(
            self.frame_adicionar, text="Adicionar Produto", command=self.adicionar_produto)
        self.btn_adicionar.grid(row=6, columnspan=2, pady=10)

        # Excluir Produto
        self.frame_excluir = tk.Frame(self.root)
        self.frame_excluir.pack(padx=10, pady=10)

        tk.Label(self.frame_excluir, text="Produto ID:").grid(row=0, column=0)
        self.entry_produto_id = tk.Entry(self.frame_excluir)
        self.entry_produto_id.grid(row=0, column=1)

        self.btn_excluir = tk.Button(
            self.frame_excluir, text="Excluir Produto", command=self.excluir_produto)
        self.btn_excluir.grid(row=1, columnspan=2, pady=10)

        # Verificar Estoque Baixo
        self.frame_estoque_baixo = tk.Frame(self.root)
        self.frame_estoque_baixo.pack(padx=10, pady=10)

        self.btn_verificar_estoque_baixo = tk.Button(
            self.frame_estoque_baixo, text="Verificar Estoque Baixo", command=self.verificar_estoque_baixo)
        self.btn_verificar_estoque_baixo.grid(row=0, column=0, pady=10)

        # Listar Produtos
        self.frame_listar = tk.Frame(self.root)
        self.frame_listar.pack(padx=10, pady=10)

        self.btn_listar = tk.Button(
            self.frame_listar, text="Listar Produtos", command=self.listar_produtos)
        self.btn_listar.grid(row=0, column=0)

        self.text_listar = tk.Text(self.frame_listar, height=10, width=50)
        self.text_listar.grid(row=1, column=0)

    def adicionar_produto(self):
        try:
            nome = self.entry_nome.get()
            descricao = self.entry_descricao.get()
            quantidade = int(self.entry_quantidade.get())
            preco = float(self.entry_preco.get())
            estoque_minimo = int(self.entry_estoque_minimo.get())
            fornecedor_id = int(self.entry_fornecedor_id.get())

            self.gerenciador.adicionar_produto(
                nome, descricao, quantidade, preco, estoque_minimo, fornecedor_id)
            messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")

            # Limpar campos após adicionar o produto
            self.entry_nome.delete(0, tk.END)
            self.entry_descricao.delete(0, tk.END)
            self.entry_quantidade.delete(0, tk.END)
            self.entry_preco.delete(0, tk.END)
            self.entry_estoque_minimo.delete(0, tk.END)
            self.entry_fornecedor_id.delete(0, tk.END)
        except ValueError as ve:
            self.show_error("Valor inválido", ve)
        except Exception as e:
            self.show_error("Erro ao adicionar produto", e)

    def excluir_produto(self):
        try:
            produto_id = int(self.entry_produto_id.get())
            self.gerenciador.excluir_produto(produto_id)
            messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")

            # Limpar campos após excluir o produto
            self.entry_produto_id.delete(0, tk.END)
        except ValueError as ve:
            self.show_error("Valor inválido", ve)
        except Exception as e:
            self.show_error("Erro ao excluir produto", e)

    def verificar_estoque_baixo(self):
        try:
            produtos_baixo_estoque = self.gerenciador.verificar_estoque_baixo()
            if not produtos_baixo_estoque:
                messagebox.showinfo(
                    "Estoque Baixo", "Nenhum produto com estoque baixo.")
            else:
                produtos = "\n".join([f"Nome: {produto[0]}, Quantidade: {produto[1]}, Estoque Mínimo: {
                                     produto[2]}" for produto in produtos_baixo_estoque])
                messagebox.showwarning("Produtos com Estoque Baixo", produtos)
        except Exception as e:
            self.show_error("Erro ao verificar estoque baixo", e)

    def listar_produtos(self):
        try:
            produtos = self.gerenciador.listar_produtos()
            self.text_listar.delete(1.0, tk.END)  # Limpar o texto
            for produto in produtos:
                self.text_listar.insert(tk.END, f"{produto}\n")
        except Exception as e:
            self.show_error("Erro ao listar produtos", e)

    def show_error(self, title, message):
        messagebox.showerror(title, message)


# Criar a janela principal
root = tk.Tk()
app = AplicativoEstoque(root)
root.mainloop()
