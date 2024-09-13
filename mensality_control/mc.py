import json
import tkinter as tk
from tkinter import messagebox
import tkinter.simpledialog


class Mensalidade:
    def __init__(self, nome, valor):
        self.nome = nome
        self.valor = valor


class ControleMensalidadeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Controle de Mensalidades")

        self.controle = ControleMensalidade()
        self.controle.carregar_mensalidades()  # Carregar mensalidades do arquivo JSON

        self.frame = tk.Frame(root)
        self.frame.pack(padx=20, pady=20)

        self.label = tk.Label(self.frame, text="Mensalidades")
        self.label.pack()

        self.listbox = tk.Listbox(self.frame, width=40, height=10)
        self.listbox.pack()

        self.atualizar_lista_mensalidades()

        self.adicionar_btn = tk.Button(self.frame, text="Adicionar Mensalidade", command=self.adicionar_mensalidade)
        self.adicionar_btn.pack(pady=5)

        self.remover_btn = tk.Button(self.frame, text="Remover Mensalidade", command=self.remover_mensalidade)
        self.remover_btn.pack(pady=5)

        # Salvar mensalidades ao fechar a janela
        root.protocol("WM_DELETE_WINDOW", self.fechar_janela)

    def adicionar_mensalidade(self):
        nome = tk.simpledialog.askstring("Adicionar Mensalidade", "Digite o nome da mensalidade:")
        if nome:
            valor = tk.simpledialog.askfloat("Adicionar Mensalidade", "Digite o valor da mensalidade:")
            if valor is not None:
                self.controle.adicionar_mensalidade(nome, valor)
                self.atualizar_lista_mensalidades()
                messagebox.showinfo("Sucesso", "Mensalidade adicionada com sucesso.")

    def remover_mensalidade(self):
        selecionado = self.listbox.curselection()
        if selecionado:
            indice = int(selecionado[0])
            self.controle.remover_mensalidade(indice)
            self.atualizar_lista_mensalidades()
            messagebox.showinfo("Sucesso", "Mensalidade removida com sucesso.")
        else:
            messagebox.showwarning("Aviso", "Selecione uma mensalidade para remover.")

    def atualizar_lista_mensalidades(self):
        self.listbox.delete(0, tk.END)
        for mensalidade in self.controle.mensalidades:
            self.listbox.insert(tk.END, f"{mensalidade.nome}: R$ {mensalidade.valor:.2f}")

    def fechar_janela(self):
        self.controle.salvar_mensalidades()  # Salvar mensalidades no arquivo JSON
        self.root.destroy()


class ControleMensalidade:
    def __init__(self):
        self.mensalidades = []

    def adicionar_mensalidade(self, nome, valor):
        mensalidade = Mensalidade(nome, valor)
        self.mensalidades.append(mensalidade)

    def remover_mensalidade(self, indice):
        del self.mensalidades[indice]

    def carregar_mensalidades(self):
        try:
            with open("mensalidades.json", "r") as f:
                data = json.load(f)
                self.mensalidades = [Mensalidade(m['nome'], m['valor']) for m in data]
        except FileNotFoundError:
            print("Arquivo de mensalidades não encontrado.")

    def salvar_mensalidades(self):
        with open("mensalidades.json", "w") as f:
            json.dump([vars(m) for m in self.mensalidades], f)


def main():
    root = tk.Tk()
    app = ControleMensalidadeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

