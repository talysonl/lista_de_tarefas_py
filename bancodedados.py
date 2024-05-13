import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import date

# Função para conectar ao banco de dados
def conectar_bd():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="Co010910BR7!",
            database="StarkTaskManager"
        )
    except mysql.connector.Error as err:
        messagebox.showerror("Erro de Conexão", f"Erro ao conectar ao banco de dados: {err}")
        return None

# Função para desconectar do banco de dados
def desconectar_bd(db):
    if db:
        db.close()

# Função para adicionar uma nova tarefa
def adicionar_tarefa():
    descricao = entry_descricao.get()
    status = combo_status.get()
    if descricao.strip() == '':
        messagebox.showwarning("Erro", "Por favor, insira uma descrição para a tarefa.")
        return

    try:
        db = conectar_bd()
        if db:
            with db.cursor() as cursor:
                sql = "INSERT INTO Tasks (description, start_date, end_date, status) VALUES (%s, %s, %s, %s)"
                values = (descricao, date.today(), None, status)
                cursor.execute(sql, values)
                db.commit()
                messagebox.showinfo("Sucesso", "Tarefa adicionada com sucesso!")
                mostrar_tarefas()
                entry_descricao.delete(0, tk.END)  # Limpar o campo de texto após adicionar
    finally:
        desconectar_bd(db)

# Função para exibir as tarefas na lista
def mostrar_tarefas():
    try:
        db = conectar_bd()
        if db:
            with db.cursor() as cursor:
                cursor.execute("SELECT * FROM Tasks")
                rows = cursor.fetchall()

                listbox_tarefas.delete(0, tk.END)

                for row in rows:
                    listbox_tarefas.insert(tk.END, f"{row[0]} - {row[1]} - {row[4]}")

    finally:
        desconectar_bd(db)

# Função para editar uma tarefa selecionada
def editar_tarefa():
    selecionado = listbox_tarefas.curselection()
    if not selecionado:
        messagebox.showwarning("Erro", "Por favor, selecione uma tarefa para editar.")
        return

    indice = selecionado[0]
    nova_descricao = entry_descricao.get()
    novo_status = combo_status.get()

    try:
        db = conectar_bd()
        if db:
            with db.cursor() as cursor:
                tarefa_id = listbox_tarefas.get(indice).split()[0]
                sql = "UPDATE Tasks SET description = %s, status = %s WHERE id = %s"
                values = (nova_descricao, novo_status, tarefa_id)
                cursor.execute(sql, values)
                db.commit()
                messagebox.showinfo("Sucesso", "Tarefa editada com sucesso!")
                mostrar_tarefas()
    finally:
        desconectar_bd(db)

# Função para remover uma tarefa selecionada
def remover_tarefa():
    selecionado = listbox_tarefas.curselection()
    if not selecionado:
        messagebox.showwarning("Erro", "Por favor, selecione uma tarefa para remover.")
        return

    indice = selecionado[0]

    try:
        db = conectar_bd()
        if db:
            with db.cursor() as cursor:
                tarefa_id = listbox_tarefas.get(indice).split()[0]
                sql = "DELETE FROM Tasks WHERE id = %s"
                cursor.execute(sql, (tarefa_id,))
                db.commit()
                messagebox.showinfo("Sucesso", "Tarefa removida com sucesso!")
                mostrar_tarefas()
    finally:
        desconectar_bd(db)

# Criar a interface gráfica
root = tk.Tk()
root.title("Stark Task Manager")

# Componentes da interface
label_descricao = tk.Label(root, text="Descrição:")
label_descricao.pack()

entry_descricao = tk.Entry(root, width=50)
entry_descricao.pack()

label_status = tk.Label(root, text="Status:")
label_status.pack()

combo_status = ttk.Combobox(root, values=["A Fazer", "Em Andamento", "Concluído"])
combo_status.pack()

frame_botoes = tk.Frame(root)
frame_botoes.pack(pady=10)

button_adicionar = tk.Button(frame_botoes, text="Adicionar Tarefa", command=adicionar_tarefa)
button_adicionar.pack(side=tk.LEFT, padx=10)

button_editar = tk.Button(frame_botoes, text="Editar Tarefa", command=editar_tarefa)
button_editar.pack(side=tk.LEFT, padx=10)

button_remover = tk.Button(frame_botoes, text="Remover Tarefa", command=remover_tarefa)
button_remover.pack(side=tk.LEFT, padx=10)

frame_tarefas = tk.Frame(root)
frame_tarefas.pack(pady=20)

label_tarefas = tk.Label(frame_tarefas, text="Lista de Tarefas")
label_tarefas.pack()

listbox_tarefas = tk.Listbox(frame_tarefas, width=60, height=10)
listbox_tarefas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar_tarefas = tk.Scrollbar(frame_tarefas, orient=tk.VERTICAL)
scrollbar_tarefas.pack(side=tk.RIGHT, fill=tk.Y)

listbox_tarefas.config(yscrollcommand=scrollbar_tarefas.set)
scrollbar_tarefas.config(command=listbox_tarefas.yview)

# Exibir tarefas ao iniciar
mostrar_tarefas()

# Estilizar a interface gráfica
root.configure(bg="black")  # Cor de fundo da janela principal
label_descricao.configure(fg="white", bg="black")  # Cores do texto e fundo do label
label_status.configure(fg="white", bg="black")  # Cores do texto e fundo do label
frame_botoes.configure(bg="black")  # Cor de fundo do frame dos botões
button_adicionar.configure(bg="green", fg="white")  # Cores do botão Adicionar
button_editar.configure(bg="orange", fg="white")  # Cores do botão Editar
button_remover.configure(bg="red", fg="white")  # Cores do botão Remover
label_tarefas.configure(fg="white", bg="black")  # Cores do texto e fundo do label Lista de Tarefas
listbox_tarefas.configure(bg="white", fg="black")  # Cores do fundo e texto da listbox

# Iniciar a interface gráfica
root.mainloop()
