import tkinter as tk
from tkinter import messagebox
import sqlite3

conn = sqlite3.connect("bibliotheque.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS livres (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre TEXT,
    auteur TEXT,
    annee INTEGER
)
""")
conn.commit()

def ajouter_livre():
    titre = entry_titre.get()
    auteur = entry_auteur.get()
    annee = entry_annee.get()

    if titre == "" or auteur == "" or annee == "":
        messagebox.showwarning("Attention", "Tous les champs sont obligatoires")
        return

    cursor.execute("INSERT INTO livres (titre, auteur, annee) VALUES (?, ?, ?)",
                   (titre, auteur, annee))
    conn.commit()

    afficher_livres()
    vider_champs()

def afficher_livres():
    listbox.delete(0, tk.END)
    cursor.execute("SELECT * FROM livres")
    for livre in cursor.fetchall():
        listbox.insert(tk.END, f"{livre[0]} - {livre[1]} | {livre[2]} ({livre[3]})")

def supprimer_livre():
    selected = listbox.curselection()
    if not selected:
        return

    item = listbox.get(selected[0])
    livre_id = item.split(" - ")[0]

    cursor.execute("DELETE FROM livres WHERE id=?", (livre_id,))
    conn.commit()

    afficher_livres()

def rechercher_livre():
    mot = entry_recherche.get()

    listbox.delete(0, tk.END)
    cursor.execute("""
    SELECT * FROM livres
    WHERE titre LIKE ? OR auteur LIKE ?
    """, ('%' + mot + '%', '%' + mot + '%'))

    for livre in cursor.fetchall():
        listbox.insert(tk.END, f"{livre[0]} - {livre[1]} | {livre[2]} ({livre[3]})")

def vider_champs():
    entry_titre.delete(0, tk.END)
    entry_auteur.delete(0, tk.END)
    entry_annee.delete(0, tk.END)

root = tk.Tk()
root.title("Gestion Bibliothèque")

tk.Label(root, text="Titre").pack()
entry_titre = tk.Entry(root)
entry_titre.pack()

tk.Label(root, text="Auteur").pack()
entry_auteur = tk.Entry(root)
entry_auteur.pack()

tk.Label(root, text="Année").pack()
entry_annee = tk.Entry(root)
entry_annee.pack()

tk.Button(root, text="Ajouter", command=ajouter_livre).pack()
tk.Button(root, text="Supprimer", command=supprimer_livre).pack()

tk.Label(root, text="Recherche").pack()
entry_recherche = tk.Entry(root)
entry_recherche.pack()

tk.Button(root, text="Rechercher", command=rechercher_livre).pack()

listbox = tk.Listbox(root, width=50)
listbox.pack()

afficher_livres()

root.mainloop()