# Application de gestion de Boulangerie (produits et commandes uniquement)

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestion de Boulangerie")
        self.geometry("800x600")
        
        # Création de la base de données
        self.conn = sqlite3.connect('boulangerie.db')
        self.create_tables()
        
        # Création des onglets
        self.tab_control = ttk.Notebook(self)
        self.tab_produit = ttk.Frame(self.tab_control)
        self.tab_commande = ttk.Frame(self.tab_control)
        
        self.tab_control.add(self.tab_produit, text='Produits')
        self.tab_control.add(self.tab_commande, text='Commandes')
        
        self.tab_control.pack(expand=1, fill='both')
        
        # Initialisation des onglets
        self.init_produit_tab()
        self.init_commande_tab()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS produits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                prix REAL NOT NULL,
                categorie TEXT NOT NULL,
                quantite INTEGER NOT NULL
            )
        ''')    
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS commandes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produit_id INTEGER NOT NULL,
                quantite INTEGER NOT NULL,
                FOREIGN KEY (produit_id) REFERENCES produits(id)
            )
        ''')
        
        self.conn.commit()
    
    def init_produit_tab(self):
        self.produit_frame = ttk.Frame(self.tab_produit)
        self.produit_frame.pack(fill='both', expand=True)
        
        # Liste des produits
        self.produit_listbox = tk.Listbox(self.produit_frame)
        self.produit_listbox.pack(side='left', fill='both', expand=True)
        self.produit_listbox.bind('<<ListboxSelect>>', self.on_produit_select)
        
        # Boutons pour ajouter, supprimer et mettre à jour les produits
        self.btn_add_produit = ttk.Button(self.produit_frame, text="Ajouter Produit", command=self.add_produit)
        self.btn_add_produit.pack(side='top', fill='x')
        
        self.btn_delete_produit = ttk.Button(self.produit_frame, text="Supprimer Produit", command=self.delete_produit)
        self.btn_delete_produit.pack(side='top', fill='x')
        
        self.btn_update_produit = ttk.Button(self.produit_frame, text="Mettre à Jour Produit", command=self.update_produit)
        self.btn_update_produit.pack(side='top', fill='x')
        
        self.load_produits()

    def load_produits(self):
        self.produit_listbox.delete(0, tk.END)
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM produits")
        for row in cursor.fetchall():
            self.produit_listbox.insert(tk.END, f"{row[1]} - {row[2]}€ - {row[3]} - {row[4]}") if row[4] > 0 else 0
        self.conn.commit()

    def on_produit_select(self, _):
        selected = self.produit_listbox.curselection()
        if selected:
            index = selected[0]
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM produits")
            produit = cursor.fetchall()[index]
            self.selected_produit_id = produit[0]
            self.selected_produit_nom = produit[1]
            self.selected_produit_prix = produit[2]
            self.selected_produit_categorie = produit[3]
            self.selected_produit_quantite = produit[4]
        else:
            self.selected_produit_id = None
            self.selected_produit_nom = None
            self.selected_produit_prix = None
            self.selected_produit_categorie = None
            self.selected_produit_quantite = None  

    def add_produit(self):
        def save_produit():
            nom = entry_nom.get()
            prix = entry_prix.get()
            categorie = entry_categorie.get()
            quantite = entry_quantite.get()
            
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM produits WHERE nom=? AND categorie=?",
                           (nom, categorie))
            if cursor.fetchone():
                messagebox.showerror("Erreur", "Le produit existe déjà.")
                return
            if nom and prix and categorie and quantite:
                cursor.execute("INSERT INTO produits (nom, prix, categorie, quantite) VALUES (?, ?, ?, ?)",
                               (nom, float(prix), categorie, int(quantite)))
                self.conn.commit()
                self.load_produits()
                add_window.destroy()
            else:
                messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
        
        add_window = tk.Toplevel(self)
        add_window.title("Ajouter Produit")
        
        ttk.Label(add_window, text="Nom:").pack(pady=5)
        entry_nom = ttk.Entry(add_window)
        entry_nom.pack(fill='x', padx=10)
        
        ttk.Label(add_window, text="Prix (€):").pack(pady=5)
        entry_prix = ttk.Entry(add_window)
        entry_prix.pack(fill='x', padx=10)
        
        ttk.Label(add_window, text="Catégorie:").pack(pady=5)
        entry_categorie = ttk.Combobox(add_window, values=["Pain", "Viennoiserie", "Pâtisserie"])
        entry_categorie.pack(fill='x', padx=10)
        entry_categorie['state'] = 'readonly'
        
        ttk.Label(add_window, text="Quantité:").pack(pady=5)
        entry_quantite = ttk.Entry(add_window)
        entry_quantite.pack(fill='x', padx=10)
        
        ttk.Button(add_window, text="Enregistrer", command=save_produit).pack(pady=10)

    def delete_produit(self):
        selected = self.produit_listbox.curselection()
        if selected:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM commandes WHERE produit_id=?", (self.selected_produit_id,))
            if cursor.fetchone():
                messagebox.showerror("Erreur", "Ce produit est associé à une ou plusieurs commandes et ne peut pas être supprimé.")
                return
            if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer ce produit ?"):
                index = selected[0]
                cursor = self.conn.cursor()
                cursor.execute("SELECT id FROM produits")
                produit_id = cursor.fetchall()[index][0]
                cursor.execute("DELETE FROM produits WHERE id=?", (produit_id,))
                self.conn.commit()
                self.load_produits()
        else:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un produit à supprimer.")

    def update_produit(self):
        if self.selected_produit_id is not None:
            def save_update():
                nom = entry_nom.get()
                prix = entry_prix.get()
                categorie = entry_categorie.get()
                quantite = entry_quantite.get()
                if nom and prix and categorie and quantite:
                    cursor = self.conn.cursor()
                    cursor.execute("UPDATE produits SET nom=?, prix=?, categorie=?, quantite=? WHERE id=?",
                                   (nom, float(prix), categorie, int(quantite), self.selected_produit_id))
                    self.conn.commit()
                    self.load_produits()
                    update_window.destroy()
                else:
                    messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
            
            update_window = tk.Toplevel(self)
            update_window.title("Mettre à Jour Produit")
            
            ttk.Label(update_window, text="Nom:").pack(pady=5)
            entry_nom = ttk.Entry(update_window)
            entry_nom.insert(0, self.selected_produit_nom)
            entry_nom.pack(fill='x', padx=10)
            
            ttk.Label(update_window, text="Prix:").pack(pady=5)
            entry_prix = ttk.Entry(update_window)
            entry_prix.insert(0, str(self.selected_produit_prix))
            entry_prix.pack(fill='x', padx=10)
            
            ttk.Label(update_window, text="Catégorie:").pack(pady=5)
            entry_categorie = ttk.Entry(update_window)
            entry_categorie.insert(0, self.selected_produit_categorie)
            entry_categorie.pack(fill='x', padx=10)
            
            ttk.Label(update_window, text="Quantité:").pack(pady=5)
            entry_quantite = ttk.Entry(update_window)
            entry_quantite.insert(0, str(self.selected_produit_quantite))
            entry_quantite.pack(fill='x', padx=10)
            
            ttk.Button(update_window, text="Enregistrer", command=save_update).pack(pady=10)
        else:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un produit à mettre à jour.")
      
    def init_commande_tab(self):
        self.commande_frame = ttk.Frame(self.tab_commande)
        self.commande_frame.pack(fill='both', expand=True)
        
        # Liste des commandes
        self.commande_listbox = tk.Listbox(self.commande_frame)
        self.commande_listbox.pack(side='left', fill='both', expand=True)
        self.commande_listbox.bind('<<ListboxSelect>>', self.on_commande_select)
        
        # Bouton pour ajouter une commande
        self.btn_add_commande = ttk.Button(self.commande_frame, text="Ajouter Commande", command=self.add_commande)
        self.btn_add_commande.pack(side='top', fill='x')
        
        self.load_commandes()

    def load_commandes(self):
        self.commande_listbox.delete(0, tk.END)
        cursor = self.conn.cursor()
        cursor.execute("SELECT c.id, p.nom, c.quantite FROM commandes c JOIN produits p ON c.produit_id = p.id")
        for row in cursor.fetchall():
            self.commande_listbox.insert(tk.END, f"Commande ID: {row[0]} - Produit: {row[1]} (quantité: {row[2]})")
        self.conn.commit()

    def on_commande_select(self, _):
        selected = self.commande_listbox.curselection()
        if selected:
            index = selected[0]
            cursor = self.conn.cursor()
            cursor.execute("SELECT c.id, p.nom, c.quantite FROM commandes c JOIN produits p ON c.produit_id = p.id")
            commande = cursor.fetchall()[index]
            self.selected_commande_id = commande[0]
            self.selected_produit_nom = commande[1]
            self.selected_quantite = commande[2]
        else:
            self.selected_commande_id = None
            self.selected_produit_nom = None
            self.selected_quantite = None

    def add_commande(self):
        def save_commande():
            produit_info = entry_produit.get()
            quantite = entry_quantite.get()
            if produit_info and quantite:
                produit_id = int(produit_info.split(' - ')[0])
                cursor = self.conn.cursor()
                cursor.execute("SELECT quantite FROM produits WHERE id=?", (produit_id,))
                stock = cursor.fetchone()
                if stock and int(quantite) <= stock[0]:
                    cursor.execute("INSERT INTO commandes (produit_id, quantite) VALUES (?, ?)",
                                   (produit_id, int(quantite)))
                    cursor.execute("UPDATE produits SET quantite = quantite - ? WHERE id=?", (int(quantite), produit_id))
                    self.conn.commit()
                    self.load_commandes()
                    self.load_produits()
                    add_window.destroy()
                else:
                    messagebox.showerror("Erreur", "Stock insuffisant pour cette commande.")
            else:
                messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
        
        add_window = tk.Toplevel(self)
        add_window.title("Ajouter Commande")

        ttk.Label(add_window, text="Sélectionnez le Produit:").pack(pady=5)
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, nom FROM produits WHERE quantite > 0")
        produits = [f"{row[0]} - {row[1]}" for row in cursor.fetchall()]
        entry_produit = ttk.Combobox(add_window, values=produits, state='readonly')
        entry_produit.pack(fill='x', padx=10)

        ttk.Label(add_window, text="Quantité:").pack(pady=5)
        entry_quantite = ttk.Entry(add_window)
        entry_quantite.pack(fill='x', padx=10)
        
        ttk.Button(add_window, text="Enregistrer", command=save_commande).pack(pady=10)

if __name__ == "__main__":
    app = Application()
    app.mainloop()
    app.conn.close()