import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter.ttk import Combobox
import sqlite3


class RegistrationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dispositivos Ffex - Sistema Completo")
        self.root.geometry("450x600")
        self.db_name = "cadastro.db"
        self.init_db()
        self.create_ui()

    def init_db(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dispositivo TEXT NOT NULL,
                serie TEXT UNIQUE,
                estado TEXT NOT NULL,
                observacao TEXT,
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def create_ui(self):
        tk.Label(self.root, text="Controle de Dispositivos", font=("Arial", 16, "bold")).pack(pady=15)

        # Campos de Entrada
        tk.Label(self.root, text="Tipo de Dispositivo:").pack()
        self.dispositivo_entry = Combobox(self.root, values=["Laptop", "Teclado", "Mouse", "Fone de Ouvido"], width=37)
        self.dispositivo_entry.current(0)
        self.dispositivo_entry.pack(pady=5)

        tk.Label(self.root, text="N° de Série (9 dígitos):").pack()
        self.serie_entry = tk.Entry(self.root, width=40)
        self.serie_entry.pack(pady=5)

        tk.Label(self.root, text="Estado de Conservação:").pack()
        self.estado_entry = Combobox(self.root, values=["Ativo", "Inativo", "Manutenção", "Indefinido"], width=37)
        self.estado_entry.current(0)
        self.estado_entry.pack(pady=5)

        tk.Label(self.root, text="Observações:").pack()
        self.observacao_entry = tk.Entry(self.root, width=40)
        self.observacao_entry.pack(pady=5)

        # Frame de Botões
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        
        btn_style = {"bg": "#2b5b84", "fg": "white", "width": 12, "font": ("Arial", 9, "bold")}

        tk.Button(button_frame, text="Salvar/Atualizar", command=self.save_user, **btn_style).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Buscar/Editar", command=self.load_for_edit, **btn_style).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="Listar Todos", command=self.list_users, **btn_style).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Excluir", command=self.delete_user, bg="#dc3545", fg="white", width=12, font=("Arial", 9, "bold")).grid(row=1, column=1, padx=5, pady=5)
        
        tk.Button(self.root, text="Exportar para Excel", command=self.export_to_excel, bg="#28a745", fg="white", width=28, font=("Arial", 10, "bold")).pack(pady=10)
        tk.Button(self.root, text="Limpar Campos", command=self.clear_fields, width=32).pack()

    def save_user(self):
        dispositivo = self.dispositivo_entry.get()
        serie = self.serie_entry.get()
        estado = self.estado_entry.get()
        observacao = self.observacao_entry.get()

        if not dispositivo or not serie:
            messagebox.showerror("Erro", "Dispositivo e N° de série são obrigatórios!")
            return
        if len(serie) != 9:
            messagebox.showerror("Erro", "O N° de série deve ter 9 caracteres!")
            return

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id FROM usuarios WHERE serie = ?', (serie,))
        exists = cursor.fetchone()

        if exists:
            if messagebox.askyesno("Confirmar", "Série já cadastrada. Atualizar dados?"):
                cursor.execute('UPDATE usuarios SET dispositivo=?, estado=?, observacao=? WHERE serie=?', (dispositivo, estado, observacao, serie))
                messagebox.showinfo("Sucesso", "Dados atualizados!")
        else:
            cursor.execute('INSERT INTO usuarios (dispositivo, serie, estado, observacao) VALUES (?, ?, ?, ?)', (dispositivo, serie, estado, observacao))
            messagebox.showinfo("Sucesso", "Cadastrado com sucesso!")

        conn.commit()
        conn.close()
        self.clear_fields()

    def load_for_edit(self):
        serie_busca = simpledialog.askstring("Editar", "Digite o N° de série:")
        if not serie_busca: return

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE serie = ?', (serie_busca,))
        user = cursor.fetchone()
        conn.close()

        if user:
            self.clear_fields()
            self.dispositivo_entry.set(user[1])
            self.serie_entry.insert(0, user[2])
            self.estado_entry.set(user[3])
            self.observacao_entry.insert(0, user[4])
        else:
            messagebox.showerror("Erro", "Não encontrado.")

    def delete_user(self):
        serie_del = simpledialog.askstring("Excluir", "Digite o N° de série do dispositivo que deseja APAGAR:")
        if not serie_del: return

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT dispositivo FROM usuarios WHERE serie = ?', (serie_del,))
        found = cursor.fetchone()

        if found:
            if messagebox.askconfirm("Atenção", f"Tem certeza que deseja excluir o {found[0]} (Série: {serie_del})?"):
                cursor.execute('DELETE FROM usuarios WHERE serie = ?', (serie_del,))
                conn.commit()
                messagebox.showinfo("Sucesso", "Dispositivo removido do sistema.")
        else:
            messagebox.showerror("Erro", "Série não encontrada.")
        
        conn.close()
        self.clear_fields()

    def list_users(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT dispositivo, serie, estado FROM usuarios')
        users = cursor.fetchall()
        conn.close()

        if not users:
            messagebox.showinfo("Vazio", "Nenhum registro encontrado.")
            return

        lista = "\n".join([f"{u[0]} | SN: {u[1]} | {u[2]}" for u in users])
        messagebox.showinfo("Inventário Atual", lista)

    def clear_fields(self):
        self.dispositivo_entry.set("Laptop")
        self.serie_entry.delete(0, tk.END)
        self.estado_entry.set("Ativo")
        self.observacao_entry.delete(0, tk.END)

    def export_to_excel(self):
        conn = sqlite3.connect(self.db_name)
        df = pd.read_sql_query("SELECT * FROM usuarios", conn)
        conn.close()
        if not df.empty:
            df.to_excel("inventario_ffex.xlsx", index=False)
            messagebox.showinfo("Exportar", "Arquivo 'inventario_ffex.xlsx' gerado!")

if __name__ == "__main__":
    root = tk.Tk()
    app = RegistrationApp(root)
    root.mainloop()
