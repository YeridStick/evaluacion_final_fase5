import argparse
import os
import tkinter as tk
from tkinter import messagebox
from datetime import datetime


APP_NAME = "Fase4YeridRamirez"
STUDENT_NAME = "Yerid Stick Ramirez Guzman"
PASSWORD = "ARBOL"
MAX_LEVELS = 4


class Node:
    def __init__(self, value, level=1):
        self.value = value
        self.level = level
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def clear(self):
        self.root = None

    def insert(self, value):
        if self.root is None:
            self.root = Node(value, 1)
            return True, "Nodo agregado correctamente."

        current = self.root
        while True:
            if value == current.value:
                return False, "El nodo ya existe en el árbol."

            next_level = current.level + 1

            if value < current.value:
                if current.left is None:
                    if next_level > MAX_LEVELS:
                        return False, "No puede exceder 4 niveles."
                    current.left = Node(value, next_level)
                    return True, "Nodo agregado correctamente."
                current = current.left
            else:
                if current.right is None:
                    if next_level > MAX_LEVELS:
                        return False, "No puede exceder 4 niveles."
                    current.right = Node(value, next_level)
                    return True, "Nodo agregado correctamente."
                current = current.right

    def search(self, value):
        current = self.root
        while current is not None:
            if value == current.value:
                return True
            if value < current.value:
                current = current.left
            else:
                current = current.right
        return False

    def preorder(self):
        result = []

        def walk(node):
            if node:
                result.append(node.value)
                walk(node.left)
                walk(node.right)

        walk(self.root)
        return result

    def inorder(self):
        result = []

        def walk(node):
            if node:
                walk(node.left)
                result.append(node.value)
                walk(node.right)

        walk(self.root)
        return result

    def postorder(self):
        result = []

        def walk(node):
            if node:
                walk(node.left)
                walk(node.right)
                result.append(node.value)

        walk(self.root)
        return result


class LoginWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title(APP_NAME)
        self.window.geometry("360x260")
        self.window.resizable(False, False)

        tk.Label(
            self.window,
            text="Aplicación: Árboles binarios",
            font=("Arial", 11)
        ).pack(pady=10)

        tk.Label(
            self.window,
            text=f"Estudiante: {STUDENT_NAME}",
            font=("Arial", 10)
        ).pack(pady=5)

        tk.Label(
            self.window,
            text=f"Fecha: {datetime.now().strftime('%d/%m/%Y')}",
            font=("Arial", 10)
        ).pack(pady=5)

        tk.Label(
            self.window,
            text="Contraseña:",
            font=("Arial", 10)
        ).pack(pady=10)

        self.password_entry = tk.Entry(self.window, show="*", justify="center")
        self.password_entry.pack()
        self.password_entry.bind("<Return>", lambda event: self.validate_password())

        tk.Button(
            self.window,
            text="Ingresar",
            command=self.validate_password
        ).pack(pady=15)

        self.window.mainloop()

    def validate_password(self):
        password = self.password_entry.get()

        if password == PASSWORD:
            self.window.destroy()
            MainWindow()
        else:
            messagebox.showerror("Error", "Contraseña incorrecta.")
            self.password_entry.delete(0, tk.END)


