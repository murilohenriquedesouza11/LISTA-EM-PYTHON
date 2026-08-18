import tkinter as tk
from tkinter import ttk, messagebox
import os

# ============================================
# lista de compras - aplicativo em tkinter
# ============================================

Arquivo = "lista_compras . txt"

class listaComprasapp:
 def __init__(self, root):
  self.root = root
  self.root . title("🛒 lista de compras")
  self.root . geometry("750x550")
  self.root . confegure(bg=  "#f0f4f8")

  # Dados em memoria
  self.itens = []
  self.item_selecionado = None

  self.criar_widgets()
  self.caregar_do_arquivo()
  self.atualizar_lista()

 def criar_widgeds(self):
    #========titulo========
    lbl_titulo = tk.Label(
        self.root,
        text="🛒 lista de compras",
        font=("arial", 20, "bold")
        bg= "#f0f4f8",
        fg="#la5276"
        )
    lbl_titulo.pack(pady=10)

    #=======frame de entrada ==========
    frame_entrada = tk. Frame(self.root, bg= "#f0f4f8")
    frame_entrada.pack(pady=10, padx=20, fill="x")

    # Descricao
    tk.Label(frame_entrada, text="Descrição", font=("Arial", 11), bg="#f0f4f8", fg="#2c3e50").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    self.txt_descricao = tk.Entry(frame_entrada, font=("Arial", 11), width=30,relief="solid", bd=1)
    self.txt_descricao.grid(row=0, column=1, padx=5, pady=5)

    #quantidade
    tk.Label(frame_entrada, text="Quantidade", font=("Arial", 11), bg="#f0f4f8", fg="#2c3e50").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    self.txt_quantidade = tk.Entry(frame_entrada, font=("Arial", 11), width=30,relief="solid", bd=1)
    self.txt_quantidade.grid(row=0, column=3, padx=5, pady=5)
 
    #preço
    tk.Label(frame_entrada, text="Preço Unit. (R$):", font=("Arial", 11), bg="#f0f4f8", fg="#2c3e50").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    self.txt_preço = tk.Entry(frame_entrada, font=("Arial", 11), width=30,relief="solid", bd=1)
    self.txt_preço.grid(row=0, column=5, padx=5, pady=5)

    # ================ FRAME DE BOTOẼS ================
    frame_botoes = tk.Frame(self.root, bg="#f0f4f8")
    frame_botoes.pack(pady=10)

    #Botão inserir
    self.btn_inserir = tk.Button(
      frame_botoes,
      text="🏥inserir",
      font=("Arial", 11, "bold")
      bg="#f0f4f8", fg("white")
      width=12, cursor="hand2",
      relief="flat",
      command=self.inserir
    )
    self.btn_inserir.pack(side="left", padx=5)
   
    # Botão Editar
    self.btn_editar = tk.Button(
      frame_botoes,
      text="- Editar",
      font=("Arial", 11, "bold"),
      bg="#f39c12", fg="White",
      width=12, cursor="hand2"
      relief="flat",
      command=self.editar
    )
    self.btn_editar.pack(side="left", padx=5)
   
    # Botão Deletar
    self.btn_deletar = tk.Button(
      frame_botoes,
      text="🗑️ Deletar",
      font=("Arial", 11, "bold"),
      bg="#e74c3c", fg="White",
      width=12, cursor="hand2",
      relief="flat",
      command=self.Deletar
    )
    self.btn_deletar.pack(side="left", padx=5)

    # Botão limpar campos
    self.btn_inserir = tk.Button(
      frame_botoes,
      text="limpar",
      font=("Arial", 11, "bold")
      bg="#f0f4f8", fg("white")
      width=12, cursor="hand2",
      relief="flat",
      command=self.inserir
    )
    self.btn_limpar.pack
    
    
    # ========== LISTA DE ITENS (TREEVIEW) =========
    frame_lista = tk.Frame(self.root, bg="#f0f4f8")
    frame_lista.pack(pady=10, padx=20, fill="both", expand=True)
    
    # Scrollbar
    scrollbar = tk.Scrollbar(frame_lista)
    scrollbar.pack(side="right", fill="y")
    
    # Treeview
    colunas = ("descricao", "quantidade", "preco", "subtotal")
    self.tree = ttk.Treeview(
        frame_lista,
        show= "headings",
        yscrollcommand=scrollbar.set,
        height=10
    )
    scrollbar.config(command=self.tree.yview)
    
    # Configurar colunas
    self.tree.heading("descricao", text="Descrição")
    self.tree.heading("quantidade", text="0td")
    self.tree.heading("preco", text="Preço Unit. (R$)")
    self.tree.heading("subtotal", text="Subtotal (R$)")
    
    self.tree.column("descricao", widht=250, anchor="W")
    self.tree.column("quantidade", widht=60, anchor="center")
    self.tree.column("preco", widht=120, anchor="e")
    self.tree.column("subtotal", widht=120, anchor="e")
    
    self.treee.pack(fill)
    
    # Evento da seleçao
    self.tree.bind("<<TreeviewSelect>>", self.on_select)
    
    # ========= TOTAL =========
    frame_total = tk.Frame(self.root, bg="#f0f4f8")
    frame_total.pack(pady=10, padx=20, fill="X")
    
    self.lbl_total = tk.Label(
        frame_total,
        text="TOTAL: R$ 0,00",
        font=("Arial", 16, "bold"),
        bg="#f0f4f8",
        fg="#1a5276",
    )
    self.lbl_total.pack(side="right")
    
    # ======== STATUS BAR =========
    self.lbl_status = tk.Label(
        self.root,
        text="pronto. Selecione um item para editar ou deletar.",
        font=("Arial", 9),
        bg="#d5dbdb"
        fg="#2c3e50",
        anchor="W"
    )

    self.lbl_status.pack(fill="X", side="botton")

    # Estilo Treeview
    style = ttk.Style()
    style.theme_use("clan")
    style.configure("Treeview", font=("Arial", 10), rowheight=25)
    style.configure("Treeview.Heading", font=("Arial", 11, "bold"),background="#3498db", foreground="white")
    style.map("Treeview", background=(("selected", "#aed6f1")))

 def on_select(self, event):
       """Quando um item da lista é selecionado, preenche os campos"""
       selecao = self.tree.selection()
       if selecao:
          item_id = selecao[0]
          valores = self.tree.item(item_id, "values")

          self.txt_descricao.delete(0, tk.END)
          self.txt_descricao.insert(0, valores[1])

          self.txt_quantidade(0, tk.END)
          self.txt_quantidade.insert(0, valores[1])

          self.txt_preco.delete(0, tk.END)
          self.txt_status.config(text=f"Item selecionado: {valores[0]}")

       def limpar_campos(self):
          """Limpa todos os campos de entrada"""
          self.txt_descricao.delete(0, tk.END)
          self.txt_quantidade.delete(0, tk.END)
          self.txt_preco.delete(0, tk.END)
          self.item_selecionado = None
          self.tree.selection_remove(self.tree.selection())
          self.lbl_status.config(text="Campos limpos. Pronto para inserir novo item,")
          self.txt_descricao.focus()

      def validar_entrada(self):
          """Valida os campos de entrada"""
          descricao = self.txt_descricao.get().strip()
          quantidade = self.txt_quantidade.get().strip()
          preco = self.txt_preco.get().strip()

          if not descricao:
            messagebox.sinowrning("Aviso", "Digite a descricao do item!")
            return None   
          
          

          
     


    
   
