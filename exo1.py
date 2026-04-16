import tkinter as tk
from tkinter import messagebox
import sqlite3

conn = sqlite3.connect("contacts.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT,
    telephone TEXT
)
""")
conn.commit()

def ajouter_contact():
    nom = entry_nom.get()
    tel = entry_tel.get()

    if nom == "" or tel == "":
        messagebox.showwarning("Attention", "Remplir tous les champs")
        return

    cursor.execute("INSERT INTO contacts (nom, telephone) VALUES (?, ?)", (nom, tel))
    conn.commit()

    afficher_contacts()
    entry_nom.delete(0, tk.END)
    entry_tel.delete(0, tk.END)

def afficher_contacts():
    listbox.delete(0, tk.END)
    cursor.execute("SELECT * FROM contacts")
    for contact in cursor.fetchall():
        listbox.insert(tk.END, f"{contact[0]} - {contact[1]} ({contact[2]})")

def supprimer_contact():
    selected = listbox.curselection()
    if not selected:
        return

    item = listbox.get(selected[0])
    contact_id = item.split(" - ")[0]

    cursor.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
    conn.commit()

    afficher_contacts()

root = tk.Tk()
root.title("Gestion des Contacts")

tk.Label(root, text="Nom").pack()
entry_nom = tk.Entry(root)
entry_nom.pack()

tk.Label(root, text="Téléphone").pack()
entry_tel = tk.Entry(root)
entry_tel.pack()

tk.Button(root, text="Ajouter", command=ajouter_contact).pack()
tk.Button(root, text="Supprimer", command=supprimer_contact).pack()

listbox = tk.Listbox(root, width=40)
listbox.pack()

afficher_contacts()

root.mainloop()