class MainWindow:
    def __init__(self):
        self.tree = BinarySearchTree()

        self.window = tk.Tk()
        self.window.title("Árbol Binario de Búsqueda")
        self.window.geometry("900x620")
        self.window.resizable(False, False)

        self.create_widgets()
        self.window.mainloop()

    def create_widgets(self):
        top_frame = tk.Frame(self.window)
        top_frame.pack(pady=10)

        self.value_entry = tk.Entry(top_frame, width=10, justify="center")
        self.value_entry.grid(row=0, column=0, padx=5)
        self.value_entry.bind("<Return>", lambda event: self.add_node())

        tk.Button(top_frame, text="Agregar Nodo", command=self.add_node).grid(row=0, column=1, padx=5)
        tk.Button(top_frame, text="Buscar Nodo", command=self.search_node).grid(row=0, column=2, padx=5)
        tk.Button(top_frame, text="Limpiar", command=self.clear_tree).grid(row=0, column=3, padx=5)
        tk.Button(top_frame, text="Salir", command=self.window.destroy).grid(row=0, column=4, padx=5)

        self.canvas = tk.Canvas(self.window, width=860, height=390, bg="white", highlightbackground="black")
        self.canvas.pack(padx=15, pady=10)

        bottom_frame = tk.Frame(self.window)
        bottom_frame.pack(pady=10)

        tk.Label(bottom_frame, text="Preorden").grid(row=0, column=0, padx=5)
        self.preorder_text = tk.Entry(bottom_frame, width=30)
        self.preorder_text.grid(row=0, column=1, padx=5)

        tk.Label(bottom_frame, text="Inorden").grid(row=0, column=2, padx=5)
        self.inorder_text = tk.Entry(bottom_frame, width=30)
        self.inorder_text.grid(row=0, column=3, padx=5)

        tk.Label(bottom_frame, text="Posorden").grid(row=0, column=4, padx=5)
        self.postorder_text = tk.Entry(bottom_frame, width=30)
        self.postorder_text.grid(row=0, column=5, padx=5)

    def get_integer_value(self):
        value = self.value_entry.get().strip()

        try:
            return int(value)
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número entero.")
            return None

    def add_node(self):
        value = self.get_integer_value()
        if value is None:
            return

        success, message = self.tree.insert(value)

        if not success:
            messagebox.showerror("Error", message)
        else:
            self.update_view()

        self.value_entry.delete(0, tk.END)

    def search_node(self):
        value = self.get_integer_value()
        if value is None:
            return

        exists = self.tree.search(value)

        if exists:
            messagebox.showinfo("Buscar Nodo", f"Valor {value} existe en el árbol.")
        else:
            messagebox.showinfo("Buscar Nodo", f"Valor {value} no existe en el árbol.")

        self.value_entry.delete(0, tk.END)

    def clear_tree(self):
        self.tree.clear()
        self.canvas.delete("all")
        self.set_entry_text(self.preorder_text, "")
        self.set_entry_text(self.inorder_text, "")
        self.set_entry_text(self.postorder_text, "")
        self.value_entry.delete(0, tk.END)

    def update_view(self):
        self.canvas.delete("all")

        if self.tree.root is not None:
            self.draw_tree(self.tree.root, 430, 40, 190)

        self.set_entry_text(self.preorder_text, self.format_list(self.tree.preorder()))
        self.set_entry_text(self.inorder_text, self.format_list(self.tree.inorder()))
        self.set_entry_text(self.postorder_text, self.format_list(self.tree.postorder()))

    def draw_tree(self, node, x, y, horizontal_distance):
        radius = 18

        if node.left:
            child_x = x - horizontal_distance
            child_y = y + 85
            self.canvas.create_line(x, y + radius, child_x, child_y - radius)
            self.draw_tree(node.left, child_x, child_y, horizontal_distance // 2)

        if node.right:
            child_x = x + horizontal_distance
            child_y = y + 85
            self.canvas.create_line(x, y + radius, child_x, child_y - radius)
            self.draw_tree(node.right, child_x, child_y, horizontal_distance // 2)

        self.canvas.create_oval(
            x - radius,
            y - radius,
            x + radius,
            y + radius,
            fill="#c9f6f7",
            outline="#4d9ea0"
        )
        self.canvas.create_text(x, y, text=str(node.value), font=("Arial", 10, "bold"))

    @staticmethod
    def format_list(values):
        return " ".join(str(value) for value in values)

    @staticmethod
    def set_entry_text(entry, text):
        entry.delete(0, tk.END)
        entry.insert(0, text)


def _parse_args():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--from-integrator", action="store_true")
    args, _ = parser.parse_known_args()
    return args


def main():
    args = _parse_args()
    run_from_integrator = args.from_integrator or os.getenv("RUN_FROM_INTEGRATOR", "").lower() == "true"

    if run_from_integrator:
        MainWindow()
    else:
        LoginWindow()


if __name__ == "__main__":
    main()

