import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import os
from tkcalendar import Calendar, DateEntry

class GimnasioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gimnasio")
        self.root.geometry("1000x650")
        self.root.configure(bg="#f0f0f0")

        self.miembros = []
        self.column_indexes = {"Nombre": 0, "CI": 1, "Inicio de Inscripción": 2, "Pagado": 3}
        self.sort_direction = {"Nombre": False, "CI": False, "Inicio de Inscripción": False, "Pagado": False}
        self.selected_item = None

        self.crear_widgets()
        self.actualizar_lista()

        # Agregar mensaje adicional
        mensaje_adicional = tk.Label(self.root, text="Muchas gracias por preferir a DevSpark comuníquese con nosotros a través de Whatsapp +50407186 o en Facebook como DevSpark", font=("Helvetica", 8), bg="#f0f0f0", fg="#333")
        mensaje_adicional.pack(pady=5)

    def crear_widgets(self):
        # Título
        titulo = tk.Label(self.root, text="꧁ঔৣ☬✞Gimnasio✞☬ঔৣ꧂", font=("Helvetica", 16), bg="#f0f0f0", fg="#333")
        titulo.pack(pady=10)

        # Formulario
        frame_formulario = tk.Frame(self.root, bg="#f0f0f0")
        frame_formulario.pack(pady=10, fill=tk.X)

        # Utiliza grid para el layout del formulario
        self.entry_nombre = tk.Entry(frame_formulario)
        self.entry_nombre.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)

        tk.Label(frame_formulario, text="Nombre:", bg="#f0f0f0").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        self.entry_ci = tk.Entry(frame_formulario)
        self.entry_ci.grid(row=0, column=3, sticky=tk.EW, padx=5, pady=5)

        tk.Label(frame_formulario, text="CI:", bg="#f0f0f0").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)

        self.entry_inicio_inscripcion = DateEntry(frame_formulario, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/MM/yyyy')
        self.entry_inicio_inscripcion.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)

        tk.Label(frame_formulario, text="Inicio de Inscripción:", bg="#f0f0f0").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

        self.var_pagado = tk.BooleanVar()
        self.check_pagado = tk.Checkbutton(frame_formulario, text="Pagado", variable=self.var_pagado, bg="#f0f0f0")
        self.check_pagado.grid(row=1, column=2, columnspan=2, sticky=tk.W, padx=5, pady=5)

        frame_botones = tk.Frame(frame_formulario, bg="#f0f0f0")
        frame_botones.grid(row=2, column=0, columnspan=4, pady=10, sticky=tk.EW)

        self.boton_agregar = tk.Button(frame_botones, text="Agregar", command=self.agregar_miembro, bg="#4CAF50", fg="white", padx=10, pady=5)
        self.boton_agregar.pack(side=tk.LEFT, padx=5)

        self.boton_actualizar = tk.Button(frame_botones, text="Actualizar", command=self.actualizar_miembro, bg="#9370DB", fg="white", padx=10, pady=5)
        self.boton_actualizar.pack(side=tk.LEFT, padx=5)

        self.boton_buscar = tk.Button(frame_botones, text="Buscar", command=self.buscar_miembros, bg="#2196F3", fg="white", padx=10, pady=5)
        self.boton_buscar.pack(side=tk.LEFT, padx=5)

        self.boton_eliminar = tk.Button(frame_botones, text="Eliminar", command=self.eliminar_miembro, bg="#F44336", fg="white", padx=10, pady=5)
        self.boton_eliminar.pack(side=tk.LEFT, padx=5)

        self.boton_guardar = tk.Button(frame_botones, text="Guardar", command=self.guardar_miembros, bg="#FFFF00", fg="black", padx=10, pady=5)
        self.boton_guardar.pack(side=tk.LEFT, padx=5)

        # Treeview
        self.tree = ttk.Treeview(self.root, columns=list(self.column_indexes.keys()), show="headings", height=15)
        self.tree.pack(pady=10, fill=tk.X)

        for column, index in self.column_indexes.items():
            self.tree.heading(column, text=column, command=lambda c=column: self.sort_column(c))
            self.tree.column(column, width=100, anchor="center")

        self.tree.tag_configure("pagado", foreground="green")
        self.tree.tag_configure("no_pagado", foreground="red")

        self.tree.bind("<Double-1>", self.on_double_click)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def actualizar_lista(self):
        # Limpiar el Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Agregar los miembros al Treeview
        for miembro in self.miembros:
            tag = "pagado" if miembro["Pagado"] else "no_pagado"
            self.tree.insert("", tk.END, values=list(miembro.values()), tags=(tag,))

    def agregar_miembro(self):
        nombre = self.entry_nombre.get().strip()
        ci = self.entry_ci.get().strip()
        inicio_inscripcion = self.entry_inicio_inscripcion.get()
        pagado = self.var_pagado.get()

        if nombre and ci and inicio_inscripcion:
            nuevo_miembro = {
                "Nombre": nombre,
                "CI": ci,
                "Inicio de Inscripción": inicio_inscripcion,
                "Pagado": pagado
            }
            self.miembros.append(nuevo_miembro)
            self.actualizar_lista()
            self.limpiar_formulario()
            messagebox.showinfo("Datos guardados", "Los datos se han guardado correctamente.")
        else:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")

    def actualizar_miembro(self):
        if self.selected_item is not None:
            nombre = self.entry_nombre.get().strip()
            ci = self.entry_ci.get().strip()
            inicio_inscripcion = self.entry_inicio_inscripcion.get()
            pagado = self.var_pagado.get()

            if nombre and ci and inicio_inscripcion:
                self.miembros[self.selected_item] = {
                    "Nombre": nombre,
                    "CI": ci,
                    "Inicio de Inscripción": inicio_inscripcion,
                    "Pagado": pagado
                }
                self.actualizar_lista()
                self.limpiar_formulario()
                messagebox.showinfo("Datos actualizados", "Los datos se han actualizado correctamente.")
            else:
                messagebox.showerror("Error", "Por favor, complete todos los campos.")
        else:
            messagebox.showerror("Error", "Seleccione un miembro para actualizar.")

    def buscar_miembros(self):
        nombre = self.entry_nombre.get().strip()
        ci = self.entry_ci.get().strip()

        if nombre or ci:
            resultados = [miembro for miembro in self.miembros if (nombre and nombre.lower() in miembro["Nombre"].lower()) or (ci and ci in miembro["CI"])]
            self.actualizar_lista(resultados)
        else:
            self.actualizar_lista()

    def eliminar_miembro(self):
        if self.selected_item is not None:
            confirmacion = messagebox.askyesno("Confirmar eliminación", "¿Estás seguro de que quieres eliminar este miembro?")
            if confirmacion:
                del self.miembros[self.selected_item]
                self.actualizar_lista()
                self.limpiar_formulario()
                messagebox.showinfo("Miembro eliminado", "El miembro ha sido eliminado correctamente.")
        else:
            messagebox.showerror("Error", "Selecciona un miembro para eliminar.")

    def guardar_miembros(self):
        if self.miembros:
            with open("miembros.txt", "w") as f:
                for miembro in self.miembros:
                    f.write(f"{miembro['Nombre']},{miembro['CI']},{miembro['Inicio de Inscripción']},{miembro['Pagado']}\n")
            messagebox.showinfo("Datos guardados", "Los datos se han guardado correctamente.")
        else:
            messagebox.showerror("Error", "No hay miembros para guardar.")

    def sort_column(self, column):
        self.sort_direction[column] = not self.sort_direction[column]
        self.miembros.sort(key=lambda x: x[column], reverse=self.sort_direction[column])
        self.actualizar_lista()

    def on_double_click(self, event):
        item = self.tree.selection()[0]
        index = self.tree.index(item)
        miembro = self.miembros[index]

        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, miembro["Nombre"])
        self.entry_ci.delete(0, tk.END)
        self.entry_ci.insert(0, miembro["CI"])
        self.entry_inicio_inscripcion.set_date(datetime.strptime(miembro["Inicio de Inscripción"], "%d/%m/%Y"))
        self.var_pagado.set(miembro["Pagado"])

        self.selected_item = index

    def on_select(self, event):
        item = self.tree.selection()[0]
        index = self.tree.index(item)
        miembro = self.miembros[index]

        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, miembro["Nombre"])
        self.entry_ci.delete(0, tk.END)
        self.entry_ci.insert(0, miembro["CI"])
        self.entry_inicio_inscripcion.set_date(datetime.strptime(miembro["Inicio de Inscripción"], "%d/%m/%Y"))
        self.var_pagado.set(miembro["Pagado"])

        self.selected_item = index

    def limpiar_formulario(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_ci.delete(0, tk.END)
        self.entry_inicio_inscripcion.set_date(datetime.now())
        self.var_pagado.set(False)
        self.selected_item = None

if __name__ == "__main__":
    root = tk.Tk()
    app = GimnasioApp(root)
    root.mainloop()