# 🥖 Application de Gestion de Boulangerie

Cette application de bureau permet de gérer les **produits** et les **commandes** d’une boulangerie à travers une interface graphique conviviale développée avec **Tkinter**.

## 🚀 Fonctionnalités

### 🧺 Produits
- Ajouter un nouveau produit (nom, prix, catégorie, quantité)
- Modifier les informations d’un produit existant
- Supprimer un produit (sauf s’il est utilisé dans des commandes)
- Affichage des produits en stock uniquement

### 📦 Commandes
- Ajouter une commande liée à un produit existant
- Mise à jour automatique du stock après commande
- Affichage de toutes les commandes passées

## 🧱 Technologies utilisées

| Élément              | Détail                          |
|----------------------|---------------------------------|
| Langage              | Python 3.x                      |
| Interface graphique  | Tkinter                         |
| Base de données      | SQLite (via `sqlite3`)          |
| Interface utilisateur| `ttk.Notebook`, `Listbox`, `Entry`, `Combobox`, `Button` |

## 📂 Structure des données

### Table `produits`
| Champ      | Type     |
|------------|----------|
| id         | INTEGER (PK) |
| nom        | TEXT     |
| prix       | REAL     |
| categorie  | TEXT     |
| quantite   | INTEGER  |

### Table `commandes`
| Champ      | Type     |
|------------|----------|
| id         | INTEGER (PK) |
| produit_id | INTEGER (FK) |
| quantite   | INTEGER  |

## ▶️ Lancer l'application

```bash
python gestion_boulangerie.py
